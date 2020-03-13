# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Marco Calcagni (mcalcagni@dinamicheaziendali.it)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields


class ModuleType(models.Model):
    _name = 'module.type'
    _description = 'Duration of module'

    name = fields.Char(required=True)
    time = fields.Float(required=True)
