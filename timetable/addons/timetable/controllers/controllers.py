# -*- coding: utf-8 -*-
from odoo import http


class Timetable(http.Controller):
    @http.route('/timetable/timetable/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/timetable/timetable/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('timetable.listing', {
            'root': '/timetable/timetable',
            'objects': http.request.env['timetable.timetable'].search([]),
        })

    @http.route('/timetable/timetable/objects/<model("timetable.timetable"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('timetable.object', {
            'object': obj
        })
