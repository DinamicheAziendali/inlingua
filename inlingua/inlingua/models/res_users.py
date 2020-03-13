# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).


from odoo import fields, models


class UsersInherit(models.Model):
    _inherit = 'res.users'

    # student = fields.Boolean(string='Student')
    professor = fields.Boolean(string='Professor',
                               related='partner_id.professor')
