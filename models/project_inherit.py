from odoo import models, api, _, fields
from odoo.exceptions import UserError


class ProjectInherit(models.Model):
    _inherit = "project.project"

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', string='Client', auto_join=True, tracking=True)
    project_description = fields.Char("Description")
    invite_user = fields.Many2many("res.users", string="Invite User")
    project_start_date = fields.Date("Project Start Date")
    project_end_date = fields.Date("Project End Date")
    notification_date = fields.Date("Notification Date")
    currency_id = fields.Many2one('res.currency', string="Currency")
    project_budget = fields.Selection([("fixed", "Fixed Budget"),
                                       ("weekly", "Weekly Budget"),
                                       ("custom", "Custom Budget")])
    fixed_budget = fields.Monetary("Total Budget")
    weekly_budget = fields.Monetary("Weekly Budget")
    custom_price = fields.Monetary("Price per hour")
    custom_hours = fields.Integer("Hours")
    custom_minutes = fields.Integer("Minutes")
    # total_custom_price = fields.Monetary("Total cost", compute="_compute_total_cost")
    total_custom_price = fields.Monetary("Total cost")
    methodology = fields.Char("Methodology")

    @api.model
    def create(self, vals):
        # Prevent double project creation
        self = self.with_context(mail_create_nosubscribe=True)
        project = super(ProjectInherit, self).create(vals)
        if not vals.get('subtask_project_id'):
            project.subtask_project_id = project.id
        if project.privacy_visibility == 'portal' and project.partner_id:
            project.message_subscribe(project.partner_id.ids)
        return project

    # def _compute_total_cost(self):
    #     if self.custom_price == 0.0:
    #         raise UserError(_('Please Enter the base price'))
    #     elif self.custom_hours == 0 and self.custom_minutes == 0:
    #         raise UserError(_('Please enter the hours or minutes of the project.'))
    #     else:
    #         if self.custom_minutes == 0:
    #             self.total_custom_price = self.custom_hours * self.custom_price
    #         elif self.custom_hours == 0:
    #             self.total_custom_price = self.custom_minutes * self.custom_price
    #         else:
    #             self.total_custom_price = self.custom_price * self.custom_minutes * self.custom_hours
    #     return

    def open_tasks(self):
        active_id = self.env["project.dashboard"].browse(self.env.context.get('active_ids'))
        self.methodology = dict(active_id._fields['method_name'].selection).get(active_id.method_name)
        if active_id.method_name == 'agile':
            self.env["project.task.type"].create({'name': "Requirement Gathering",
                                                  'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(
                                                      active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Development", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(
                                                      active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Testing", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(
                                                      active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Delivery", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(
                                                      active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Feedback", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(
                                                      active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
        elif active_id.method_name == 'waterfall':
            self.env["project.task.type"].create({'name': "Requirement Gathering", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Analysis", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Design", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Development", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Testing", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Deployment & maintenance", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
        elif active_id.method_name == 'kanban':
            self.env["project.task.type"].create({'name': "New", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "To Do", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "In progress", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Testing", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Done", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
        elif active_id.method_name == 'scrum':
            self.env["project.task.type"].create({'name': "Requirement Gathering", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Update Product backlog", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Development", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Sprint Review", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Delivery", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Sprint Retrospective", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
        elif active_id.method_name == 'prince':
            self.env["project.task.type"].create({'name': "Starting up", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Directing", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Initiating", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create({'name': "Controlling a stage", 'project_ids': [(6, 0, self.ids)],
                                                  'method_name': dict(active_id._fields['method_name'].selection).get(
                                                      active_id.method_name)})
            self.env["project.task.type"].create(
                {'name': "Managing product delivery", 'project_ids': [(6, 0, self.ids)],
                 'method_name': dict(active_id._fields['method_name'].selection).get(active_id.method_name)})
            self.env["project.task.type"].create(
                {'name': "Managing stage boundaries", 'project_ids': [(6, 0, self.ids)],
                 'method_name': dict(active_id._fields['method_name'].selection).get(active_id.method_name)})
            self.env["project.task.type"].create({'name': "Closing", 'project_ids': [(6, 0, self.ids)]})
        return super(ProjectInherit, self).open_tasks()
