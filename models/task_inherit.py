from odoo import models, fields, api, _


class TaskInherit(models.Model):
    _inherit = "project.task"

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High')
    ], default='0', index=True, string="Priority")
    updated_issue = fields.Char("Name")
