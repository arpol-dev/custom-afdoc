from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_id = fields.Many2one(default=lambda self: self.env.company.ids[0] if self.env.company else None)

class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    company_id = fields.Many2one('res.company', 'Company', index=True, default=lambda self: self.env.company.ids[0] if self.env.company else None)