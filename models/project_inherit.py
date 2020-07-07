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
    fixed_budget = fields.Monetary("Total Budget", currency_field='currency_id')
    weekly_budget = fields.Monetary("Weekly Budget", currency_field='currency_id')
    custom_price = fields.Monetary("Price per hour", currency_field='currency_id')
    custom_hours = fields.Integer("Hours")
    custom_minutes = fields.Integer("Minutes")
    total_custom_price = fields.Monetary("Total cost", currency_field='currency_id', compute="_compute_total_cost")
    methodology = fields.Char("Methodology")
    channel_id = fields.Many2one('mail.channel', string='Channel', ondelete='cascade')
    enable_chat = fields.Selection([
        ("yes", "Yes"),
        ("no", "No")
    ], string="Create Chat Channel", default='yes')
    enable_time_tracker = fields.Selection([
        ("yes", "Yes"),
        ("no", "No")
    ], string="Enable Time Tracking", default='yes')
    announce_count = fields.Integer(string="Announcements")
    attachment_ids = fields.Many2many('ir.attachment', string='Files')

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

    def _compute_total_cost(self):
        if self.project_budget == "custom":
            if self.custom_price == 0.0:
                raise UserError(_('Please Enter the base price'))
            elif self.custom_hours == 0 and self.custom_minutes == 0:
                raise UserError(_('Please enter the hours or minutes of the project.'))
            else:
                if self.custom_minutes == 0:
                    self.total_custom_price = self.custom_hours * self.custom_price
                elif self.custom_hours == 0:
                    self.total_custom_price = self.custom_minutes * self.custom_price
                else:
                    self.total_custom_price = self.custom_price * self.custom_minutes * self.custom_hours
        else:
            self.total_custom_price = 0
        return

    def action_project_view(self):
        action = self.env.ref('project_phases_v13.view_project_phase').read()[0]
        action['params'] = {
            'project_ids': self.ids,
        }
        action['context'] = {
            'active_id': self.id,
            'active_ids': self.ids,
            'search_default_name': self.name,
        }
        return action

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
                                                      active_id._fields[
                                                          'method_name'].selection).get(
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
        if self.enable_chat == 'yes':
            channel_obj = self.env["mail.channel"]
            channel_obj.sudo().create({
                'name': self.name,
            })

            channel_obj1 = channel_obj.search([('name', '=', self.name)])
            for res in self.invite_user:
                channel_obj2 = channel_obj1.sudo().write({
                    'channel_last_seen_partner_ids': [(0, 0, {'partner_id': res.partner_id.id})]

                })
                message = _("%s has been added to the channel</br>") % res.partner_id.name
                channel_obj1.sudo().message_post(body=message, message_type="comment", subtype="mail.mt_comment")
            self.channel_id = channel_obj1.id
            self.message_pop()

        return super(ProjectInherit, self).open_tasks()

    def message_pop(self):
        message_id = self.env['message.wizard'].create({'message': _("Invitation is successfully sent")})
        return {
            'name': _('Successful'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            # pass the id
            'res_id': message_id.id,
            'target': 'new'
        }
