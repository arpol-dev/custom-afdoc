from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    member_profile = fields.Selection([
        ('fondateur', 'Membre Fondateur'),
        ('bienfaiteur', 'Membre Bienfaiteur'),
        ('honneur', 'Membre d\'Honneur')
    ], string='Titre exceptionnel', help='[Optionnel] Définit un titre exceptionnel de membre de l\'association à un contact (prévu par les statuts de l\'association). Renseigner ce champ avec n\'importe quelle valeur implique que le contact est adhérent de l\'association sans limite dans le temps.')

    member_products = fields.Many2many('product.product', string='Produits d\'adhésion', help='Produits d\'adhésion associés à ce contact.', compute='_compute_member_products', store=True)

    @api.onchange('member_profile')
    def _onchange_membership_profile(self):
        for partner in self:
            partner.free_member = True if partner.member_profile else False

    def write(self, vals):
        if 'member_profile' in vals:
            vals['free_member'] = True if vals['member_profile'] else False
        return super(ResPartner, self).write(vals)

    @api.depends('member_lines')
    def _compute_member_products(self):
        for partner in self:
            if partner.member_lines:
                partner.member_products = partner.member_lines.filtered(lambda line: line.state in ['free', 'paid']).mapped('membership_id')
            else:
                partner.member_products = [(5, 0, 0)]