from odoo import models, fields, api


class TimetableView(models.Model):
    _inherit = 'ir.ui.view'
    type = fields.Selection(
        selection_add=[('timetable', 'TimeTable')]
    )


class TimetableActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'
    view_mode = fields.Selection(
        selection_add=[('timetable', 'TimeTable')]
    )
