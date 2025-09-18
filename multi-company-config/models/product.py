from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    company_id = fields.Many2one(default=lambda self: self.env.company.ids[0] if self.env.company else False)
    