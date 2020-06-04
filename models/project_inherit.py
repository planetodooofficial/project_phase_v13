from odoo import models, api, _, fields


class ProjectInherit(models.Model):
    _inherit = "project.project"

    project_description = fields.Char("Description")
    invite_user = fields.Char("Invite User")
    project_start_date = fields.Date("Project Start Date")
    project_end_date = fields.Date("Project End Date")
    notification_date = fields.Date("Set Remainder for End date")
    project_budget = fields.Selection([("fixed", "Fixed Budget"),
                                       ("weekly", "Weekly Budget"),
                                       ("custom", "Custom Budget")])

    def open_tasks(self):
        super(ProjectInherit, self).open_tasks()
        ctx = dict(self._context)
        ctx.update({'search_default_project_id': self.id})
        action = self.env['ir.actions.act_window'].for_xml_id('project', 'act_project_project_2_project_task_all')
        project_obj = self.env["project.task.type"].create({'name': "Requirement Gathering"})
        return dict(action, context=ctx)
