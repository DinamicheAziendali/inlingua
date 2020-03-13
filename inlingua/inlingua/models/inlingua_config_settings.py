# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class InlinguaSettings(models.TransientModel):
    _name = 'inlingua.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.user.company_id, required=True)

    contract_account_income = \
        fields.Many2one('account.account', company_dependent=True,
                        string="Conto vendite contratti",
                        domain=[('deprecated', '=', False)],
                        help="Conto contabile economico "
                             "per fatture da contratti.")

    contract_invoice_journal = \
        fields.Many2one('account.journal',
                        string="Registro fatture contratti",
                        company_dependent=True, )

    contract_tax = \
        fields.Many2one('account.tax',
                        string="Iva default per fatture da contratti",
                        help="Iva che si applica nell'automatismi di "
                             "generazione nuove fatture da contratto.",)

    @api.multi
    def set_contract_account_income_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'inlingua.config.settings', 'contract_account_income',
            self.contract_account_income.id)

    @api.multi
    def set_contract_invoice_journal_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'inlingua.config.settings', 'contract_invoice_journal',
            self.contract_invoice_journal.id)

    @api.multi
    def set_contract_tax_defaults(self):
        return self.env['ir.values'].sudo().set_default(
                'inlingua.config.settings', 'contract_tax',
                self.contract_tax.id)
