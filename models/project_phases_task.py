from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    phase_ids = fields.Many2one("project.phases")
    method_name = fields.Selection([
        ("waterfall", "Waterfall Model"),
        ("agile", "Agile Model"),
        ("scrum", "Scrum"),
        ("kanban", "Kanban"),
        ("prince", "PRINCE2")
    ], string="Select the Project Methodology")
