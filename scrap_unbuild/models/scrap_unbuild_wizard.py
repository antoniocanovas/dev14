from odoo import _, api, fields, models

class ScrapUnbuildWizard(models.TransientModel):
    _name = 'scrap.unbuild.wizard'
    _description = 'Scrap Unbuild Wizard'

    @api.depends('product_tmpl_id', 'unbuild_set_id', 'create_date')
    def get_unbuild_wizard_name(self):
        name = str(datetime.date.now())
        if self.product_tmpl_id.id: name += " " + self.product_tmpl_id.name
        if self.unbuild_set_id.id: name += " " + self.unbuild_set_id.name
        self.name = name

    name = fields.Char('Name', compute='get_unbuild_wizard_name', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product')
    unbuild_set_id = fields.Many2one('unbuild.set', string='SET')
    inventory_id = fields.Many2one('stock.inventory', string='Inventory', readonly=True)
    line_ids = fields.One2many('unbuild.product.line.wizard', 'unbuild_wizard_id', string='Parts')
