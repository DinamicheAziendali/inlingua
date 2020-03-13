# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Marco Calcagni (mcalcagni@dinamicheaziendali.it)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields


class ClassProgramm(models.Model):
    _name = 'class.programm'
    _description = 'Class Programm'

    name = fields.Char(required=True)
