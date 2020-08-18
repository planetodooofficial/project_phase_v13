

from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = "project.project"

    repository_ids = fields.One2many(
        comodel_name="project.git.repository",
        string="Repositories",
        inverse_name="project_id"
    )
