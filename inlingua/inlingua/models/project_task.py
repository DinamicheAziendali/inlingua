# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from dateutil.parser import parse

from odoo import fields, models, api
# from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError


class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'
    _description = 'Lesson'
    
    professor_id = fields.Many2one('res.partner', string='Professor',
                                   required=True,
                                   domain=[('professor', '=', True)])
    professor_user = fields.Many2one(compute='get_professor_user', store=True)
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)

    task_student_ids = fields.One2many('project.task.student', 'task_id')
    language_course_id = fields.Many2one('class.language',
                                         related='project_id.language_id',
                                         string='Course Language', store=True)
    course_type_id = fields.Many2one('class.type',
                                     related='project_id.course_type_id',
                                     string='Course Type')

    test = fields.Boolean(string='Test')
    notes = fields.Char(string='Note')

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
                    WHERE project_id = " + str(project_id) + "                                      \
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
            ' WHERE professor_id = %d' \
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
