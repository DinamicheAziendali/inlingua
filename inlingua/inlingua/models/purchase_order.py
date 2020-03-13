# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
from odoo import fields, models, api
from datetime import datetime, date


class PurchaseOrderInh(models.Model):
    _inherit = "purchase.order"

    # notice_day = fields.Char(string='Day Notice')

    type_order = fields.Selection([ ('model0', 'Ordine a Terzista'),
                                    ('model1', 'Conferimento di incarico'),
                                    ('model2', 'Contratto di Collaborazione Professionale')])
    
    # Termini di fatturazione
    invoicing_terms                 = fields.Text(string='Termini di fatturazione')
    
    # Ordine di vendita di riferimento    
    sale_order_id                   = fields.Many2one('sale.order', string='Sales Order')

    # Totale dell'ordine (imponibile)
    sale_order_amount_untaxed       = fields.Monetary(
                                        related='sale_order_id.amount_untaxed',
                                        string='Order amount')

    # Totale importo già assegnato a terzisti per il sale order di riferimento.
    sale_order_residual_assigned    = fields.Monetary(
                                        related='sale_order_id.assigned_purchase_amount',
                                        string='Assigned to contractors')

    # Totale importo restante assegnabile a terzisti.
    sale_order_residual_to_assign   = fields.Monetary(related='sale_order_id.residual_to_assign', string='Amount to assign')
    
    note_attachment                 = fields.Text(string='Note e/o allegati')
    reference_contact               = fields.Text(string='Referenti')


    # @api.onchange('is_contractor_order')
    # def onchange_is_contractor_order(self):
    #     res={}
    #     if self.is_contractor_order:
    #         res['domain'] = {'partner_id': ['&',('supplier', '=', True) ,('contractor', '=', True)]}
    #     else:
    #         res['domain'] = {'partner_id': [('supplier', '=', True)]}
    #     return res

    @api.onchange('type_order')
    def onchange_type_order(self):
        res={}
        if self.type_order == 'model0':
            # è un ordine a terzista.
            res['domain'] = {'partner_id': ['&',('supplier', '=', True) ,('contractor', '=', True)]}
        else:
            res['domain'] = {'partner_id': [('supplier', '=', True)]}
        return res

    # al cambio dell'ordine di vendita a cui fa riferimento, carico il dettaglio
    # nell'ordine di acquisto.
    @api.onchange('sale_order_id')
    def onchange_sale_order_lines(self):
    #    import pdb; pdb.set_trace()

        id_order = False
        if self._origin.id:
            id_order =  self._origin.id
        if not id_order and self.id:
            id_order = self.id
            
        # ciclo sugli ordini di vendita per creare le righe dell'ordine di acquisto
        vals = []
        for so_line in self.sale_order_id.order_line:
        
            vals.append((0,0, {
                'order_id': id_order,
                'name': so_line.name,
                'product_id': so_line.product_id.id,
                'product_qty': so_line.product_uom_qty,
                'price_unit': so_line.price_unit,
                'product_uom': so_line.product_uom.id,
                'date_planned': fields.Datetime.to_string(datetime.today()),
            }))

        #if self.sale_order_id.order_line:
        self.update({'order_line' : vals})


class PurchaseOrders(models.Model):
    _inherit = "purchase.order.line"
    date_end = fields.Date(string='Date End')
