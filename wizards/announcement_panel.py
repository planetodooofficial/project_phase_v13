from odoo import models, fields, api, _


class AnnouncementPanel(models.TransientModel):
    _name = "announcement.panel"

    announce_title = fields.Char("Title")
    announce_description = fields.Html("Description")
    project_id = fields.Many2one('project.project', 'Project')
    announce_start = fields.Datetime("Announcement Start Date/Time")
    announce_end = fields.Datetime("Announcement End Date/Time")

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
