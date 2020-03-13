import logging
from odoo import models, fields, api

_logger = logging.getLogger('lesson_scheduler')


class Lesson(models.Model):
    _name = 'timetable.lesson'
    _description = 'Resource schedule'

    name = fields.Text()
    #resource_id = fields.Many2one(string='Resource', comodel_name='resource.resource', required=True)
    resource_id = fields.Many2one(string='Resource', comodel_name='res.partner', domain="[('professor', '=', True)]", 
				required=True)
    course_id = fields.Many2one(string='Course', comodel_name='project.project', required=True)
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)
    # from_rule = fields.Many2one(string="From rule", comodel_name="timetable.scheduling_rule")

    _sql_constraints = [
        (
            'resource_booking_overlapping_check',

            'EXCLUDE USING gist (resource_id WITH =, '
            ' numrange(cast(extract(epoch from start_time) as bigint), '
            ' cast(extract(epoch from end_time) as bigint),\'[]\') WITH && )',

            "Resource is already allocated in this time interval"
        )
    ]
