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
    # _rec_name = 'partner_id'

    task_id = fields.Many2one('project.task')
    student_id = fields.Many2one('res.partner',
                                 domain=[('student', '=', True)],
                                 # solo quelli nel progetto
                                 string='Student', required=True)
    present = fields.Boolean('Present', default=True)
    project_id = fields.Many2one(related='task_id.project_id')
    note = fields.Text(string='Note')
    grade = fields.Char(string='Grade')
    active = fields.Boolean('Active', default=True)
