from odoo import models, api, _, fields


class ProjectInherit(models.Model):
    _inherit = "project.task.type"

    method_name = fields.Char("Methodology")
