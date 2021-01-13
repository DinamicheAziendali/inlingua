# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models, _


class UpdateSospesaWizard(models.TransientModel):
    _name = "update.sospesa.wizard"
    _description = "Update Sospesa Wizard"

    @api.model
    def _count(self):
        return len(self._context.get('active_ids', []))

    count = fields.Integer(default=_count, string='Conteggio lezione')

    @api.multi
    def update_sospesa(self):
        lessons = self.env['project.task'].browse(self._context.get('active_ids', []))
        for lesson in lessons:
            lesson.active = False
