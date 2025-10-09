from odoo import models, fields, api
from random import randint


class ResPartner(models.Model):
    _inherit = 'res.partner'

    mandat_ids = fields.Many2many('res.partner.mandat', string='Mandats')

class ResPartnerMandat(models.Model):
    _name = 'res.partner.mandat'
    _description = 'Mandat du partenaire'

    def _get_default_color(self):
            return randint(1, 11)
    
    name = fields.Char('Nom du mandat', required=True)
    description = fields.Text('Description')
    color = fields.Integer(string='Color', default=_get_default_color)
