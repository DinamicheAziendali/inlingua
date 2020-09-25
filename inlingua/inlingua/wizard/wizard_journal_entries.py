# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models, api
from datetime import datetime


class JournalEntriesWizard(models.TransientModel):
    _name = "journal.entries.wizard"

    def get_date_today(self):
        today = datetime.now().date()
        return today

    journal_ids = fields.Many2many('account.journal', string='Journal')
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(
        string='Date To', required=True, default=get_date_today)

    def _get_account_move_line(self):
        model_am = self.env['account.move']
        journal_name = ''
        date_from = datetime.strptime(self.date_from, "%Y-%m-%d").strftime('%d/%m/%y')
        date_to = datetime.strptime(self.date_to, "%Y-%m-%d").strftime('%d/%m/%y')
        if self.journal_ids:
            for journal in self.journal_ids:
                am = model_am.search([
                    ('journal_id', '=', journal.id),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to)
                ], order='date')
                model_am |= am
            for journal in self.journal_ids:
                if journal_name:
                    journal_name += ', ' + journal.display_name
                else:
                    journal_name = journal.display_name

        else:
            am = model_am.search([
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
            ], order='date')
            model_am |= am
        data = {
            'journal': journal_name,
            'date_from': date_from,
            'date_to': date_to,
            'account_move': model_am.ids
        }
        return data

    @api.multi
    def print_journal_entries(self):
        list_am = self._get_account_move_line()
        report_name = 'inlingua.template_journal_entries_view'
        return self.env['report'].get_action(self, report_name, list_am)


class ReportJournalEntries(models.AbstractModel):
    _name = 'report.inlingua.template_journal_entries_view'

    @api.multi
    def render_html(self, docids, data):
        account_move = self.env['account.move'].browse(data['account_move'])
        docargs = {
            'journal': data['journal'],
            'date_from': data['date_from'],
            'date_to': data['date_to'],
            'account_move': account_move,
        }
        if 'context' in docargs.keys():
            del docargs['context']
        return self.env['report'].render(
            'inlingua.template_journal_entries_view', values=docargs)
