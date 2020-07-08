from odoo import fields, models, tools


class CalendarPlanner(models.Model):
    _inherit = "calendar.event"

    project_id = fields.Many2one('project.project', string='Project')
    project_start_date = fields.Date("Project Start Date", related="project_id.project_start_date")
    project_end_date = fields.Date("Project End Date", related="project_id.project_end_date")
    project_name = fields.Char("Project Name", related="project_id.name")
    create_plan = fields.Selection([
        ('task', 'Task'),
        ('meeting', 'Meeting'),
        ('project', 'Project')
    ], string="Type of Event")

    def create_event(self):
        calendar_event = self.env['calendar.event'].create({
            'name': self.project_name,
            'start': self.project_start_date,
            'stop': self.project_end_date,
        })
