from odoo import models, fields, api
from datetime import date

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

    # merberstate compute method has flaws in the standard membership module, we redefine it here.
    @api.depends('member_lines.account_invoice_line',
                 'member_lines.account_invoice_line.move_id.state',
                 'member_lines.account_invoice_line.move_id.payment_state',
                 'member_lines.account_invoice_line.move_id.partner_id',
                 'free_member',
                 'member_lines.date_to', 'member_lines.date_from',
                 'associate_member', 'associate_member.membership_state')
    def _compute_membership_state(self):
        today = fields.Date.today()
        for partner in self:
            partner.membership_start = self.env['membership.membership_line'].search([
                ('partner', '=', partner.associate_member.id or partner.id), ('date_cancel', '=', False)
            ], limit=1, order='date_from').date_from
            partner.membership_stop = self.env['membership.membership_line'].search([
                ('partner', '=', partner.associate_member.id or partner.id), ('date_cancel', '=', False)
            ], limit=1, order='date_to desc').date_to
            partner.membership_cancel = self.env['membership.membership_line'].search([
                ('partner', '=', partner.id)
            ], limit=1, order='date_cancel').date_cancel

            if partner.associate_member:
                partner.membership_state = partner.associate_member.membership_state
                continue

            if partner.free_member and partner.membership_state != 'paid':
                partner.membership_state = 'free'
                continue

            current_mlines = partner.member_lines.filtered(lambda line: (line.date_to or date.min) >= today and (line.date_from or date.min) <= today)
            others_mlines = partner.member_lines - current_mlines
            STATE_ORDER = {
                'none': 0,
                'waiting': 1,
                'invoiced': 2,
                'canceled': 3,
                'paid': 4
            }

            if current_mlines:
                cur_state = max(
                    current_mlines.mapped('state'),
                    key=lambda s: STATE_ORDER.get(s, -1),
                ) 
                partner.membership_state = cur_state
            else:
                partner.membership_state = 'none'
            
            if (not current_mlines or cur_state not in ['free', 'paid']) and others_mlines:
                old_state = max(
                    others_mlines.mapped('state'),
                    key=lambda s: STATE_ORDER.get(s, -1),
                )
                if old_state == 'paid':
                    partner.membership_state = 'old'