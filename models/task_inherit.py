from odoo import models, fields, api, _


class TaskInherit(models.Model):
    _inherit = "project.task"

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High')
    ], default='0', index=True, string="Priority")
    updated_issue = fields.Char("Name")
    parent_task_name = fields.Char(string="Sub-task Of:", compute="_parent_task_name")
    project_id = fields.Many2one('project.project', string='Project')

    def _parent_task_name(self):
        self.parent_task_name = self.parent_id.name
