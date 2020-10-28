# coding=utf-8
import logging

from odoo import models, fields

_logger = logging.getLogger('lesson_scheduler')

class SchedulingRule(models.Model):
    _name       = 'project.task_scheduling_rule'
    _description = 'Weekly scheduling rule'
    _order = 'weekday asc, start_time asc'

    professor_id = fields.Many2one(
        string='Professor', comodel_name='res.partner',
        required=True, domain=[('professor', '=', True)]
    )

    weekday     = fields.Selection(
        [
            (1, "Lunedì"), (2, "Martedì"), (3, "Mercoledì"),
            (4, "Giovedì"), (5, "Venerdì"), (6, "Sabato"), (7, "Domenica")
        ],
        string="Giorno",
        required=True
    )

    start_time  = fields.Float(required=True)  # fields.Text(string='hh:mm', required="true")
    modules     = fields.Integer(string='Modules', required=True)
    project_id  = fields.Many2one(comodel_name='project.project')
