from odoo import models, api, _, fields


class ProjectDashboard(models.Model):
    _name = "project.dashboard"

    name = fields.Char(string="Name")
    method_name = fields.Selection([
        ("waterfall", "Waterfall Model"),
        ("agile", "Agile Model"),
        ("scrum", "Scrum"),
        ("kanban", "Kanban"),
        ("prince", "PRINCE2"),
        ("blank", "Create Custom Method")
    ])

    waterfall_method = fields.Selection([
        ("requirement", "Requirement Gathering"),
        ("analysis", "Analysis"),
        ("design", "Design"),
        ("develop", "Development"),
        ("test", "Testing"),
        ("deploy", "Deployment & maintenance")
    ], default="requirement")

    def method_action(self):
        project_obj = self.env["project.task.type"].create({'name': "Requirement Gathering"})
        return
