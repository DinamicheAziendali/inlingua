# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime


class ProjectTaskStudent(models.Model):
    # Record del singolo allievo nella singola lezione.
    _name = 'project.task.student'
    _description = "Student on Lesson"
    _rec_name = 'task_id'

    def _check_login(self):
        for lesson in self:
            user = self.env.user
            if user.has_group('inlingua.group_professor'):
                lesson.check_login = True
            else:
                lesson.check_login = False

    check_login = fields.Boolean(compute='_check_login', default=False)
    task_id = fields.Many2one('project.task')
    student_id = fields.Many2one('res.partner',
                                 domain=[('student', '=', True)],
                                 # solo quelli nel progetto
                                 string='Student', required=True)
    present = fields.Boolean('Present', default=True)
    project_id = fields.Many2one(related='task_id.project_id')
    professor_id = fields.Many2one(related='task_id.professor_id')
    date = fields.Date(related='task_id.date_deadline')
    start_hour = fields.Char(related='task_id.start_hour')
    end_hour = fields.Char(related='task_id.end_hour')
    language_id = fields.Many2one(related='task_id.project_id.language_id')
    note = fields.Text(string='Note')
    grade = fields.Char(string='Grade')
    project_date_start = fields.Date(related='task_id.project_id.date_start')
    project_date_end = fields.Date(related='task_id.project_id.date_end')
    project_start_level = fields.Many2one(related='task_id.project_id.start_level')
    project_duration_lessons = fields.Integer(related='task_id.project_id.duration_lessons')
    project_programm_id = fields.Many2one(related='task_id.project_id.programm_id')
    project_number_of_module = fields.Integer(related='task_id.project_id.number_of_module')
    project_module4lesson = fields.Integer(related='task_id.project_id.module4lesson')
    project_book_lessons = fields.Integer(compute='get_project_book_lessons')
    project_office_id = fields.Many2one(related='task_id.project_id.office_id')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    active = fields.Boolean('Active', default=True)

    @api.depends('project_number_of_module', 'project_module4lesson')
    def get_project_book_lessons(self):
        for student in self:
            if student.project_number_of_module and student.project_module4lesson:
                if student.project_module4lesson != 0:
                    student.project_book_lessons = \
                        student.project_number_of_module / student.project_module4lesson
                else:
                    raise UserError(
                        "Controllare 'Default Moduli per Lezione' uguale a 0 del progetto %s"
                        % student.project_id.name
                    )

    def get_list_lessons_progress_report(self):
        for student in self:
            list_lessons = []
            for lesson in student.project_id.task_ids:
                data_lesson = []
                for students in lesson.task_student_ids:
                    if students.student_id.id == student.student_id.id:
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

