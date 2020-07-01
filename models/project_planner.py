from odoo import fields, models


class CalenderPlanner(models.Model):
    _name = "project.planner"

    # user_id = fields.Many2one('res.users', string='Assigned To', readonly=True)
    # date_assign = fields.Datetime(string='Assignation Date', readonly=True)
    # date_end = fields.Datetime(string='Ending Date', readonly=True)
    date_deadline = fields.Date(string='Deadline', readonly=True)
    # date_last_stage_update = fields.Datetime(string='Last Stage Update', readonly=True)
    project_id = fields.Many2one('project.project', string='Project')
    # priority = fields.Selection([
    #     ('0', 'Low'),
    #     ('1', 'Normal'),
    #     ('2', 'High')
    # ], readonly=True, string="Priority")
    stage_id = fields.Many2one('project.task.type', string='Stage')
    project_start_date = fields.Date("Project Start Date")
    project_end_date = fields.Date("Project End Date")
    create_plan = fields.Selection([
        ('task', 'Task'),
        ('meeting', 'Meeting'),
        ('project', 'Project')
    ], string="Type of Event")
    calendar_event_id = fields.Many2one('calendar.event', string="Calendar Meeting", ondelete='cascade')
