

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    commit_ids = fields.Many2many(
        comodel_name="project.git.commit",
        id1="task_id",
        id2="commit_id",
        relation="task_commit_rel",
        string="Commits"
    )

    commits_count = fields.Integer(
        string="Commits Count",
        compute="_compute_commits_count",
    )


    @api.depends('commit_ids')
    def _compute_commits_count(self):
        for record in self:
            record.commits_count = len(record.commit_ids)


    def open_commits(self):
        action = self.env["ir.actions.act_window"].for_xml_id(
            "project_git",
            "action_git_commit",
        )
        action["domain"] = [("task_ids", "in", [self.id])]
        return action
