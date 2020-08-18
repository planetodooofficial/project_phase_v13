from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class AnnouncementPanel(http.Controller):

    @http.route('/project_phases_v13/announcements', auth='user', type='json')
    def announcement_panel(self):
        announce = request.env["announcement.panel"].sudo().search([])
        if not announce:
            return {
                'html':
                    request.env.ref('project_phases_v13.announcement_panel_template').render(
                        {'name': 'No announcements'}
            )}
        for ann in announce:
            announcements = {
                'html': request.env.ref('project_phases_v13.announcement_panel_template').render({
                    'name': ann.name
                })
            }
        return announcements
