# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields, api

# Modello degli incassi su contratti privati
class PaymentTermLine(models.Model):
    _name = 'payment.term.line'
    _order = "date,rate_amount desc"

    def _get_default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=_get_default_currency_id,
                                  track_visibility='always', required=True)
    
    # Id del contratto parent
    contract_id = fields.Many2one('private.contract',
                                  readonly=True, string='Contract')

    # Id del cliente
    partner_id  = fields.Many2one('res.partner',
                                 related='contract_id.partner_id',
                                 store=True,
                                 string='Customer')

    # number_contract = fields.Char(related='contract_id.number_contract',
    #                               readonly=True, store=True)

    # TODO: ma serve davvero?
    balance_value = fields.Monetary(string="Balance Value ",
                                    related='contract_id.balance_value',
                                    readonly=True)

    # Importo incassato
    rate_amount = fields.Monetary(string='Rate Amount',
                                  currency_field='currency_id')

    # Data dell'incasso
    date        = fields.Date(string='Date')

    journal_id  = fields.Many2one('account.journal', string='Payment',
                                 domain=[('type', 'in', ('bank', 'cash'))])

    # E' da fatturare?
    to_account  = fields.Boolean(string='To Account')

    # E' fatturato?
    invoiced    = fields.Boolean(string='Invoiced')
    
    invoice_id  = fields.Many2one('account.invoice', string='Invoice')
    
    move_id     = fields.Many2one('account.move', string='Move')

    @api.multi
    def set_to_account(self):
        for line in self:
            if line.to_account == True:
                line.to_account = False
            else:
                line.to_account = True

    # Stampa della ricevuta (ristampa)
    def f_print_receipt(self):
        return self.env['report'].get_action(self,
                                             'inlingua.view_receipt_private_contract')
        

class TypeDue(models.Model):
    _name = 'type.due'
    name = fields.Char(required=True)
