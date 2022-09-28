# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order',

    active = fields.Boolean('Active', store=True, default=True)
    revision0_id = fields.Many2one('sale.order', string='First quotation', store=True)
    revision_ids = fields.One2many('sale.order', 'revision0_id', string="Revisions")
    revision_count =  fields.Integer(string="Revisions",
                                        compute="get_revision_count",
                                        store=False
                                        )

    all_mail_messages = fields.Many2many('mail.message',
                                         string="Messages",
                                         compute="get_all_messages",
                                         store=False
                                         )

    def get_revision_count(self):
        self.revision_count = len(self.revision_ids.ids)

    def get_all_messages(self):
        messages = self.env['mail.message'].search([('model', '=', 'sale.order'),
                                                    ('res_id', 'in', self.revision_ids.ids)])
        self.all_mail_messages = [(6, 0, messages.ids)]

    def get_new_sale_order_revision(self):
        for r in self:
            if r.revision0_id == False:
                r['revision0_id'] = r.id
            version = 1
            for so in r.revision_ids:
                version_name = so.name.split(".")
                if (len(version_name) > 1) and (int(version_name[1]) > version):
                    version = int(version_name[1])
            if (version + 1 < 10):
                versionchar = ".0" + str(version + 1)
            else:
                versionchar = "." + str(version + 1)
            r.copy({'name': r.revision0_id.name + versionchar})