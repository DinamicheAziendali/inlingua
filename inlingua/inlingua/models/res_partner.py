# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).


from odoo import fields, models, api


class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    birthplace  = fields.Char(string='BirthPlace')
    student     = fields.Boolean(string='Student')
    professor   = fields.Boolean(string='Professor')
    contractor  = fields.Boolean(string='Contractor')

    language_ids = fields.One2many('language.student', 'partner_id',
                                   string='Language')
    language_professor_ids = fields.One2many('language.professor',
                                             'partner_id',
                                             string='Languages taught')
    
    professional_title_ids = fields.Many2many('partner.professional.title',
                                              string='Professional Titles')

    # non più usati: start
    qualification = fields.Char(string='Qualification')
    # non più usati: end

    lesson_ids = fields.One2many('project.task', 'professor_id', string='Lezioni')
    lesson_count = fields.Integer(compute='_compute_lesson_count', string='# lezioni')

    def _compute_lesson_count(self):
        for partner in self:
            partner.lesson_count = len(partner.lesson_ids)

    @api.multi
    def name_get(self):
        res = []
        for partner in self:
            name = partner.name or ''
            # if partner.company_name or partner.parent_id:
            # if not name and partner.type in ['invoice', 'delivery',
            #                                  'other']:
            #     name = dict(self.fields_get(['type'])['type']['selection'])[
            #         partner.type]
            # if not partner.is_company:
            #     name = "%s, %s" % (
            #     partner.commercial_company_name or partner.parent_id.name,
            #     name)
            if self._context.get('show_address_only'):
                name = partner._display_address(without_company=True)
            if self._context.get('show_address'):
                name = name + "\n" + partner._display_address(
                    without_company=True)
            name = name.replace('\n\n', '\n')
            name = name.replace('\n\n', '\n')
            if self._context.get('show_email') and partner.email:
                name = "%s <%s>" % (name, partner.email)
            if self._context.get('html_format'):
                name = name.replace('\n', '<br/>')
            res.append((partner.id, name))
        return res


class LanguageStudent(models.Model):
    _name = 'language.student'
    _rec_name = 'language_id'

    language_id = fields.Many2one('class.language', string='Language',
                                  required=True)
    current_level = fields.Many2one('student.level', string='Current Level')
    be_reached_level = fields.Many2one('student.level',
                                       string='Level to be Reached')
    partner_id = fields.Many2one('res.partner')


class LanguageProfessor(models.Model):
    _name = 'language.professor'
    _rec_name = 'language_id'

    language_id = fields.Many2one('class.language', string='Language Taught',
                                  required=True)
    partner_id = fields.Many2one('res.partner')
