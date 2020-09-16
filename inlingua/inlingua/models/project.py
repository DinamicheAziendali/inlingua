###
# -*- coding: utf-8 -*-
# Copyright (C) 2018-2019:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# @author: Antonio Arcucci (antonio.arcucci@logicos.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
###

import logging
from datetime import datetime, timedelta

import croniter
from dateutil.parser import parse

from odoo import fields, models, api
from odoo.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ProjectInherit(models.Model):
    _inherit = 'project.project'

    description     = fields.Char(string='Description')

    language_id     = fields.Many2one('class.language', string='Course Language')
    course_type_id  = fields.Many2one('class.type',     string='Course Type')
    programm_id     = fields.Many2one('class.programm', string='Programm')

    student_number  = fields.Integer(string='Student Number')
    start_level     = fields.Many2one('student.level', string='Start Level')
    now_level       = fields.Many2one('student.level', string='Now Level')
    target_level    = fields.Many2one('student.level', string='Target Level')

    flexible_course     = fields.Boolean(string='Flexible Course')
    managed_by_teacher  = fields.Boolean(string='Managed By Teacher')
    date_start          = fields.Date(string='Expected Date Start', required=True)
    date_end            = fields.Date(string='Expected Date End')
    date_last_lesson    = fields.Date(compute='get_last_timetable_lesson',
                                        string='Last timetable lesson')

    # office_in = fields.Boolean(string='In')
    # office_out = fields.Boolean(string='Out')
    type_office         = fields.Selection([
                            ('in', 'In'),
                            ('out', 'Out')
                        ], string='Tipo Sede')

    office_id           = fields.Many2one('office.office', string='Office')

    number_of_module    = fields.Integer('number of module')
    module4lesson       = fields.Integer('number of module for lesson')
    module_type_id      = fields.Many2one('module.type', string='Duration Module', track_visibility='onchange')
    duration_lessons    = fields.Integer(string='Duration Lesson', compute='compute_duration_lesson')
    project_student_ids = fields.One2many('project.student', 'project_id', string='Students')
    contract_ids        = fields.One2many('private.contract', 'project_course_id')

    allow_timesheets    = fields.Boolean("Allow timesheets", default=False)
    label_tasks         = fields.Char(string='Use Lessons as', default='Lezioni',
                              help="Gives label to lessons on course's kanban view.")

    # Minuti già schedulati su timetable
    minutes_scheduled   = fields.Integer( string='Minuti schedulati',
                                          compute='get_scheduled_minutes')

    # Minuti rimanenti da schedulare
    minutes_remaining   = fields.Integer( string='Minuti da schedulare',
                                          compute='get_minutes_remaining')          

    # Lezioni già schedulati su timetable
    modules_scheduled   = fields.Integer( string='Moduli schedulati',
                                          compute='get_modules_scheduled')

    # Lezioni rimanenti da schedulare
    modules_remaining   = fields.Integer( string='Moduli da schedulare',
                                          compute='get_modules_remaining')                                

    # Scheduling settings (Frequenza)
    scheduling_rules_ids = fields.One2many( comodel_name='project.task_scheduling_rule',
                                            inverse_name='project_id',
                                            string='Schedulazioni',
                                            required=True
                                        )

    # Calcolo numero di moduli schedulati
    @api.depends('minutes_scheduled')
    @api.onchange('duration_lessons')
    def get_modules_scheduled(self):
        # import pdb; pdb.set_trace()
        self.modules_scheduled = 0
        if self.duration_lessons > 0:
            self.modules_scheduled = self.minutes_scheduled / self.duration_lessons

    # Calcolo numero di moduli restanti da schedulare
    @api.depends('minutes_scheduled')
    @api.onchange('duration_lessons', 'number_of_module')
    def get_modules_remaining(self):
        #import pdb; pdb.set_trace()
        self.modules_remaining = 0
        module_size         = self.module_type_id.time
        #if self.duration_lessons > 0:
        #     self.modules_remaining = ((self.number_of_module * self.duration_lessons) - self.minutes_scheduled) / self.duration_lessons

        if module_size > 0:
            self.modules_remaining = ((self.number_of_module * module_size) - self.minutes_scheduled) / module_size

    # Calcolo numero di minuti restanti da schedulare
    @api.depends('minutes_scheduled')
    @api.onchange('duration_lessons', 'number_of_module')
    def get_minutes_remaining(self):
        # import pdb; pdb.set_trace()
        self.minutes_remaining = (self.number_of_module * self.duration_lessons) - self.minutes_scheduled

    # Prelievo dell'ultima lezione presente sul timetable
    # @api.depends('amount_untaxed', 'purchase_order_ids')
    def get_last_timetable_lesson(self):
        oLezione = self.env['project.task']
        # import pdb; pdb.set_trace()
        
        lesson = oLezione.search([('project_id', '=', self.id)], order="start_time desc", limit=1)
        self.date_last_lesson = lesson.start_time
            

    @api.constrains('module_type_id')
    def check_time(self):
        for course in self:
            for module_type in course.module_type_id:
                if not module_type.time or module_type.time < 1:
                    raise ValidationError('Duration module must be greater 0')

    # sql contraints non funziona e la constrains con
    # le api odoo non entra prp nella funzione
    # _sql_constraints = [
    #     ('name_unique',
    #      'unique(name)',
    #      'Name Course must be unique!'),]

    # @api.multi
    # @api.constrains('name')
    # def _check_name_project(self):
    #     projects = self.env['project.project'].search([()])
    #     project_name = projects.mapped('name')
    #     for project in self:
    #         if project.name in project_name:
    #             raise ValidationError(
    #                 ('Name Course must be unique')
    #             )

    # Methods
    def schedule_lessons(self, args):
        self.handle_scheduling_rule(args)

    # calcola la prima data utile per schedulare una lezione
    def get_next_schedule(self, start_date):
        available_schedules = []
        for schedule in self.scheduling_rules_ids:
            start_h = int(schedule.start_time)  # recupero ore di inizio
            start_m = int((schedule.start_time - start_h) * 60)  # recupero ore di fine

            # test per ora legale
            #start_h -= 2

            # start_hhmm = # schedule.start_time.split(':', 2)
            schedule_cron       = "" + str(start_m) + " " + str(start_h) + " * * " + str(schedule.weekday) + ""
            cron                = croniter.croniter(schedule_cron, start_date)
            next_date           = cron.get_next(datetime)
            computed_schedule   = {'date': next_date, 'obj': schedule}
            available_schedules.append(computed_schedule)

        return sorted(available_schedules, key=lambda sch: sch['date'])[0]

    # Clears scheduled lessons after specified date
    def clear_future_lessons(self, date):
        env = self.env
        task_model = env['project.task']
        scheduled_lessons = task_model.search([
            ('project_id', '=', self.id),
            ('start_time', '>', date.strftime("%Y-%m-%d"))
        ])
        for lesson in scheduled_lessons:
            logger.info('Removing future lesson %s  starting at  %s ', lesson.name, lesson.start_time)
            lesson.unlink()

    # Get already scheduled time in minutes before specified date
    def get_scheduled_minutes(self):
        env = self.env
        task_model = env['project.task']
        result = 0
        logger.info(' *** Ricerca lezioni già presente project_id %s', self.id)
        scheduled_lessons = task_model.search([
            ('project_id', '=', self.id),
            #('start_time', '<', date.strftime("%Y-%m-%d"))
        ])
        for lesson in scheduled_lessons:
            if lesson.end_time and lesson.start_time:
                diff = datetime.strptime(lesson.end_time, '%Y-%m-%d %H:%M:%S') - \
                       datetime.strptime(lesson.start_time, '%Y-%m-%d %H:%M:%S')
                t = (diff.seconds + diff.microseconds / 1000000.0) / 60.0
                logger.info('Counting past scheduled lesson %s min [ %s ]', t, lesson.start_time)
                # They are now in seconds, subtract and then divide by 60 to get minutes.
                result += t

        logger.info('Total past scheduled time %s minutes', result)
        self.minutes_scheduled = result 
        return result

    # Fill empty spaces starting from specified date according to scheduling rule
    def fill_scheduling_rule(self, args, start_time=None):
        self.handle_scheduling_rule(args, start_time=start_time, skip_conflicts=True)

    # Append after last lesson of this course according to scheduling rules
    def append_scheduling_rule(self, args):
        env = self.env
        task_model = env['project.task']

        last_lesson = task_model.search([('project_id', '=', self.id)], limit=1, order='end_time desc')
        start_time = parse(last_lesson.end_time) if last_lesson is not None else parse(self.date_start)

        self.handle_scheduling_rule(args, start_time=start_time)

    # Calcola la durata di una lezione in minuti
    @api.onchange('module4lesson', 'module_type_id')
    def compute_duration_lesson(self):
        for project in self:
            project.duration_module = project.module_type_id.time
            module_for_lesson = project.module4lesson
            project.duration_lessons = project.duration_module * module_for_lesson

    # Schedules lessons according to scheduling rules
    def handle_scheduling_rule(self, args, start_time=None, skip_conflicts=False):
        env = self.env
        task_model = env['project.task']
        current_date = start_time if start_time is not None else parse(self.date_start)

        # self.clear_future_lessons(date_from)
        module_size         = self.module_type_id.time
        total_modules       = self.number_of_module
        already_scheduled   = self.get_scheduled_minutes()
        remaining_minutes   = (total_modules * module_size) - already_scheduled

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
            end_ts = schedule_date + timedelta(minutes=minutes_to_schedule)

            # creo l'elemento potenzialmente schedulabile
            lesson = {
                "name": self.name,
                "professor_id": int(schedule_obj.professor_id.id),
                "project_id": int(self.id),
                "start_time": schedule_date.strftime('%Y-%m-%d %H:%M:%S.000000%z'),
                "end_time": end_ts.strftime('%Y-%m-%d %H:%M:%S.000000%z'),
            }
            current_date = end_ts + timedelta(minutes=1)

            logger.info('Inizio %s - Fine %s', lesson['start_time'], lesson['end_time'])
            overlapped_lessons = task_model.get_overlapped_lessons(lesson['professor_id'], lesson['start_time'],
                                                                   lesson['end_time'])
            if not len(overlapped_lessons) > 0:
                task_model.create(lesson)
                remaining_minutes -= minutes_to_schedule
            elif skip_conflicts:
                logger.info('skipping conflict lesson %s', lesson['start_time'])
            else:
                raise ValidationError(
                    'impossibile allocare il docente ' + schedule_obj.professor_id.name +
                    ' alla lezione del' + lesson['start_time'] + ' perché gia impegnato in un\' altra attività')

        return "scheduling completato"

    @api.multi
    def get_time_lessons(self, time_lesson):
        hh = int(time_lesson)
        mm = time_lesson - hh
        mms = str(int(round(mm * 60)))
        if (len(mms) == 1):
            mms = '0' + mms
        data = str(hh) + ":" + mms
        return data

    @api.multi
    def open_wizard_material_delivered(self):
        view_ref = self.env['ir.model.data'].get_object_reference(
            'inlingua', 'delivered_material_view_wizard')
        view_id = view_ref[1] if view_ref else False
        return {
            'name': 'Delivered Material',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(False, 'form'), (False, 'form')],
            'res_model': 'material.delivered.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_course_id': self.id },
            'nodestroy': False,
            'flags': {
                'action_buttons': False,
                'sidebar': False,
            },
        }

class StudentLevel(models.Model):
    _name = 'student.level'
    _order = 'name'

    name = fields.Char(string='Level')
