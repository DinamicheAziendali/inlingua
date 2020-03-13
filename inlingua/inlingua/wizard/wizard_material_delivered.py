# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models, api
from datetime import datetime


class AddRateWizard(models.TransientModel):
    _name = "material.delivered.wizard"
    _rec_name = 'material_delivered'


    company_private = fields.Char(string='Company/Private:')
    material_delivered = fields.Char(string='Material Delivered')
    course_id = fields.Many2one('project.project', string='Course')

    @api.multi
    def print_model_material_delivered(self):
        return self.env['report'].get_action(self,
                                             'inlingua.report_view_material_delivered')
        # return {'type': 'ir.actions.report.xml',
        #         'report_name': 'inlingua.report_receipt_view'}
