from odoo import models, fields, api


class Time_Tracker_Settings(models.Model):
    _inherit = 'res.users'

    screenshot_limit_per_minutes = fields.Selection([('5', '5'), ('10', '10'), ('15', '15')], string='Screenshot Limit (Per Minute)')
    activity_level_tracking = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Activity Level Tracking')
    app_url_tracking = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='App & Url Tracking')
    weekly_time_limit = fields.Integer('Weekly Time Limit (Hours)')
    auto_pause_time = fields.Selection([('5', '5'), ('10', '10'), ('15', '15')], string='Auto-pause tracking after')
    notification_for_screenshot = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Notify when screenshot is '
                                                                                          'taken')
    allow_screenshots = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Allow Screenshots')
    allow__deletion_screenshots = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Allow Deletion of '
                                                                                          'Screenshots')
