# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from dateutil.parser import parse

from odoo import fields, models, api
# from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError
from datetime import datetime
import pytz
import calendar
import locale
locale.setlocale(locale.LC_ALL, 'it_IT.utf-8')


class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'
    _description = 'Lesson'
    _order = 'project_id, start_time'

    def _check_login(self):
        for lesson in self:
            user = self.env.user
            if user.has_group('inlingua.group_professor'):
                lesson.check_login = True
            else:
                lesson.check_login = False

    def _set_name_like_course(self):
        model_project = self.env['project.project']
        project_id = model_project.browse(
            self.env.context.get('default_project_id'))
        if project_id:
            return project_id.name
        else:
            return False

    name = fields.Char(default=_set_name_like_course)
    check_login = fields.Boolean(compute='_check_login', default=False)
    professor_id = fields.Many2one(
        'res.partner', string='Professor',
        required=True, domain=[('professor', '=', True)],
        default=lambda self: self.env.user.partner_id if self.env.user.partner_id.professor else False)
    professor_user = fields.Many2one(compute='get_professor_user', store=True)
    start_time = fields.Datetime(string='Start Time', required=True, copy=False)
    end_time = fields.Datetime(string='End Time', required=True, copy=False)
    start_hour = fields.Char(string='Ora inizio', store=True,
                             compute='_get_start_hour_lesson')
    end_hour = fields.Char(string='Ora fine', store=True,
                           compute='_get_end_hour_lesson')
    weekday = fields.Char(string="Giorno", store=True,
                          compute='_get_weekday_lesson')

    task_student_ids = fields.One2many('project.task.student', 'task_id')
    language_course_id = fields.Many2one('class.language',
                                         related='project_id.language_id',
                                         string='Course Language', store=True)
    course_type_id = fields.Many2one('class.type',
                                     related='project_id.course_type_id',
                                     string='Course Type')

    test = fields.Boolean(string='Test')
    notes = fields.Char(string='Note')
    date_deadline = fields.Date(string='Deadline', compute='_get_date_lesson')
    project_description = fields.Char(
        related='project_id.description', store=True)
    project_contract = fields.Char(compute='_get_project_contract', store=True)

    @api.depends('project_id')
    def _get_project_contract(self):
        for lesson in self:
            if lesson.project_id:
                for contract in lesson.project_id.contract_ids:
                    if lesson.project_contract:
                        lesson.project_contract += \
                            ', ' + contract.number_contract
                    else:
                        lesson.project_contract = contract.number_contract

    @api.depends('start_time', 'project_id')
    def _get_start_hour_lesson(self):
        for lesson in self:
            local_tz = pytz.timezone('Europe/Paris')
            utc_tz = pytz.timezone('UTC')
            if lesson.start_time:
                start_time = parse(lesson.start_time)
                start_time = start_time.replace(tzinfo=utc_tz)
                lesson.start_hour = '%s:%s:%s' % (
                    start_time.astimezone(local_tz).hour,
                    start_time.strftime("%M"),
                    start_time.strftime("%S"))

    @api.depends('end_time')
    def _get_end_hour_lesson(self):
        for lesson in self:
            local_tz = pytz.timezone('Europe/Paris')
            utc_tz = pytz.timezone('UTC')
            if lesson.end_time:
                end_time = parse(lesson.end_time)
                end_time = end_time.replace(tzinfo=utc_tz)
                lesson.end_hour = '%s:%s:%s' % (
                    end_time.astimezone(local_tz).hour,
                    end_time.strftime("%M"),
                    end_time.strftime("%S"))

    def day_name_from_weekday(self, weekday):
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
        days = list(calendar.day_name)
        return days[weekday]

    @api.depends('date_deadline')
    def _get_weekday_lesson(self):
        for lesson in self:
            if lesson.date_deadline:
                date_deadline = parse(lesson.date_deadline)
                weekday = date_deadline.weekday()
                lesson.weekday = lesson.day_name_from_weekday(weekday)

    @api.depends('start_time', 'end_time')
    def _get_date_lesson(self):
        for lesson in self:
            local_tz = pytz.timezone('Europe/Paris')
            utc_tz = pytz.timezone('UTC')
            if lesson.start_time:
                start_time = parse(lesson.start_time)
                start_time = start_time.replace(tzinfo=utc_tz)
                lesson.date_deadline = start_time.astimezone(local_tz)
            if lesson.end_time and not lesson.date_deadline:
                end_time = parse(lesson.end_time)
                end_time = end_time.replace(tzinfo=utc_tz)
                lesson.date_deadline = end_time.astimezone(local_tz)

    @api.onchange('project_id')
    def get_task_student_ids(self):
        for task in self:
            list_student = []
            task_id = False
            model_task_student = self.env['project.task.student']
            if task.project_id and task.project_id.project_student_ids:
                for student in task.project_id.project_student_ids:
                    list_student.append(student.student_id.id)
            for student in list_student:
                if self._origin.id:
                    task_id = self._origin.id
                if not task and task.id:
                    task_id = task.id
                model_task_student.create({
                    'task_id': task_id,
                    'student_id': student
                })

    @api.model
    def create(self, vals):
        res = super(ProjectTaskInherit, self).create(vals)
        for task in res:
            list_student = []
            model_task_student = self.env['project.task.student']
            if task.project_id and task.project_id.project_student_ids:
                for student in task.project_id.project_student_ids:
                    list_student.append(student.student_id.id)
            for student in list_student:
                model_task_student.create({
                    'task_id': task.id,
                    'student_id': student
                })
        return res

    @api.onchange('start_time')
    def get_date_deadline(self):
        for task in self:
            if task.start_time:
                task.date_deadline = task.start_time

    @api.depends('professor_id')
    def get_professor_user(self):
        for task in self:
            if task.professor_id:
                user = self.env['res.users'].search([('partner_id', '=', task.professor_id.id)], limit=1)
                if user:
                    task.professor_user = user.id

    # Calcola il tempo totale delle lezioni schedulate escludendone una.
    def get_scheduled_total_time(self, project_id, lesson_to_ignore):
        query = "                                                                                   \
                    SELECT SUM(extract(epoch from (end_time - start_time)) :: integer / 60) m_sum   \
                    FROM project_task                                                               \
                    WHERE active = True" \
                "         AND project_id = " + str(project_id) + "                                      \
                          AND    id != " + str(lesson_to_ignore) + "                                \
                "
        print query
        cr = self.env.cr
        cr.execute(query)
        return cr.dictfetchall()[0]['m_sum']

    # Ritorna la lista delle lezioni overlapped
    def get_overlapped_lessons(self, professor_id, start_time, end_time, lesson_to_ignore=None):
        cr = self.env.cr
        q = 'SELECT t.name, t.start_time, t.end_time' \
            ' FROM  project_task t ' \
            ' WHERE t.active = True' \
            '   AND t.professor_id = %d' \
            '   AND tsrange(t.start_time, t.end_time, \'[]\') && tsrange(\'%s\', \'%s\', \'[]\')'
        if lesson_to_ignore is not None:
            q += 'AND id <> %d '
            q = q % (professor_id, start_time, end_time, lesson_to_ignore)
        else:
            q = q % (professor_id, start_time, end_time)
        cr.execute(q)
        result = cr.fetchall()
        return result

    # Constraint che controlla la fruibilità della lezione in base
    # alle lezioni gia schedulate
    @api.constrains('start_time', 'end_time')
    def course_time_up(self):
        for lesson in self:
            if lesson.project_id:
                course_minutes = int(lesson.project_id.number_of_module) * int(lesson.project_id.module_type_id.time)
                lesson_minutes = (parse(lesson.end_time) - parse(lesson.start_time)).seconds / 60
                scheduled_total = self.get_scheduled_total_time(lesson.project_id.id, lesson.id) or 0

                if scheduled_total + lesson_minutes > course_minutes:
                    raise ValidationError("Questa lezione supera il limite di tempo erogabile dal corso")

    # Constraint che non ci siano circostanze di overbooking
    # alle lezioni gia schedulate
    @api.constrains('professor_id', 'start_time', 'end_time')
    def course_overlapping(self):
        for lesson in self:
            if lesson.professor_id and lesson.start_time and lesson.end_time:
                overlapped = self.get_overlapped_lessons(lesson.professor_id, lesson.start_time, lesson.end_time,
                                                         lesson.id)
                if len(overlapped) > 0:
                    activities_list_text = ""
                    for o in overlapped:
                        activities_list_text += "\t– " + str(o[0]) + "\t[ " + str(o[1]) + " - " + str(o[2]) + "]\n"
                    message = str(self.professor_id.name) + " è gia impegnato/a nelle seguenti attività:\n" + \
                              activities_list_text + "durante il periodo: [" + str(lesson.start_time) + " - " + str(
                        lesson.end_time) + "]"

                    raise ValidationError(message)
