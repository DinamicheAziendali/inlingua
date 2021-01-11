# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models, _


class UpdateProfessorWizard(models.TransientModel):
    _name = "update.professor.wizard"
    _description = "Aggiorna Docente Wizard"

    @api.model
    def _count(self):
        return len(self._context.get('active_ids', []))

    count = fields.Integer(default=_count, string='Conteggio lezione')
    professor_id = fields.Many2one(
        'res.partner',
        string='Docente',
        required=True,
        domain=[('professor', '=', True)]
    )

    @api.multi
    def update_professor(self):
        lessons = self.env['project.task'].browse(self._context.get('active_ids', []))
        for lesson in lessons:
            lesson.professor_id = self.professor_id.id
