# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order',

    active = fields.Boolean('Active', store=True, default=True)
    revision_ids = fields.Many2many(comodel_name='sale.order',
                                    string="Revisions",
                                    relation='so_sorevision_rel',
                                    column1="so",
                                    column2="sorevision",
                                    store=True,
                                    context={'active_test': False}
                                    )
    revision_count = fields.Integer(string="Revisions",
                                    compute="get_revisions_count",
                                    store=False
                                    )
    revision_messages = fields.Many2many('mail.message',
                                         string="Messages",
                                         compute="get_revision_messages",
                                         store=False
                                         )

    def get_revisions_count(self):
        self.revision_count = len(self.revision_ids.ids)

    def get_revision_messages(self):
        messages = self.env['mail.message'].search([('model', '=', 'sale.order'),
                                                    ('res_id', 'in', self.revision_ids.ids)])
        self.revision_messages = [(6, 0, messages.ids)]

    def get_new_sale_order_revision(self):
        for record in self:
            version = 0
            original = record.name.split(".")[0]

            # Looking for last revision code, and create new revision with code +1:
            saleorders = self.env['sale.order'].search([('name', 'ilike', original),
                                                        ('active','in',[False,True])])
            for so in saleorders:
                name_version = so.name.split(".")
                if (len(name_version) > 1) and (int(name_version[1]) > version):
                    version = int(name_version[1])
            if (version + 1 < 10):
                versionchar = ".0" + str(version + 1)
            else:
                versionchar = "." + str(version + 1)
            new = record.copy({'name': original + versionchar})

            # Updating revision_ids in related sales orders:
            saleorders = self.env['sale.order'].search([('name', 'ilike', original),
                                                        ('active','in',[False,True])])
            for so in saleorders:
                so.write({'revision_ids':[(6,0,saleorders.ids)]})

            # Refresh screen with new revision:
            view_id = self.env.ref('sale.view_order_form').id
            return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sale.order',
                'type': 'ir.actions.act_window',
                'view_id': view_id,
                'context': dict(self.env.context),
                'target': 'current',
                'res_id': new.id,
            }