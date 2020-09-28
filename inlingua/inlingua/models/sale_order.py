# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).


from odoo import fields, models, api
from datetime import datetime, date


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    # Un SO può avere più contratti associati
    contract_ids = fields.One2many('private.contract', 'order_id',
                                   string='Contracts')

    # Un SO può avere più PO associati
    purchase_order_ids = fields.One2many('purchase.order', 'sale_order_id',
                            string='Purchase Orders')

    # Accordo quadro di riferimento
    general_agreement_id = fields.Many2one('sale.order',
                                           string='Framework Agreement')
    
    # è un accordo quadro?
    framework_agreement = fields.Boolean('Is Framework Agreement')

    # Importo residuo dell'accordo quadro di cui emettere ordine di vendita
    residual_framework_agreement = fields.Monetary(
        related='general_agreement_id.amount_total',
        string='Residual Framework Agreement')

    original_total = fields.Float(compute='compute_original_total',
                                  string='Original Total')
    pa_cig = fields.Char(required=False, string='CIG')

    # Tipo di servizio richiesto
    service_type = fields.Selection(
           [('custom',  'Personalizzato'),
            ('agreed',  'Come concordato'),
            ('startAt', 'Data inizio')],
           'Servizio richiesto')

    # Solo se service_type = startAt
    service_date = fields.Date('Data inizio servizio')

    # Solo se service_type = agreed
    service_agreed = fields.Boolean('Come concordato')

    # Solo se service_type = custom
    service_custom = fields.Text('Descrizione servizio')

    # Data e numero ordine del cliente
    customer_order_number = fields.Char(required=False, string='Numero ordine cliente')
    customer_order_date = fields.Date(string='Data ordine cliente')

    # Totale importo assegnato a terzisti tramite ordine di acquisto
    assigned_purchase_amount    = fields.Monetary(compute='compute_assigned_purchase_total', string='Assigned Amount')
    residual_to_assign          = fields.Monetary(compute='compute_sale_order_to_assign', string='Amount to assign')

    # Totale residuo ordine
    amount_residual = fields.Monetary(
        string='Saldo Ordine',
        readonly=True,
        compute='_amount_residual',
        track_visibility='always'
    )

    @api.depends('amount_total')
    def _amount_residual(self):
        for order in self:
            if order.framework_agreement:
                order.amount_residual = order.amount_total
            else:
                amount_residual = order.amount_total
                for invoice in order.invoice_ids:
                    if invoice.state == 'open' or invoice.state == 'paid':
                        if invoice.type == 'out_invoice':
                            amount_residual -= invoice.amount_total
                        else:
                            amount_residual += invoice.amount_total
                if amount_residual < 0:
                    order.amount_residual = 0
                else:
                    order.amount_residual = amount_residual

    # Totale ordini di acquisto ancora da assegnare a terzisti
    @api.depends('amount_untaxed', 'purchase_order_ids')
    def compute_sale_order_to_assign(self):
        model_purchase = self.env['purchase.order']
        # import pdb; pdb.set_trace()
        for order in self:
            total = 0
            purchase_ids = model_purchase.search([('sale_order_id', '=', order.id)])
            for purchase in purchase_ids:
                total += purchase.amount_untaxed

            order.residual_to_assign = order.amount_untaxed - total


    # Totale ordini di acquisto assegnati a terzisti
    @api.depends('purchase_order_ids')
    def compute_assigned_purchase_total(self):
        model_purchase = self.env['purchase.order']
        for order in self:
            total = 0
            purchase_ids = model_purchase.search([('sale_order_id', '=', order.id)])
            for purchase in purchase_ids:
                total += purchase.amount_untaxed
            order.assigned_purchase_amount = total


    def compute_original_total(self):
        total = 0
        for order in self:
            for line in order.order_line:
                if line.price_total > 0:
                    total += line.price_total
            order.original_total = total
            total = 0

    # @api.onchange('amount_total', 'general_agreement_id')
    # def auto_decreases_general_agreement(self):
    #     self.decreases_general_agreement()


    # RIDEFINIZIONE DEL CAMPO VISUALIZZATO NELLA LISTBOX ORDINI
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            # name = "[%s] %s" % (record.name, record.date_order)
            name = '[{}] {:.10}'.format(record.name, record.date_order)
            result.append((record.id, name))
        return result

    @api.multi
    def decreases_general_agreement(self):
        model_sale_order_line = self.env['sale.order.line']
        for order in self:
            if order.general_agreement_id:
                generale_agr_id = order.general_agreement_id
                line = model_sale_order_line.search(
                    [('order_id', '=', generale_agr_id.id),
                     ('name', 'ilike', order.name)], limit=1)
                if line:
                    line.write({'price_unit': - order.amount_total})
                if not line:
                    model_product = self.env['product.product']
                    product = model_product.search([('type', '=', 'service'),
                                                    ('name', 'ilike',
                                                     'formazione')], limit=1)
                    if not product:
                        product = model_product.create({'name': 'formazione',
                                                        'type': 'service'})
                    if len(generale_agr_id.order_line) > 0:
                        taxes = generale_agr_id.order_line[0].tax_id
                    else:
                        taxes = False
                    name_line_order = order.name
                    if order.confirmation_date:
                        date_order = order.confirmation_date
                        new_date_order = datetime.strptime(date_order,
                                                           "%Y-%m-%d %H:%M:%S").date()
                        name_line_order += ' del ' + new_date_order.strftime('%d-%m-%y')
                    model_sale_order_line.create(
                        {'order_id': generale_agr_id.id,
                         'name': name_line_order,
                         'product_id': product.id,
                         'product_uom_qty': 1,
                         'price_unit': - order.amount_total,
                         'tax_id': [
                             (6, 0, [tax.id for tax in
                                     taxes])],
                         })
            else:
                return
