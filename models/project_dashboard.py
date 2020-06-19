from odoo import models,\
    fields


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

    agile_method = fields.Selection([
        ("requirement", "Requirement Gathering"),
        ("develop", "Development"),
        ("test", "Testing"),
        ("delivery", "Delivery"),
        ("feedback", "Feedback")
    ], default="requirement")
