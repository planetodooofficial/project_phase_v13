from odoo import models, api, _, fields
from odoo.exceptions import UserError, ValidationError


class Users(models.Model):
    _inherit = "res.users"

    @api.model_create_multi
    def create(self, vals_list):
        users = super(Users, self).create(vals_list)
        group = self.env['res.groups'].search([('name', '=', 'See all Timesheets')])
        users.write({
            'groups_id': [(6, 0, [group.id])] or False
        })
        return users


class ProjectInherit(models.Model):
    _inherit = "project.project"

    project_id = fields.Many2one('project.project', string='Project')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', string='Client', auto_join=True, tracking=True)
    project_description = fields.Char("Description")
    project_start_date = fields.Date("Project Start Date")
    project_end_date = fields.Date("Project End Date")
    notification_date = fields.Date("Notification Date")
    currency_id = fields.Many2one('res.currency', string="Currency")
    invite_user = fields.Many2many("res.users", string="Invite user")
    user_access_rights = fields.One2many('user.access.roles', 'project_ids', 'Assign Users')
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
    milestone_count = fields.Integer(compute='_compute_milestone_count', string='Milestones')

    def _compute_milestone_count(self):
        has_milestone = self.env['milestone.project'].search_count([('project_id', 'in', self.ids)])
        self.milestone_count = has_milestone

    @api.model
    def create(self, vals):
        # Prevent double project creation.
        self = self.with_context(mail_create_nosubscribe=True)
        project = super(ProjectInherit, self).create(vals)
        if not vals.get('subtask_project_id'):
            project.subtask_project_id = project.id
        if project.privacy_visibility == 'portal' and project.partner_id:
            project.message_subscribe(project.partner_id.ids)

        # Assign groups to the user everytime the project is created.
        # One user can be assigned only to one project at a time
        group_admin = self.env['res.groups'].search([('name', '=', 'Administrator')])
        for group in group_admin:
            if group.full_name == 'Project / Administrator':
                group_admin = group
                break
        group_manager = self.env['res.groups'].search([('name', '=', 'Organization Project Manager')])
        group_user = self.env['res.groups'].search([('name', '=', 'User')])
        group_viewer = self.env['res.groups'].search([('name', '=', 'Organization Project Viewer')])

        for values in vals['user_access_rights']:
            if values[2]['user_rights'] == 'Administrator':
                users = self.env['res.users'].search([('id', '=', values[2]['user'])]).id
                group_admin.write({'users': [(4, users)]})
            elif values[2]['user_rights'] == 'Organization Project Manager':
                users = self.env['res.users'].search([('id', '=', values[2]['user'])]).id
                group_manager.write({'users': [(4, users)]})
            elif values[2]['user_rights'] == 'User':
                users = self.env['res.users'].search([('id', '=', values[2]['user'])]).id
                group_user.write({'users': [(4, users)]})
            elif values[2]['user_rights'] == 'Organization Project Viewer':
                users = self.env['res.users'].search([('id', '=', values[2]['user'])]).id
                group_viewer.write({'users': [(4, users)]})
            values.pop()

        already_assign_user = ''
        for user in project.user_access_rights.user:
            proj = self.env['project.project']
            already_assign_user = proj.search([('invite_user', '=', user.id)])

        if already_assign_user != project:
            raise ValidationError(_('User is already assigned for a Project. Please select different user.'))

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

    def create_event(self):
        calendar_event = self.env['calendar.event'].create({
            'name': self.name,
            'start': self.project_start_date,
            'stop': self.project_end_date,
            'project_id': self.id
        })
        tasks = self.env['project.task'].search([('project_id', 'in', self.ids)])
        for rec in tasks:
            calendar_event = self.env['calendar.event'].create({
                'name': rec.name,
                'start': rec.date_deadline,
                'stop': rec.date_deadline,
                'project_id': self.id,
                'allday': 1,
                'description': 'Task Deadline'
            })
        milestone = self.env['milestone.project'].search([('project_id', 'in', self.ids)])
        for rec in milestone:
            calendar_event = self.env['calendar.event'].create({
                'name': rec.name,
                'start': rec.milestone_start_date,
                'stop': rec.milestone_end_date,
                'project_id': self.id,
                'allday': 1,
                'description': 'Project Milestone'
            })

    def open_tasks(self):
        # Function for creation of tasks based on the project methodology selected
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
        # Creation of Chat channel if user enables it from the project form
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
        return super(ProjectInherit, self).open_tasks()


class User_Access_Rights(models.TransientModel):
    _name = 'user.access.roles'

    project_ids = fields.Many2one('project.project', 'Project ID')
    user = fields.Many2one('res.users', 'User')
    user_rights = fields.Selection([('Administration', 'Administration'),
                                    ('Organization Project Manager', 'Organization Project Manager'),
                                    ('Organization Project Viewer', 'Organization Project Viewer'),
                                    ('Project Manager', 'Project Manager'),
                                    ('Project Viewer', 'Project Viewer'),
                                    ('User', 'User')], string='Access Rights')
