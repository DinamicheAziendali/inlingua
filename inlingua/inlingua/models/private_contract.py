# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Marco Calcagni (mcalcagni@dinamicheaziendali.it)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# @author: Antonio Arcucci (antonio.arcucci@logicos.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).


from odoo import fields, models, api, exceptions, _
from datetime import datetime
# from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import calendar


class PrivateContract(models.Model):
    _name           = 'private.contract'
    _description    = "Private Contract"
    _rec_name       = 'number_contract'
    _inherit        = 'mail.thread'

    def get_tot_invoice(self, contract):
        if contract:
            tot_invoice = 0
            for invoice in contract.invoice_ids:
                tot_invoice += invoice.amount_total
            return tot_invoice

    def get_tot_to_invoice(self, contract):
        if contract:
            # residual_to_invoice = 0
            tot_invoice = self.get_tot_invoice(contract)
            residual_to_invoice = contract.total_value - tot_invoice
            return residual_to_invoice

    def get_date_today(self):
        today = datetime.now().date()
        return today

    type_contract       = fields.Selection(selection=[
                                        ('private', 'Private'),
                                        ('company_without_order',
                                                 'Company without order'),
                                        ('company_with_order',
                                                 'Company with order')],
                                     required=True,
                                     string='Type Contract')

    order_id            = fields.Many2one('sale.order', string='Order')

    partner_id          = fields.Many2one('res.partner', string='Client', required=True,
                                 track_visibility='always')

    contractor_id       = fields.Many2one('res.partner', string='Contractor',
                                 track_visibility='onchange')

    partner_birthplace  = fields.Char(related='partner_id.birthplace',
                                     string='Customer BirthPlace',
                                     track_visibility='onchange')

    partner_resident    = fields.Char(compute='get_partner_resident',
                                   string='Resident',
                                   track_visibility='onchange')

    partner_fiscalcode  = fields.Char(related='partner_id.fiscalcode',
                                     string='Customer FiscalCode',
                                     track_visibility='onchange')

    partner_birthdate   = fields.Date(related='partner_id.birthdate_date',
                                    string='Customer Birthdate',
                                    track_visibility='onchange')

    partner_vat         = fields.Char(related='partner_id.vat',
                              string='Vat', track_visibility='onchange')

    student_id          = fields.Many2one('res.partner', string='Student',
                                 track_visibility='onchange')

    student_birthplace  = fields.Char(related='student_id.birthplace',
                                     string='Student BirthPlace')

    student_resident    = fields.Char(compute='get_student_resident',
                                   string='Resident',
                                   track_visibility='onchange')

    student_fiscalcode  = fields.Char(related='student_id.fiscalcode',
                                     string='Student FiscalCode',
                                     track_visibility='onchange')

    student_birthdate   = fields.Date(related='student_id.birthdate_date',
                                    string='Student Birthdate')

    date_contract       = fields.Date(string='Contract date', default=get_date_today,
                                track_visibility='always')

    language_id         = fields.Many2one('class.language',
                                  string='Course Language',
                                  track_visibility='always')

    course_type_id      = fields.Many2one('class.type', string='Course Type',
                                     track_visibility='onchange')

    programm_id         = fields.Many2one('class.programm',
                                  string='Programm',
                                  track_visibility='onchange')

    module_type_id      = fields.Many2one('module.type',
                                     string='Duration Module',
                                     track_visibility='onchange')

    number_of_module    = fields.Integer('Number of modules',
                                      track_visibility='onchange')

    module4lesson       = fields.Integer('number of module for lesson', default=1,
                                   track_visibility='onchange')

    # da calcolare number_of_module / module4lesson
    number_of_lesson    = fields.Integer(string='Number of Lessons',
                                      compute='get_numb_lesson',
                                      track_visibility='onchange')

    # Costo d'iscrizione
    cost_entry          = fields.Monetary(string="Entry Price",
                                 help='Cost of entry ',
                                 currency_field='currency_id',
                                 track_visibility='onchange')

    # Costo totale dei moduli
    cost_module         = fields.Monetary(string="Modules Cost",
                                  help='Total module price',
                                  currency_field='currency_id',
                                  track_visibility='onchange',
                                  )

    # Costi aggiuntivi
    cost_extra          = fields.Monetary(string="Extra Cost",
                                 help='Extra Cost',
                                 currency_field='currency_id',
                                 track_visibility='onchange')
    
    # calculate totale dei costi del contratto
    total_value         = fields.Monetary(string="Total Value",
                                  help='Total Value',
                                  currency_field='currency_id',
                                  track_visibility='always',
                                  compute='get_total_value')
    
    payment_method_id   = fields.Many2one('account.payment.term',
                                        string='Payment Method',
                                        track_visibility='onchange')
    
    # calculate dell'incassato sul contratto
    balance_value = fields.Monetary(string="Balance Value",
                                    currency_field='currency_id',
                                    track_visibility='onchange',
                                    compute='get_balance',
                                    store=True)

    # calcolo dell'importo da incassare
    to_cash     = fields.Monetary(string="To cash",
                                    currency_field='currency_id',
                                    track_visibility='onchange',
                                    compute='get_to_cash',
                                    store=True)
    
    monday      = fields.Boolean(string='Monday')
    tuesday     = fields.Boolean(string='Tuesday')
    wednesday   = fields.Boolean(string='Wednesday')
    thursday    = fields.Boolean(string='Thursday')
    friday      = fields.Boolean(string='Friday')
    saturday    = fields.Boolean(string='Saturday')

    time_from   = fields.Float('From')
    time_end    = fields.Float('To')

    # private = fields.Boolean('Private')
    # company = fields.Boolean('Company')
    state       = fields.Selection(
                selection=[('to_combine', 'To Combine'),
                        ('combined', 'Combined'),
                        ('in_progress', 'In Progress'),
                        ('processed', 'Processed')],
                string='State',
                readonly=True, compute='compute_state', store=True,
                track_visibility='onchange')

    entry       = fields.Float(string='Entry', track_visibility='onchange')
    deposit     = fields.Monetary(string='Deposit', track_visibility='onchange')
    number_rate = fields.Integer(string='Number Rate', track_visibility='onchange')

    type_due    = fields.Many2one('type.due', string='Due', track_visibility='onchange')

    # rate_amount = fields.Float(string='Rate Amount')
    rate_amount         = fields.Monetary(string='Rate Amount',
                                  compute='compute_rate_amount',
                                  track_visibility='onchange')

    # Elenco degli incassi relazionati
    payment_line_ids    = fields.One2many('payment.term.line', 'contract_id',
                                       track_visibility='onchange')

    student_ids         = fields.Many2many('res.partner', track_visibility='always')
    
    project_course_id   = fields.Many2one('project.project', string='Course',
                                        track_visibility='always')
    
    number_contract     = fields.Char(string='Number Contract',
                                  track_visibility='always')
    
    module_price        = fields.Monetary(string='Module Cost',
                                track_visibility='onchange',
                                compute='get_cost_module',
                                store=True)
    
    invoice_ids         = fields.One2many('account.invoice', 'private_contract_id', string='Invoices')
    
    purchase_id         = fields.Many2one('purchase.order', string='Purchase Order')

    # type_invoice = fields.Selection(
    #     selection=[('total', 'Total'), ('partially', 'Partially')],
    #     string='Type Invoice', store=True)
    # journal_id = fields.Many2one('account.journal', string='Journal')

    @api.constrains('module_type_id')
    def check_time(self):
        for contract in self:
            for module_type in contract.module_type_id:
                if not module_type.time or module_type.time < 1:
                    raise ValidationError('Duration module must be greater 0')

    @api.onchange('type_contract')
    def clear_order(self):
        for contract in self:
            if contract.type_contract != 'company_with_order':
                contract.order_id = False

    @api.onchange('partner_id')
    def set_student_if_partner_is_student(self):
        for contract in self:
            if contract.partner_id.student:
                contract.student_id = contract.partner_id.id

    # Calcolo costo totali dei moduli
    '''
    @api.depends('module_price', 'number_of_module')
    def get_cost_module(self):
        for contract in self:
            if contract.module_price and contract.number_of_module:
                contract.cost_module = contract.module_price * contract.number_of_module
    '''

    # Calcolo costo del singolo modulo
    @api.depends('cost_module', 'number_of_module')
    def get_cost_module(self):
        for contract in self:
            contract.module_price = 0
            if contract.cost_module > 0 and contract.number_of_module > 0:
                contract.module_price = contract.cost_module / contract.number_of_module

    @api.onchange('student_id')
    def get_default_language(self):
        for contract in self:
            if contract.type_contract and contract.type_contract == 'private':
                # if contract.private and not contract.company:
                lang_student = self.env['language.student'].search(
                    [('partner_id', '=', contract.student_id.id)])
                if len(lang_student) == 1:
                    contract.language_id = lang_student.language_id.id
                if len(lang_student) == 0:
                    contract.language_id = False

    # Calcolo del saldo del contratto ovvero quanto resta da incassare
    @api.depends('balance_value', 'total_value')
    def get_to_cash(self):
        for contract in self:
            contract.to_cash = contract.total_value - contract.balance_value

    # Calcolo del saldo del contratto ovvero quanto resta da incassare
    @api.depends('payment_line_ids', 'total_value')
    def get_balance(self):
        for contract in self:
            contract.balance_value = sum(line.rate_amount for line in contract.payment_line_ids)

    # @api.constrains('private', 'company')
    # def _check_contract(self):
    #     if not self.private and not self.company:
    #         raise ValidationError("Contract must be private or for company")

    @api.depends('project_course_id.date_start', 'project_course_id.date_end')
    def compute_state(self):
        today = datetime.now()
        format_date = "%Y-%m-%d"
        for contract in self:
            course = contract.project_course_id
            if course.date_start:
                date_start = datetime.strptime(course.date_start, format_date)
            else:
                date_start = False
            if course.date_end:
                date_end = datetime.strptime(course.date_end, format_date)
            else:
                date_end = False
            if not course:
                contract.state = 'to_combine'
            elif course and date_start and today < date_start:
                contract.state = 'combined'
            elif course and date_end and today > date_end:
                contract.state = 'processed'
            elif course and date_end and date_start \
                    and date_end > today > date_start:
                contract.state = 'in_progress'

    def get_invoice_defaults(self):
        contract_account_income_id = self.env['ir.values'].get_default(
            'inlingua.config.settings', 'contract_account_income')
        contract_invoice_journal_id = self.env['ir.values'].get_default(
            'inlingua.config.settings', 'contract_invoice_journal')
        contract_tax_id = self.env['ir.values'].get_default(
            'inlingua.config.settings', 'contract_tax')
        return (contract_account_income_id, contract_invoice_journal_id,
                contract_tax_id)

    @api.multi
    def create_total_invoice(self):
        for contract in self:
            model_invoice = self.env['account.invoice']
            model_invoice_line = self.env['account.invoice.line']
            total_invoice = sum(
                line.rate_amount for line in contract.payment_line_ids if
                not line.invoiced and line.rate_amount > 0)
            if total_invoice <= 0:
                raise UserError(_(
                    'Nessuna riga disponibile per la fatturazione.'))
            account_id, journal_id, tax_id, = self.get_invoice_defaults()

            if total_invoice > 0:
                invoice = model_invoice.create(
                    {'partner_id': contract.partner_id.id,
                     'journal_id': journal_id,
                     'account_id':
                         contract.partner_id.property_account_receivable_id.id,
                     'private_contract_id': contract.id,
                     })

                for line in contract.payment_line_ids:
                    if not line.invoiced and line.rate_amount > 0:
                        line.invoiced = True
                        line.invoice_id = invoice.id

                date_rate = datetime.strptime(contract.date_contract,
                                              '%Y-%m-%d').strftime('%d/%m/%y')
                
                model_invoice_line.create(
                    {'invoice_id': invoice.id,
                     'name': 'Corso di lingua, contratto n. ' +
                             contract.number_contract + ' del ' + date_rate,
                     'account_id': account_id,
                     'quantity': '1',
                     'price_unit': total_invoice,
                     'invoice_line_tax_ids': [(6, 0, [tax_id])],
                     })

                invoice.compute_taxes()

    @api.multi
    def create_partially_invoice(self):
        for contract in self:
            model_invoice = self.env['account.invoice']
            model_invoice_line = self.env['account.invoice.line']
            total_invoice = sum(
                line.rate_amount for line in contract.payment_line_ids if
                not line.invoiced and line.rate_amount > 0 and line.to_account)

            if total_invoice <= 0:
                raise UserError(_(
                    'Nessuna riga disponibile per la fatturazione.'))
            account_id, journal_id, tax_id, = self.get_invoice_defaults()
            
            if total_invoice > 0:
                invoice = model_invoice.create(
                    {'partner_id': contract.partner_id.id,
                     'journal_id': journal_id,
                     'account_id':
                         contract.partner_id.property_account_receivable_id.id,
                     'private_contract_id': contract.id,
                     })

                for line in contract.payment_line_ids:
                    if not line.invoiced and line.rate_amount > 0 \
                            and line.to_account:
                        line.invoiced = True
                        line.invoice_id = invoice.id

                date_rate = datetime.strptime(contract.date_contract,
                                              '%Y-%m-%d').strftime('%d/%m/%y')
                model_invoice_line.create(
                    {'invoice_id': invoice.id,
                     'name': 'Corso di lingua, contratto n. ' +
                             contract.number_contract + ' del ' + date_rate,
                     'account_id': account_id,
                     'quantity': '1',
                     'price_unit': total_invoice,
                     'invoice_line_tax_ids': [(6, 0, [tax_id])],
                     })
                invoice.compute_taxes()

    @api.multi
    def generate_account_move(self):
        for contract in self:
            model_move = self.env['account.move']
            invoices = {}
            for line in contract.payment_line_ids:
                # if line.invoice_id:
                #     invoices[line.invoice_id] = line.invoice_id.
                if line.to_account and line.rate_amount < 0 and not line.move_id:
                    print 'xx'

    # chiamata solo da write
    def add_student_to_project(self, course, student):
        val = {}
        today = datetime.now().date()
        course_id = self.env['project.project'].browse(course)
        model_project_student = self.env['project.student']
        if student:
            student_id = self.env['res.partner'].browse(student)
        else:
            student_id = self.student_id
        proj_student = model_project_student.search(
            [('project_id', '=', course),
             ('student_id', '=', student_id.id)])
        if proj_student:
            pass
        else:
            for course in course_id:
                if course.date_start and datetime.strptime(course.date_start,
                                                           '%Y-%m-%d').date() >= today:
                    val['project_id'] = course_id.id
                    val['student_id'] = student_id.id
                    model_project_student.create(val)

    def add_student_to_task_project(self, course, student):
        val = {}
        today = datetime.now().date()
        course_id = self.env['project.project'].browse(course)
        model_project_task_student = self.env['project.task.student']
        if student:
            student_id = self.env['res.partner'].browse(student)
        else:
            student_id = self.student_id
        for lesson in course_id.task_ids:
            students = []
            for student in lesson.task_student_ids:
                students.append(student.student_id.id)
            if student_id.id in students:
                pass
            else:
                if lesson.date_deadline and datetime.strptime(
                        lesson.date_deadline, '%Y-%m-%d').date() >= today:
                    val['task_id'] = lesson.id
                    val['student_id'] = student_id.id
                    model_project_task_student.create(val)
            students = []

    def remove_student_from_project_and_task(self):
        for contract in self:
            if contract.type_contract and contract.type_contract == 'private':
                # if contract.private == True:
                for course in contract.project_course_id:
                    for student in course.project_student_ids:
                        if student.student_id == contract.student_id:
                            student.unlink()
                    for task in course.task_ids:
                        for student in task.task_student_ids:
                            if student.student_id == contract.student_id:
                                student.unlink()
            if contract.type_contract and contract.type_contract != 'private':
                # if contract.company == True:
                for contract_student in contract.student_ids:
                    for course in contract.project_course_id:
                        for student in course.project_student_ids:
                            if student.student_id == contract_student:
                                student.unlink()
                        for task in course.task_ids:
                            for student in task.task_student_ids:
                                if student.student_id == contract_student:
                                    student.unlink()

    @api.model
    def create(self, vals):
        vals['number_contract'] = self.env['ir.sequence'].next_by_code(
            'private.contract')
        if vals['project_course_id'] != False:
            if vals['type_contract'] == 'private':
                # if vals['private'] == True:
                self.add_student_to_project(vals['project_course_id'],
                                            vals['student_id'])
                self.add_student_to_task_project(vals['project_course_id'],
                                                 vals['student_id'])
            if vals['type_contract'] == 'company_with_order' or \
                            vals['type_contract'] == 'company_without_order':
                # elif vals['company'] == True:
                if len(vals['student_ids']) > 0:
                    students = vals['student_ids'][0][2]
                    for student in students:
                        self.add_student_to_project(vals['project_course_id'],
                                                    student)
                        self.add_student_to_task_project(
                            vals['project_course_id'], student)
        return super(PrivateContract, self).create(vals)

    @api.multi
    def write(self, vals):
        for contract in self:
            if contract.type_contract and contract.type_contract == 'private':
                # if contract.private:
                if 'student_id' in vals.keys():
                    students = [vals['student_id']]
                else:
                    students = [self.student_id.id]
                    # students = False
                if 'project_course_id' in vals.keys():
                    if vals[
                        'project_course_id'] == False and not 'student_id' in vals.keys():
                        self.remove_student_from_project_and_task()  # Se rimuovo corso su contratto deve eliminare alunno o alunni da project e tutte task ***FUNZIONA
                    elif vals['project_course_id'] != False:
                        # if not students:
                        #     students = [False]
                        if not self.project_course_id:  # Quando aggiungo solo il corso aggiungo a proj e task tutti gli alunni (PRV E AZIENDALE OK)
                            for student in students:
                                self.add_student_to_project(
                                    vals['project_course_id'], student)
                                self.add_student_to_task_project(
                                    vals['project_course_id'], student)
                        else:  # se cambio il corso OK PRV E COMPANY
                            # if students:
                            #     students = [students]
                            for student in students:
                                self.remove_student_from_project_and_task()
                                self.add_student_to_project(
                                    vals['project_course_id'], student)
                                self.add_student_to_task_project(
                                    vals['project_course_id'], student)
                elif not 'project_course_id' in vals.keys() and students:  # se cambiano solo studenti e non corso: OK
                    # if contract.private:
                    #     students = [students]
                    for student in students:
                        self.remove_student_from_project_and_task()
                        self.add_student_to_project(
                            self.project_course_id.id,
                            student)
                        self.add_student_to_task_project(
                            self.project_course_id.id,
                            student)
            else:
                if 'student_ids' in vals.keys():
                    students = vals['student_ids']
                else:
                    students = False
                if 'project_course_id' in vals.keys():
                    if vals['project_course_id'] == False and not students:
                        self.remove_student_from_project_and_task()  # Se rimuovo corso su contratto deve eliminare alunno o alunni da project e tutte task ***FUNZIONA

                    elif vals[
                        'project_course_id'] != False and not contract.project_course_id:  # se sto aggiungendo corso
                        if not 'student_ids' in vals.keys():
                            if contract.student_ids:
                                # students = contract.student_ids
                                students = [student.id for student in
                                            contract.student_ids]
                                # if not self.project_course_id:  # Quando aggiungo solo il corso aggiungo a proj e task tutti gli alunni (PRV E AZIENDALE OK)
                                self.remove_student_from_project_and_task()
                                for student in students:
                                    self.add_student_to_project(
                                        vals['project_course_id'], student)
                                    self.add_student_to_task_project(
                                        vals['project_course_id'], student)
                        else:
                            if len(students[0][2]) > 0:
                                self.remove_student_from_project_and_task()
                                for student in students[0][2]:
                                    self.add_student_to_project(
                                        vals['project_course_id'], student)
                                    self.add_student_to_task_project(
                                        vals['project_course_id'], student)

                    elif vals[
                        'project_course_id'] != False and contract.project_course_id:  # se cambio corso
                        self.remove_student_from_project_and_task()
                        if not students:
                            students = [student.id for student in
                                        self.student_ids]
                            for student in students:
                                self.add_student_to_project(
                                    vals['project_course_id'], student)
                                self.add_student_to_task_project(
                                    vals['project_course_id'], student)
                        else:
                            if len(students[0][2]) > 0:
                                for student in students[0][2]:
                                    self.add_student_to_project(
                                        vals['project_course_id'],
                                        student)
                                    self.add_student_to_task_project(
                                        vals['project_course_id'],
                                        student)
                elif not 'project_course_id' in vals.keys() and students:
                    self.remove_student_from_project_and_task()
                    if len(students[0][2]) > 0:
                        for student in students[0][2]:
                            self.add_student_to_project(
                                self.project_course_id.id,
                                student)
                            self.add_student_to_task_project(
                                self.project_course_id.id,
                                student)
            return super(PrivateContract, self).write(vals)




            # if contract.company:
            #     if 'student_ids' in vals.keys():
            #         students = vals['student_ids']
            #     else:
            #         students = False

    @api.depends('cost_entry', 'cost_extra', 'number_rate', 'cost_module',
                 'deposit')
    def compute_rate_amount(self):
        if self.number_rate > 0:
            self.rate_amount = (
                                   self.total_value - self.deposit) \
                               / self.number_rate

    # Generazione delle rate del contratto
    def get_rate(self):
        if self.number_rate > 0 and self.rate_amount > 0 \
                and self.type_due and not self.payment_line_ids:
            self.compute_rate(self.deposit, self.number_rate,
                              self.rate_amount, self.type_due)
        else:
            raise exceptions.Warning("Isn't possible create a Rate")

    def compute_rate(self, deposit, number_rate, rate_amount,
                     type_due):
        model_payment_term = self.env['payment.term.line']
        date_rate = datetime.now().date()
        rng_rate = range(number_rate)
        n_rate = 0
        if self.type_contract and self.type_contract == 'private':
            # if self.private:
            if deposit > 0:
                model_payment_term.create({'contract_id': self.id,
                                           'rate_amount': deposit,
                                           'date': date_rate})
            if type_due.name == 'mensile':
                self.compute_monthly_rate(n_rate, rng_rate, model_payment_term,
                                          rate_amount, date_rate)
            if type_due.name == 'trimestrale':
                self.compute_quarterly_rate(n_rate, rng_rate,
                                            model_payment_term,
                                            rate_amount, date_rate)

    # Calcolo rate mensili
    def compute_monthly_rate(self, n_rate, rng_rate, model_payment_term,
                             rate_amount, date_rate):
        while n_rate < len(rng_rate):
            for rate in rng_rate:
                if date_rate.day < 28:
                    date_rate = date_rate + relativedelta(months=1)
                    model_payment_term.create(
                        {'contract_id': self.id,
                         'rate_amount': rate_amount,
                         'date': date_rate})
                else:
                    date_rate = date_rate + relativedelta(months=1)
                    year = date_rate.year
                    month = date_rate.month
                    last_day_month = \
                        calendar.monthrange(year, month)[1]
                    date_rate = date_rate.replace(
                        day=last_day_month)
                    model_payment_term.create(
                        {'contract_id': self.id,
                         'rate_amount': rate_amount,
                         'date': date_rate})
                n_rate += 1

    # Calcolo rate trimestrali
    def compute_quarterly_rate(self, n_rate, rng_rate, model_payment_term,
                               rate_amount, date_rate):
        while n_rate < len(rng_rate):
            for rate in rng_rate:
                if date_rate.day < 28:
                    date_rate = date_rate + relativedelta(months=3)
                    model_payment_term.create(
                        {'contract_id': self.id,
                         'rate_amount': rate_amount,
                         'date': date_rate})
                else:
                    date_rate = date_rate + relativedelta(months=3)
                    year = date_rate.year
                    month = date_rate.month
                    last_day_month = \
                        calendar.monthrange(year, month)[1]
                    date_rate = date_rate.replace(
                        day=last_day_month)
                    model_payment_term.create(
                        {'contract_id': self.id,
                         'rate_amount': rate_amount,
                         'date': date_rate})
                n_rate += 1

    def get_partner_resident(self):
        partner = self.partner_id
        if partner.city and partner.state_id and partner.street:
            residence = str(partner.street) + ' ' + str(partner.city) + \
                        '(' + str(partner.state_id.code) + ')'
        elif partner.city and partner.street:
            residence = str(partner.street) + ' ' + str(partner.city)
        else:
            residence = str(partner.city)
        self.partner_resident = residence.replace('False', ' ')

    def get_student_resident(self):
        student = self.student_id
        if student.city and student.state_id and student.street:
            residence = str(student.street) + ' ' + str(student.city) + \
                        '(' + str(student.state_id.code) + ')'
        elif student.city and student.street:
            residence = str(student.street) + ' ' + str(student.city)
        else:
            residence = str(student.city)
        self.student_resident = residence.replace('False', ' ')

    def _get_default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    # default da prendere currency della company
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=_get_default_currency_id,
                                  track_visibility='always', required=True)

    @api.depends('cost_entry', 'cost_module', 'cost_extra')
    def get_total_value(self):
        for contract in self:
            contract.total_value = contract.cost_entry + contract.cost_module + contract.cost_extra

    @api.depends('number_of_module', 'module4lesson')
    def get_numb_lesson(self):
        if self.number_of_module and self.module4lesson > 0:
            self.number_of_lesson = self.number_of_module / self.module4lesson

    @api.multi
    def open_wizard_add_rate(self):

        '''
        # add_rate_view_wizard è una vista (wizard_add_rate.xml), la quale usa 
        # il modello transiente add.rate.wizard che si trova in ./wizard/wizard_add_rate.py
        '''
        view_ref = self.env['ir.model.data'].get_object_reference(
            'inlingua', 'add_rate_view_wizard')
        view_id = view_ref[1] if view_ref else False
        context = self._context.copy()
        return {
            'name': 'Add Cash Out',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(False, 'form'), (False, 'form')],
            'res_model': 'add.rate.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_contract_id': self.id,},
            'nodestroy': False,
            'flags': {
                'action_buttons': False,
                'sidebar': False,
            },

        }
