from odoo import models, api, _, fields
from odoo.exceptions import UserError


class MilestoneProject(models.Model):
    _name = "milestone.project"

    title = fields.Char("Title", required=True)
    active = fields.Boolean(default=True,
                            help="If the active field is set to False, it will allow you to hide the project without removing it.")
    project_id = fields.Many2one("project.project", string="Project")
    milestone_start_date = fields.Date("Start Date")
    milestone_end_date = fields.Date("End Date")
    duration = fields.Integer("No. Of Days")
    # duration = fields.Integer("No. Of Days", compute="_calculate_duration")
    days_remaining = fields.Integer("Remaining days")
    # days_remaining = fields.Integer("Remaining days", compute="_calculate_remaining_days")
    task_count = fields.Integer(compute='_compute_task_count', string='Tasks')

    def _compute_task_count(self):
        task_data = self.env['project.task'].read_group(
            [('project_id', 'in', self.ids), '|', ('stage_id.fold', '=', False), ('stage_id', '=', False)],
            ['project_id'], ['project_id'])
        result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
        for project in self:
            project.task_count = result.get(project.id, 0)
