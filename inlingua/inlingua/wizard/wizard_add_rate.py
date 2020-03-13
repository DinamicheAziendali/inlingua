# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime


class AddRateWizard(models.TransientModel):
    _name = "add.rate.wizard"

    def _get_default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    def get_date_today(self):
        today = datetime.now().date()
        return today

    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=_get_default_currency_id,
                                  track_visibility='always', required=True)
    rate_amount = fields.Monetary(string='Rate Amount',
                                  currency_field='currency_id', required=True)
    date        = fields.Date(string='Date', required=True, default=get_date_today)
    journal_id  = fields.Many2one('account.journal', required=True,
                                 string='Payment',
                                 domain=[('type', 'in', ('bank', 'cash'))])
    contract_id = fields.Many2one('private.contract')

    # flag 'da contabilizzare'
    to_account = fields.Boolean(string='To Account')

    # Registra un incasso di un contratto privato
    @api.multi
    def add_rate(self):
        if self.rate_amount > 0:
            self.contract_id.payment_line_ids.create(
                {'contract_id': self.contract_id.id,
                 
                 #'rate_amount': -self.rate_amount, # sostituito a seguito della rimozione della generazione rate 19/09/2019
                 'rate_amount': self.rate_amount,
                 'journal_id': self.journal_id.id,
                 'to_account': self.to_account,
                 'date': self.date})
        else:
            raise ValidationError('Amount must be greater of 0')

            # def print_and_add_rate(self):
            #     self.add_rate()
            #     self.date_now = datetime.now()
            # self.ensure_one()
            # projectModel = self.env['add.rate.wizard']
            # datas = {
            #     'model': projectModel._name,
            #     'form': projectModel.read(),
            #     'context': self._context
            # }
            # return {
            #     'type': 'ir.actions.report.xml',
            #     'report_name': 'inlingua.report_receipt_view',
            #     'datas': datas
            # }

    @api.multi
    def print_and_add_rate(self):
        self.add_rate()
        return self.env['report'].get_action(self,
                                             'inlingua.report_receipt_view')
        # return {'type': 'ir.actions.report.xml',
        #         'report_name': 'inlingua.report_receipt_view'}
