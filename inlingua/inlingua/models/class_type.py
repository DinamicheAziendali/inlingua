# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Marco Calcagni (mcalcagni@dinamicheaziendali.it)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields


class ClassType(models.Model):
    _name = 'class.type'
    _description = 'Class Type'

    name = fields.Char(required=True)
    max_student = fields.Integer(string='Number max of Student')
    min_student = fields.Integer(string='Number min. of Student')
