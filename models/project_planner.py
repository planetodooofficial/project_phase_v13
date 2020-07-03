from odoo import fields, models, tools


class CalenderPlanner(models.Model):
    _name = "project.planner"
    _inherit = "project.task"
    _order = 'name desc, project_id'
    _auto = False

    project_id = fields.Many2one('project.project', string='Project',
                                 default=lambda self: self.env.context.get('default_project_id'))
    project_start_date = fields.Date("Project Start Date", related="project_id.project_start_date")
    project_end_date = fields.Date("Project End Date", related="project_id.project_end_date")
    create_plan = fields.Selection([
        ('task', 'Task'),
        ('meeting', 'Meeting'),
        ('project', 'Project')
    ], string="Type of Event")
    calendar_event_id = fields.Many2one('calendar.event', string="Calendar Meeting")
