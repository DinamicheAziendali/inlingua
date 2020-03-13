# -*- coding: utf-8 -*-

import datetime
import logging

import croniter
from dateutil.parser import parse

from odoo import models, fields

_logger = logging.getLogger('lesson_scheduler')


class WeeklySchedule(models.Model):
    _name = 'timetable.weekly_schedule'
    _description = 'Scheduling rule'

    #resource_id = fields.Many2one(string='Resource', comodel_name='resource.resource', required=True)
    resource_id = fields.Many2one(string='Resource', comodel_name='res.partner', domain="[('professor', '=', True)]",
                                required=True)

    weekday = fields.Selection(
        [
            (1, "Lunedì"), (2, "Martedì"), (3, "Mercoledì"),
            (4, "Giovedì"), (5, "Venerdì"), (6, "Sabato"), (7, "Domenica")
        ],
        string="Giorno",
        required=True
    )  # fields.Integer(string="week day (from 1 to 7)", required=True)
    start_time = fields.Text(string='hh:mm', required="true")
    modules = fields.Integer(string='Modules', required=True)
    scheduling_rule_id = fields.Many2one('timetable.scheduling_rule')


class SchedulingRule(models.Model):
    _name = 'timetable.scheduling_rule'
    _description = 'Weekly schedule on timetable scheduler'

    name = fields.Text()
    course_id = fields.Many2one(string='Corso', comodel_name='project.project', required=True)
    scheduling_start = fields.Date(string="Dopo il giorno", required=True)

    # Scheduling settings
    weekly_schedules_ids = fields.One2many(
        'timetable.weekly_schedule', 'scheduling_rule_id', string='Course', required=True
    )

    def next_weekday(self, date, weekday):
        day_gap = weekday - date.weekday()
        if day_gap <= 0:
            day_gap += 7
        return date + datetime.timedelta(days=day_gap)

    # calcola la prima data utile per schedulare una lezione
    def get_next_schedule(self, start_date):
        available_schedules = []
        for schedule in self.weekly_schedules_ids:
            start_hhmm = schedule.start_time.split(':', 2)
            schedule_cron = "" + start_hhmm[1] + " " + start_hhmm[0] + " * * " + str(schedule.weekday) + ""
            cron = croniter.croniter(schedule_cron, start_date)
            next_date = cron.get_next(datetime.datetime)
            computed_schedule = {'date': next_date, 'obj': schedule}
            available_schedules.append(computed_schedule)

        return sorted(available_schedules, key=lambda sch: sch['date'])[0]

    # check for scheduling overlapping
    # ignoring owned schedules in case of update
    def handle_scheduling_rule(self):
        module_size = 60  # todo retrieve by contract
        total_modules = 20  # todo retrieve by contract
        already_scheduled = 0  # todo retrieve by DB
        remaining_minutes = (total_modules * module_size) - already_scheduled
        current_date = parse(self.scheduling_start)
        iterations = 0
        while remaining_minutes > 0:
            iterations += 1
            schedule = self.get_next_schedule(current_date)
            schedule_obj = schedule['obj']
            schedule_date = schedule['date']

            # schedulo fino a fullfill dei minuti totali del corso

            lesson_minutes = schedule_obj.modules * module_size

            minutes_to_schedule = lesson_minutes if lesson_minutes < remaining_minutes else remaining_minutes

            # aggiungo i minuti calcolati in precedenza per generare l'intervallo
            end_ts = schedule_date + datetime.timedelta(minutes=minutes_to_schedule)

            # creo l'elemento potenzialmente schedulabile
            lesson = {
                "name": "lession " + str(iterations) + " of course",
                "resource_id": int(schedule_obj.resource_id.id),
                "course_id": int(self.course_id.id),
                "start_time": schedule_date.strftime('%Y-%m-%d %H:%M:%S.000000'),
                "end_time": end_ts.strftime('%Y-%m-%d %H:%M:%S.000000'),
            }

            try:
                self.env['timetable.lesson'].create(lesson)
                # sottraggo i minuti gia verificati
                remaining_minutes -= minutes_to_schedule
                current_date = end_ts + datetime.timedelta(minutes=1)
            except Exception as error:
                raise Exception(
                    'impossibile allocare il docente ' + schedule_obj.resource.name + ' alla lezione ...'
                )

        return True

    _constraints = [(handle_scheduling_rule, 'Invalid scheduling rules', ['weekly_schedules_ids', 'scheduling_start'])]
