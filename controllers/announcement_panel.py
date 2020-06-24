from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class AnnouncementPanel(http.Controller):

    @http.route('/project_phases_v13/announcements', auth='user', type='json')
    def announcement_panel(self):
        company = request.env.company
        if not request.env.is_admin() or \
                company.account_invoice_onboarding_state == 'closed':
            return {}
        return {
            'html': request.env.ref('project_phase_v13.announcement_panel_template').render({
                'company': company,
                'state': company.get_and_update_account_invoice_onboarding_state()
            })
        }


