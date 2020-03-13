# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT
from odoo import api, fields, models
from collections import OrderedDict

class ContractReceiptReport(models.AbstractModel):
    """Model of Customer Activity Statement"""

    _name = 'report.inlingua.report_contract_receipt_view'

    @api.multi
    def render_html(self, docids, data):
        model_contract = self.env['private.contract']
        if 'context' in data.keys():
            del data['context']
        new_data = []
        if 'contracts' in data.keys():
            for contr in data['contracts']:
                new_data.append(model_contract.browse(contr))
        # new_data = datetime.strptime(data['date_from'], '%d/%m/%Y')

        docargs = {
            'contracts': new_data,
            'date_from': datetime.strptime(data['date_from'], '%Y-%m-%d').date(),
            'date_to': datetime.strptime(data['date_to'], '%Y-%m-%d').date()
        }

        # report_contract_receipt_view è in view/contract_receipt_template.xml
        # values=docargs
        return self.env['report'].render(
            'inlingua.report_contract_receipt_view', docargs)