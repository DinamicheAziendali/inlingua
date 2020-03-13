# -*- coding: utf-8 -*-
# Copyright (C) 2019-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime

class PrintContractWizard(models.TransientModel):
    _name       = "print.contract.wizard"

    date_from     = fields.Date(string='Date From')
    date_to       = fields.Date(string='Date To')
    print_to_cash = fields.Boolean(string='Print to cash?')
    # print_all   = fields.Boolean(string='Print All?')

    @api.multi
    def button_export_pdf(self):
        self.ensure_one()
        return self._export()

    def _prepare_data(self):
        self.ensure_one()
        model_contract  = self.env['private.contract']
        date_from       = self.date_from
        date_to         = self.date_to

        domain = [('type_contract', '=', 'private')]
        if self.print_to_cash: domain.append(('to_cash', '>', 0))
        if self.date_from: domain.append(('date_contract', '>=', date_from))
        if self.date_to: domain.append(('date_contract', '<=', date_to))

        '''
        if self.print_to_cash:
            # Stampa i contratti privati da incassare
            domain = [('date_contract', '>=', date_from),
                      ('date_contract', '<=', date_to),
                      ('type_contract', '=', 'private'),
                      ('to_cash', '>', 0)]
        else:
            # Stampa da incassare ed incassati
            domain = [('date_contract', '>=', date_from),
                      ('date_contract', '<=', date_to),
                      ('type_contract', '=', 'private')]
        '''

        # Invio dati al report
        contracts   = model_contract.search(domain)
        data        = { 'contracts':    contracts.ids,
                        'date_from':    date_from,
                        'date_to'  :    date_to,
                        'print_to_cash':self.print_to_cash
                        }
        
        return data

    def _export(self):
        """
        Export to PDF.
        data (contracts) è iniettato via context al report
        """
        data = self._prepare_data()
        return self.env['report'].with_context().get_action(
            self, 'inlingua.report_contract_receipt_view', data)
