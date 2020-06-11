from odoo import api, fields, models, _


class MailChannelInherit(models.Model):
    _inherit = "mail.channel"
