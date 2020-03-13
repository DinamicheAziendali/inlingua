# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).


from odoo import fields, models, api


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    private_contract_id = fields.Many2one('private.contract', string='Contract')
    is_company = fields.Boolean(related='partner_id.is_company')

    def unlink(self):
        # res = super(AccountInvoiceInherit, self).unlink()
        model_payment_term_line = self.env['payment.term.line']
        for invoice in self:
            lines = model_payment_term_line.search([('invoice_id', '=', invoice.id)])
            for line in lines:
                line.write({'invoice_id': False,
                            'invoiced': False})
        return super(AccountInvoiceInherit, self).unlink()
