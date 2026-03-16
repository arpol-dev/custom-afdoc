from odoo import models, fields, api

class MassMailing(models.Model):
    _inherit = 'mailing.mailing'

    company_id = fields.Many2one(default=lambda self: self.env.user.company_id if self.env.user.company_id else None)

    @api.depends('reply_to_mode')
    def _compute_reply_to(self):
        for mailing in self:
            if mailing.reply_to_mode == 'new' and not mailing.reply_to:
                mailing.reply_to = self.env.user.company_id.email_formatted
            elif mailing.reply_to_mode == 'update':
                mailing.reply_to = False