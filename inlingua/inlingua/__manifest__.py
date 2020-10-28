# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
#     Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Marco Calcagni (mcalcagni@dinamicheaziendali.it)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

# noinspection PyStatementEffect
{
    'name': 'inlingua',
    'application': True,
    'version': '1.0.1',
    'category': 'inlingua',
    'summary': 'Custom model for inlingua',
    'description': """
    Applicazione per i centri di formazione inlingua Italia.
    """,
    'author': 'Marco Calcagni, Gianmarco Conte, Antonio Arcucci, Marco Magnetti',
    'website': 'https://www.logicos.it/',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'report',
        'partner_contact_birthdate',
        'l10n_it_fiscalcode',
        'l10n_it_fatturapa',
        'project',
        'project_task_default_stage',
        'hr_timesheet',
        'hr',
        'purchase',
        'sale',
        'partner_firstname',
        'account',
        'base_location',
        'web'
    ],
    'data': [
        'views/assets.xml',
        "views/timetable.xml",
        'security/res_groups.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'report/paperformat.xml',
        'report/header-footer.xml',
        'report/report_journal_entries.xml',
        'report/report_private_contract.xml',
        'report/report_purchase_order.xml',
        'report/report_receipt.xml',
        'report/report_course.xml',
        'report/report_course_sheet.xml',
        'report/report_material_delivered.xml',
        'report/report_contract_receipt.xml',
        'report/report_purchase_order_terzista.xml',
        'wizard/wizard_print_contract_receipt.xml',
        'views/res_partner.xml',
        'views/res_partner_student.xml',
        'views/private_contract.xml',
        'views/menu.xml',
        'views/project.xml',
        'views/office_activity.xml',
        'views/report_view_private_contract.xml',
        'views/report_receipt_private_contract.xml',
        'views/payment_term_line.xml',
        'views/project_task.xml',
        'views/purchase_order.xml',
        'views/purchase_order_liste.xml',
        'views/report_purchase_order_view.xml',
        'views/template_journal_entries_view.xml',
        'views/receipt_view_report.xml',
        'views/class_type.xml',
        'views/attendance_register_view_report.xml',
        'views/material_delivered_view_report.xml',
        'views/sale_order.xml',
        'views/account_invoice.xml',
        'views/res_users.xml',
        'views/contract_receipt_template.xml',
        'wizard/wizard_journal_entries.xml',
        'wizard/wizard_add_rate.xml',
        'wizard/wizard_delivered_material.xml',
        'views/inlingua_config_settings.xml',
        'data/inlingua_data.xml',
    ],
    'installable': True,
    'qweb': [
        'static/src/xml/*.xml'
    ],
}
