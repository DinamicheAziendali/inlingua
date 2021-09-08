# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models
from datetime import datetime


class ProjectStudent(models.Model):
    _name = 'project.student'
    _description = "Student on Class"
    _rec_name = 'student_id'

    # @api.model
    # def _get_date_from(self):
    #     project = self.project_id
    #     if project.date_start:
    #         return project.date_start

    project_id = fields.Many2one('project.project')
    student_id = fields.Many2one('res.partner',
                                 domain=[('student', '=', True)],
                                 string='Student', required=True)
    # date_from = fields.Date(default=_get_date_from, string="From")\
    date_from = fields.Date(string="From")
    # date_to = fields.Date(string="To")
    date_to = fields.Date(string="To")
    total_lesson_in = fields.Integer('Lesson Present')
    total_lesson_out = fields.Integer('Lesson Absent')
    level_achieve = fields.Many2one('student.level', string='Level Achieve')
    active = fields.Boolean('Active', default=True)


    # Calcolo lezioni di presenza
    # @api.depends('minutes_scheduled')
    # @api.onchange('duration_lessons')
    def get_presenze(self):
        # Le presenze sono date dal numero di task del corso dove l'allievo è presente.
        # import pdb; pdb.set_trace()
        self.modules_scheduled = 0
        if self.duration_lessons > 0:
            self.modules_scheduled = self.minutes_scheduled / self.duration_lessons

    def get_lessons_held(self):
        for project_student in self:
            lessons_held = 0
            today = fields.Date.today()
            model_lesson = self.env['project.task']
            total_lessons = model_lesson.search([
                ('project_id', '=', project_student.project_id.id),
                ('date_deadline', '>=', project_student.project_id.date_start),
                ('date_deadline', '<=', today),
            ])
            for lesson in total_lessons:
                for students in lesson.task_student_ids:
                    if students.student_id.id == project_student.student_id.id:
                        if students.present:
                            lessons_held += 1
            return lessons_held

    def get_list_lessons_progress_report(self):
        for project_student in self:
            list_lessons = []
            today = fields.Date.today()
            model_lesson = self.env['project.task']
            total_lessons = model_lesson.search([
                ('project_id', '=', project_student.project_id.id),
                ('date_deadline', '>=', project_student.project_id.date_start),
                ('date_deadline', '<=', today),
            ])
            for lesson in total_lessons:
                data_lesson = []
                for students in lesson.task_student_ids:
                    if students.student_id.id == project_student.student_id.id:
                        data_lesson = [
                            datetime.strptime(students.date, '%Y-%m-%d').strftime("%d/%m/%Y"),
                            students.start_hour,
                            students.end_hour,
                            students.task_id.name,
                            students.professor_id.name,
                            students.note,
                            students.present,
                        ]
                if data_lesson:
                    list_lessons.append(data_lesson)
            return list_lessons
