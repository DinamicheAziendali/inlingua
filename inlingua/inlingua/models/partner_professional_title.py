# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).


from odoo import fields, models, api


class PartnerAcademicTitle(models.Model):
    _name = 'partner.professional.title'

    name = fields.Char(required=True, string='Professional Title')