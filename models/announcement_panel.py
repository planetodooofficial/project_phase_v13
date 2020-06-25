from odoo import models, fields


class AnnouncementPanel(models.Model):
    _name = "announcement.panel"

    announce_title = fields.Char("Title")
    announce_description = fields.Char("Description")
    project_id = fields.Many2one('project.project', 'Project')

    def announcement_action(self, action_ref=None):
        if not action_ref:
            action_ref = 'project_phases_v13.announcement_action'
        return self.env.ref(action_ref).read()[0]

    def announcement_save(self):
        return {'type': 'ir.actions.act_window_close'}
