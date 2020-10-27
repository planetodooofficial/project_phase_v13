from odoo import models, fields, api
import logging
import base64
_logger = logging.getLogger(__name__)


class TimesheetTracker(models.Model):
    _name = "timesheet.tracker"

    name = fields.Char(default=fields.Datetime.now)
    screenshot_ids = fields.One2many("account.analytic.line", "screenshot_id", string="Screenshots")
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', 'Task')
    user_id = fields.Many2one("res.users", string="Assigned user", related='task_id.user_id', store=True)
    clicks = fields.Integer("Mouse Clicks")
    keypress = fields.Integer("Key presses")
    notes = fields.Char("Notes")
    screenshot = fields.Image("Screenshot")
    company_id = fields.Many2one("res.company", string='Company')
    employee_id = fields.Many2one('hr.employee', string='Team')

    @api.model
    def capture_screenshot(self, project_id, task_id, clicks, keypress, notes, image):
        for rec in project_id:
            employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id
            for task in task_id:
                if rec == self.env['project.task'].browse(task).project_id.id:
                    screenshots_create = self.env['timesheet.tracker'].sudo().create({
                        'project_id': rec,
                        'task_id': task,
                        'clicks': clicks,
                        'keypress': keypress,
                        'notes': notes,
                        'screenshot': image,
                        'employee_id': employee
                    })
        return True

    @api.model
    def company_details(self):
        _logger.error("Logger Starts", self.env.user.id)
        com_name = []
        user_settings = []
        users_company = self.env['res.users'].search([('id', '=', self.env.user.id)])
        a = users_company.company_ids
        for company in a:
            company_id = self.env['res.company'].search([('id', '=', company.id)])
            encoded_string = base64.b64encode(company_id.logo)
            com_name.append({
                'id': company_id.id,
                'name': company_id.name,
                'logo_image': encoded_string,
                'without_encoded_logo': company_id.logo,
                'user_id': users_company.id,
                'screenshot_limit_per_hour': users_company.screenshot_limit_per_hour,
                'activity_level_tracking': users_company.activity_level_tracking,
                'app_url_tracking': users_company.app_url_tracking,
                'weekly_time_limit': users_company.weekly_time_limit,
                'auto_pause_time': users_company.auto_pause_time,
                'notification_for_screenshot': users_company.notification_for_screenshot,
                'allow_screenshots': users_company.allow_screenshots,
                'allow__deletion_screenshots': users_company.allow__deletion_screenshots
            })
        return com_name
