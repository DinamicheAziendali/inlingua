# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


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