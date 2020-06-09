from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    industry_type = fields.Selection([
        ("agriculture", "Agriculture"), ("architecture", "Architecture"),
        ("construction", "Construction & Real Estate"), ("consult", "Consulting"), ("creative", "Creative"),
        ("education", "Education & Non-profit"), ("finance", "Finance"), ("insurance", "Insurance"),
        ("legal", "Legal Services"), ("manufacture", "Manufacturing"),
        ("media", "Media"), ("retail", "Retail")
    ], string="Industry")
