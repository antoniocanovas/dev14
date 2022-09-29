# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order',

    active = fields.Boolean('Active', store=True, default=True)
    all_revision_ids = fields.Many2many(comodel_name='sale.order',
                                        string="Revisions",
                                        relation='so_sorevision_rel',
                                        column1="so",
                                        column2="sorevision",
#                                        compute="get_all_revisions",
                                        store=True,
                                        context={'active_test': False}
                                        )
    all_revision_count = fields.Integer(string="Revisions",
                                        compute="get_all_revisions_count",
                                        store=False
                                        )
    all_mail_messages = fields.Many2many('mail.message',
                                         string="Messages",
                                         compute="get_all_messages",
                                         store=False
                                         )
#    revision0_id = fields.Many2one('sale.order', 'Original')
#    revision0_ids = fields.One2may('sale.order', 'revision0_id', string="Revs. Original")
#    revisionx_ids = fields.Many2many('sale.order', related='revision0_id.revision0_ids', store=False)


#    def get_all_revisions(self):
#        if self.id:
#            unrevision_name = self.name.split(".")[0]
#            revision = self.env['sale.order'].search([('name', 'ilike', unrevision_name),
#                                                  ('active','in',[True,False])])
#            self.all_revision_ids = [(6, 0, revision.ids)]

    def get_all_revisions_count(self):
        self.all_revision_count = len(self.all_revision_ids.ids)

    def get_all_messages(self):
        messages = self.env['mail.message'].search([('model', '=', 'sale.order'),
                                                    ('res_id', 'in', self.all_revision_ids.ids)])
        self.all_mail_messages = [(6, 0, messages.ids)]

    def get_new_sale_order_revision(self):
        for record in self:
            original = record.name.split(".")[0]
            version = 0
            #v0 = self.env['sale.order'].search([('name','=', original),('active','in',[True,False])])
            saleorders = self.env['sale.order'].search([('name', 'ilike', original)])

            for so in saleorders:
                name_version = so.name.split(".")
                if (len(name_version) > 1) and (int(name_version[1]) > version):
                    version = int(name_version[1])
            if (version + 1 < 10):
                versionchar = ".0" + str(version + 1)
            else:
                versionchar = "." + str(version + 1)
            new = record.copy({'name': original + versionchar})

#            for so in saleorders:
#                so['all_revision_ids'] = [(4,0,new.id)]

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