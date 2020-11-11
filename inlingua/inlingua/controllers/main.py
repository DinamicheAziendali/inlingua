# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Marco Calcagni (mcalcagni@dinamicheaziendali.it)
# @author: Gianmarco Conte (gconte@dinamicheaziendali.it)
# @author: Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import tools, http
from odoo.http import request
from odoo.addons.website_portal.controllers.main import website_account


class website_account(website_account):

    @http.route()
    def account(self, **kw):
        response = super(website_account, self).account(**kw)
        user = request.env.user
        lesson_count = request.env['project.task.student'].sudo().search_count([
            ('student_id', '=', user.partner_id.id)
        ])
        response.qcontext.update({'lesson_count': lesson_count})
        return response

    @http.route(['/my/lessons', '/my/lessons/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_lessons(self, page=1, date_begin=None, date_end=None, **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        Lesson = request.env['project.task.student']

        domain = [
            ('student_id', '=', user.partner_id.id)
        ]

        # count for pager
        lesson_count = Lesson.sudo().search_count(domain)
        # make pager
        pager = request.website.pager(
            url="/my/lessons",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=lesson_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        lessons = Lesson.sudo().search(domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date_begin': date_begin,
            'lessons': lessons.sudo(),
            'pager': pager,
            'default_url': '/my/lessons',
        })

        return request.render("inlingua.portal_my_lessons", values)

    @http.route(['/my/lessons/pdf/<int:lesson_id>'], type='http', auth="user", website=True)
    def portal_get_lesson(self, lesson_id=None, **kw):
        user = request.env.user
        if not user.has_group('inlingua.group_allievo_privato'):
            return request.render("website.403")

        pdf = request.env['report'].sudo().get_pdf([lesson_id], 'inlingua.report_view_progress_report')
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', 'attachment; filename=Progress Report.pdf;')
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)
