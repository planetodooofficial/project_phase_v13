from odoo import models, api, _, fields
from datetime import datetime


class MilestoneProject(models.Model):
    _name = "milestone.project"

    milestone_ids = fields.One2many('project.task', 'milestone_id', string='Milestone')
    name = fields.Char("Title", required=True)
    active = fields.Boolean(default=True,
                            help="If the active field is set to False, it will allow you to hide the project without removing it.")
    project_id = fields.Many2one("project.project", string="Project")
    milestone_start_date = fields.Date("Start Date")
    milestone_end_date = fields.Date("End Date")
    duration = fields.Integer("No. Of Days", compute="_calculate_duration")
    days_remaining = fields.Integer("Remaining days", compute="_calculate_remaining_days")
    task_count = fields.Integer(compute='_compute_task_count', string='Tasks')
    milestone_count = fields.Integer(compute='_compute_milestone_count', string='Milestones')

    def _calculate_duration(self):
        for rec in self:
            fmt = '%Y-%m-%d'
            from_date = rec.milestone_start_date
            to_date = rec.milestone_end_date
            d1 = datetime.strptime(str(from_date), fmt)
            d2 = datetime.strptime(str(to_date), fmt)
            rec.duration = str((d2 - d1).days + 1)

    def _calculate_remaining_days(self):
        for rec in self:
            fmt = '%Y-%m-%d'
            from_date = fields.Date.today()
            to_date = rec.milestone_end_date
            d1 = datetime.strptime(str(from_date), fmt)
            d2 = datetime.strptime(str(to_date), fmt)
            rec.days_remaining = str((d2 - d1).days + 1)

    def _compute_task_count(self):
        projects = self.env['project.project'].search([('name', '=', self.project_id.name)])
        has_tasks = self.env['project.task'].search_count([('project_id', 'in', projects.ids)])
        self.task_count = has_tasks

    def _compute_milestone_count(self):
        projects = self.env['project.project'].search([('name', '=', self.project_id.name)])
        has_milestone = self.env['milestone.project'].search_count([('project_id', 'in', projects.ids)])
        self.milestone_count = has_milestone


class ReportProjectMilestone(models.Model):
    _inherit = "report.project.task.user"

    milestone_id = fields.Many2one('milestone.project', string='Milestone')

    def _select(self):
        return super(ReportProjectMilestone, self)._select() + """,
            t.milestone_id"""

    def _group_by(self):
        return super(ReportProjectMilestone, self)._group_by() + """,
            t.milestone_id
            """
