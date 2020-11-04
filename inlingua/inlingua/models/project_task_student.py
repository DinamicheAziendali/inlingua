# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import fields, models


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
    active = fields.Boolean('Active', default=True)
