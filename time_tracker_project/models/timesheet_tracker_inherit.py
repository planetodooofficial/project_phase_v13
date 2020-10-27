from odoo import models, fields, api, _


class TimesheetTrackerInherit(models.Model):
    _inherit = "account.analytic.line"

    screenshot_id = fields.Many2one("timesheet.tracker", string="Screenshots")


# class ProjectInherit(models.Model):
#     _inherit = "project.project"
#
#     team_id = fields.Many2many('res.users', 'project_user_ids', 'project_id', 'user_id', string="Team")
