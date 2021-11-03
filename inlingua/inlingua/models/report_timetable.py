# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today:
# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models, api
from odoo.exceptions import UserError
from dateutil.parser import parse
from datetime import timedelta
import base64

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.platypus.paragraph import Paragraph
from werkzeug.urls import url_join


class ReportTimetable(models.Model):
    _name = "report.timetable"
    _description = "Print report timetable"

    name = fields.Char(string="Descrizione", compute="_compute_name")
    date_start = fields.Date(string="Data inizio", required=True)
    date_end = fields.Date(string="Data fine", compute="_compute_date_end")
    file_pdf = fields.Binary(string="File PDF")
    file_name_pdf = fields.Char(string="File Name", compute="_compute_file_name_pdf")

    @api.depends("date_start")
    def _compute_date_end(self):
        for report in self:
            if report.date_start:
                date_start = parse(report.date_start)
                report.date_end = date_start + timedelta(days=6)
            else:
                report.date_end = False

    @api.depends("name", "file_pdf")
    def _compute_file_name_pdf(self):
        for report in self:
            if report.file_pdf:
                report.file_name_pdf = report.name + ".pdf"
            else:
                report.file_name_pdf = False

    @api.depends("date_start", "date_end")
    def _compute_name(self):
        for report in self:
            if report.date_start and report.date_end:
                date_start = parse(report.date_start)
                date_end = parse(report.date_end)
                report.name = "Timetable: %s - %s" % (
                    date_start.strftime("%d/%m/%Y"), date_end.strftime("%d/%m/%Y"))

    @api.model
    def create(self, vals):
        res = super(ReportTimetable, self).create(vals)
        date_start = parse(res.date_start)
        date_end = parse(res.date_end)
        delta = date_end - date_start
        if date_start.weekday() != 0:
            raise UserError("La data iniziale deve essere di lunedì")
        if delta.days >= 7:
            raise UserError("La differenza tra le date è maggiore di 7")
        return res

    def get_template_report_timetable(self, report, logo, date_start, height, width):
        style_bold_center_28 = ParagraphStyle("bold_center_28")
        style_bold_center_28.fontSize = 28
        style_bold_center_28.fontName = "Helvetica-Bold"

        if date_start.month == 1:
            month = "GENNAIO"
        elif date_start.month == 2:
            month = "FEBBRAIO"
        elif date_start.month == 3:
            month = "MARZO"
        elif date_start.month == 4:
            month = "APRILE"
        elif date_start.month == 5:
            month = "MAGGIO"
        elif date_start.month == 6:
            month = "GIUGNO"
        elif date_start.month == 7:
            month = "LUGLIO"
        elif date_start.month == 8:
            month = "AGOSTO"
        elif date_start.month == 9:
            month = "SETTEMBRE"
        elif date_start.month == 10:
            month = "OTTOBRE"
        elif date_start.month == 11:
            month = "NOVEMBRE"
        else:
            month = "DICEMBRE"

        report.drawImage(logo, 1 * cm, 27.5 * cm, 7.50 * cm, 1.50 * cm, mask="auto")
        month_paragraph = Paragraph("<u>" + month + " " + str(date_start.year) + "</u>", style_bold_center_28)
        month_paragraph.wrapOn(report, width, height)
        month_paragraph.drawOn(report, 32 * cm, 28.5 * cm)
        return report

    def create_dict_professors_colors(self, lessons_ids):
        dict_professors_colors = {}
        for professor_id in lessons_ids.mapped("professor_id").sorted(lambda p: p.name):
            dict_hour_lesson = {}
            for lesson_id in lessons_ids.filtered(lambda x: x.professor_id.id == professor_id.id).sorted(
                    lambda x: x.start_time):
                start_hour = \
                    "0" + lesson_id.start_hour[:-3] if len(lesson_id.start_hour) == 7 else lesson_id.start_hour[:-3]
                end_hour = "0" + lesson_id.end_hour[:-3] if len(lesson_id.end_hour) == 7 else lesson_id.end_hour[:-3]
                hour_lesson = start_hour + " - " + end_hour + "\n" + lesson_id.name
                if hour_lesson in dict_hour_lesson:
                    dict_hour_lesson[hour_lesson].append(lesson_id.color_course)
                else:
                    dict_hour_lesson[hour_lesson] = [lesson_id.color_course]
                dict_professors_colors[professor_id.name] = dict_hour_lesson
        return dict_professors_colors

    def create_dict_professors(self, lessons_ids):
        dict_professors = {}
        for professor_id in lessons_ids.mapped("professor_id").sorted(lambda p: p.name):
            dict_hour_lesson = {}
            for lesson_id in lessons_ids.filtered(lambda x: x.professor_id.id == professor_id.id).sorted(
                    lambda x: x.start_time):
                start_hour = \
                    "0" + lesson_id.start_hour[:-3] if len(lesson_id.start_hour) == 7 else lesson_id.start_hour[:-3]
                end_hour = "0" + lesson_id.end_hour[:-3] if len(lesson_id.end_hour) == 7 else lesson_id.end_hour[:-3]
                hour_lesson = start_hour + " - " + end_hour
                weekday = parse(lesson_id.start_time).weekday()
                if hour_lesson in dict_hour_lesson:
                    if weekday in dict_hour_lesson[hour_lesson].keys():
                        dict_hour_lesson[hour_lesson][weekday].append(hour_lesson + "\n" + lesson_id.name)
                    else:
                        dict_hour_lesson[hour_lesson][weekday] = [hour_lesson + "\n" + lesson_id.name]
                else:
                    dict_hour_lesson[hour_lesson] = {
                        weekday: [hour_lesson + "\n" + lesson_id.name]
                    }
                dict_professors[professor_id.name] = dict_hour_lesson
        return dict_professors

    def get_course_color(self, lessons_ids, professor_name, line):
        dict_professors_colors = self.create_dict_professors_colors(lessons_ids)
        if professor_name in dict_professors_colors.keys():
            if line in dict_professors_colors[professor_name].keys():
                if dict_professors_colors[professor_name][line][0] == 'red':
                    return colors.red
                elif dict_professors_colors[professor_name][line][0] == 'pink':
                    return colors.pink
                elif dict_professors_colors[professor_name][line][0] == 'violet':
                    return colors.violet
                elif dict_professors_colors[professor_name][line][0] == 'cyan':
                    return colors.cyan
                elif dict_professors_colors[professor_name][line][0] == 'teal':
                    return colors.teal
                elif dict_professors_colors[professor_name][line][0] == 'lime':
                    return colors.lime
                elif dict_professors_colors[professor_name][line][0] == 'yellow':
                    return colors.yellow
                elif dict_professors_colors[professor_name][line][0] == 'orange':
                    return colors.orange
                elif dict_professors_colors[professor_name][line][0] == 'gray':
                    return colors.gray
                else:
                    return colors.white
            else:
                return colors.white
        else:
            return colors.white

    def create_pdf(self):
        file_name = "Timetable.pdf"
        report = canvas.Canvas(file_name)
        report.setPageSize(landscape(A3))
        height, width = A3
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        logo = ImageReader(url_join(base_url, "web/binary/company_logo"))
        date_start = parse(self.date_start)
        date_end = parse(self.date_end)
        lessons_ids = self.env["project.task"].search([
            ("start_time", ">=", self.date_start),
            ("start_time", "<=", self.date_end),
        ])
        style_bold_center_14 = ParagraphStyle("bold_center_12")
        style_bold_center_14.fontSize = 14
        style_bold_center_14.alignment = TA_LEFT
        style_bold_center_14.fontName = "Helvetica-Bold"

        self.get_template_report_timetable(report, logo, date_start, height, width)
        header = [[""]]
        delta = timedelta(days=1)
        while date_start <= date_end:
            if date_start.weekday() == 0:
                day = "LUNEDÌ " + str(date_start.day)
            elif date_start.weekday() == 1:
                day = "MARTEDÌ " + str(date_start.day)
            elif date_start.weekday() == 2:
                day = "MERCOLEDÌ " + str(date_start.day)
            elif date_start.weekday() == 3:
                day = "GIOVEDÌ " + str(date_start.day)
            elif date_start.weekday() == 4:
                day = "VENERDÌ " + str(date_start.day)
            elif date_start.weekday() == 5:
                day = "SABATO " + str(date_start.day)
            else:
                day = "DOMENICA " + str(date_start.day)
            header[0].append(day)
            date_start += delta
        style = [
            ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
        tables = [Table(header, colWidths=[5 * cm], style=style)]
        dict_professors = self.create_dict_professors(lessons_ids)
        for dict_professor in sorted(dict_professors.keys()):
            professor_name = Paragraph(dict_professor, style_bold_center_14)
            data = [[professor_name, "", "", "", "", "", "", ""]]
            n = 0
            for hour_lesson in sorted(dict_professors[dict_professor].keys()):
                n += 1
                for weekday in dict_professors[dict_professor][hour_lesson]:
                    if weekday in [0, 1, 2, 3, 4, 5]:
                        if n == 1:
                            data[0].pop(weekday + 1)
                            data[0].insert(weekday + 1,
                                           dict_professors[dict_professor][hour_lesson][weekday][0])
                        else:
                            if not n - 1 < len(data):
                                data.append(["", "", "", "", "", "", "", ""])
                            data[n - 1].pop(weekday + 1)
                            data[n - 1].insert(weekday + 1,
                                               dict_professors[dict_professor][hour_lesson][weekday][0])
                    else:
                        if n == 1:
                            data[0].pop()
                            data[0].insert(-1, dict_professors[dict_professor][hour_lesson][weekday][0])
                        else:
                            if not n - 1 < len(data):
                                data.append(["", "", "", "", "", "", "", ""])
                            data[n - 1].pop()
                            data[n - 1].insert(-1, dict_professors[dict_professor][hour_lesson][weekday][0])

            for line in data:
                style = [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]

                if line[1] != '':
                    style.append(
                        ("BACKGROUND", (1, 0), (1, -1), self.get_course_color(lessons_ids, dict_professor, line[1])),
                    )
                if line[2] != '':
                    style.append(
                        ("BACKGROUND", (2, 0), (2, -1), self.get_course_color(lessons_ids, dict_professor, line[2])),
                    )
                if line[3] != '':
                    style.append(
                        ("BACKGROUND", (3, 0), (3, -1), self.get_course_color(lessons_ids, dict_professor, line[3])),
                    )
                if line[4] != '':
                    style.append(
                        ("BACKGROUND", (4, 0), (4, -1), self.get_course_color(lessons_ids, dict_professor, line[4])),
                    )
                if line[5] != '':
                    style.append(
                        ("BACKGROUND", (5, 0), (5, -1), self.get_course_color(lessons_ids, dict_professor, line[5])),
                    )
                if line[6] != '':
                    style.append(
                        ("BACKGROUND", (6, 0), (6, -1), self.get_course_color(lessons_ids, dict_professor, line[6])),
                    )
                if line[-1] != '':
                    style.append(
                        ("BACKGROUND", (-1, 0), (-1, -1), self.get_course_color(lessons_ids, dict_professor, line[-1])),
                    )
                tables.append(Table([line], colWidths=[5 * cm], style=style))
        aW = width
        aH = height - (4 * cm)
        x = 1 * cm
        y = 27 * cm
        for table in tables:
            tW, tH = table.wrapOn(report, aW, aH)
            if aH < tH:
                y = 27 * cm
                report.showPage()
                self.get_template_report_timetable(report, logo, date_start, height, width)
                style = [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 12),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
                header_table = Table(header, colWidths=[5 * cm], style=style)
                hTW, hTH = header_table.wrapOn(report, width, height - (4 * cm))
                header_table.drawOn(report, x, y - hTH)
                table.drawOn(report, x, y - hTH - tH)
                y = y - hTH - tH
                if hTH + tH < height - (4 * cm):
                    aH = height - (4 * cm) - hTH - tH
                else:
                    aH = hTH + tH % (height - (4 * cm))
            else:
                table.drawOn(report, x, y - tH)
                y = y - tH
                aH = aH - tH

        report.showPage()
        report.save()

        with open(file_name, "rb") as file_timetable:
            file_base64 = base64.b64encode(file_timetable.read())
        self.write({"file_pdf": file_base64})
