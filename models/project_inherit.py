from odoo import models, api, _, fields


class ProjectInherit(models.Model):
    _inherit = "project.project"

    partner_id = fields.Many2one('res.partner', string='Client', auto_join=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    project_description = fields.Char("Description")
    invite_user = fields.Char("Invite User")
    project_start_date = fields.Date("Project Start Date")
    project_end_date = fields.Date("Project End Date")
    notification_date = fields.Date("Notification Date")
    project_budget = fields.Selection([("fixed", "Fixed Budget"),
                                       ("weekly", "Weekly Budget"),
                                       ("custom", "Custom Budget")])
    fixed_budget = fields.Monetary("Total Budget")
    weekly_budget = fields.Monetary("Weekly Budget")
    custom_price = fields.Monetary("Price per hour")
    custom_hours = fields.Integer("Hours")
    custom_minutes = fields.Integer("Minutes")
    methodology = fields.Char("Methodology")

    def open_tasks(self):
        active_id = self.env["project.dashboard"].browse(self.env.context.get('active_ids'))
        self.methodology = dict(active_id._fields['method_name'].selection).get(active_id.method_name)
        stage_obj = self.env["project.task.type"].search([('method_name', '=', self.methodology)])
        if active_id.method_name == 'agile':
            if stage_obj:
                for rec in stage_obj:
                    vals = {
                        'project_ids': [(4, self.ids)]
                    }
                    rec.write(vals)
            else:
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
