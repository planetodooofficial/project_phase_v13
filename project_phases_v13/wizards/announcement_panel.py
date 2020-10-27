from odoo import models, fields, api, _


class AnnouncementPanel(models.TransientModel):
    _name = "announcement.panel"

    name = fields.Char("Title", required=True)
    announce_description = fields.Html("Description")
    project_id = fields.Many2one('project.project', 'Project')
    announce_start = fields.Date("Announcement Start Date")
    announce_end = fields.Date("Announcement End Date")
    announce_start_time = fields.Float(default=10.0, string='Announcement Start Time')
    announce_end_time = fields.Float(default=10.0, string='Announcement End Time')
    time_indicator = fields.Selection([
        ('am', 'AM'),
        ('pm', 'PM')], default='am', required=True, string="")
    _sql_constraints = [
        ('announce_time_range',
         'CHECK(announce_start_time >= 0 and announce_start_time <= 12)',
         'Announcement time must be between 0 and 12'),
        ('end_announce_time_range',
         'CHECK(announce_end_time >= 0 and announce_end_time <= 12)',
         'Announcement time must be between 0 and 12')
    ]

    @api.model
    def delete_announcement(self):
        announce = self.search([('announce_end', '<', fields.Date.today())])
        return announce.unlink()

    @api.model
    def announcement_action_method(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Announcements'),
            'res_model': 'announcement.panel',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
            'views': [[False, 'form']]
        }

    def announcement_save(self):
        return {'type': 'ir.actions.act_window_close'}
