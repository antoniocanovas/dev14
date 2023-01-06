from odoo import _, api, fields, models
from datetime import date
from time import sleep

class ScrapUnbuildWizard(models.TransientModel):
    _name = 'scrap.unbuild.wizard'
    _description = 'Scrap Unbuild Wizard'

    @api.depends('product_tmpl_id', 'unbuild_set_id', 'create_date')
    def get_unbuild_wizard_name(self):
        name = str(date.today())
        if self.product_tmpl_id.id: name += " " + self.product_tmpl_id.name
        if self.unbuild_set_id.id: name += " " + self.unbuild_set_id.name
        self.name = name
    name = fields.Char('Name', compute='get_unbuild_wizard_name', readonly=False)

    product_tmpl_id = fields.Many2one('product.template', string='Product')
    unbuild_set_id = fields.Many2one('unbuild.set', string='SET')
    inventory_id = fields.Many2one('stock.inventory', string='Inventory', readonly=True)
    autovalidate = fields.Boolean('Autovalidate')
    line_ids = fields.One2many('unbuild.product.line.wizard', 'unbuild_wizard_id', string='Parts')


    # Crea la creación de productos, inventariado y valoración en la ubicación del producto padre:
    def get_scrap_unbuild_action(self):
        rootcode = self.product_tmpl_id.default_code[:6]
        location = self.env['stock.location'].search([('name', '=', rootcode)])
        rootpt = self.env['product.template'].search([('default_code', '=', rootcode)])
        if not rootpt.id or not location.id:
            raise Warning(
                'Revisa los códigos de los productos padre anidados, no encuentro el raiz con los 6 primeros dígitos; o la localizacón de almacén con este código.')

        # STOCK INVENTORY Creation:
        units = 0
        for li in self.line_ids: units += li.qty
        if units > 0:
            name = self.name + " " + rootpt.default_code
            newsi = self.env['stock.inventory'].create({'name': name, 'unbuild_product_tmpl_id': self.product_tmpl_id.id})
        else:
            raise Warning('No hay productos nuevos que crear en: ' + self.name)

        # NEW PRODUCTS AND STOCK INVENTORY LINES CREATION:
        for li in self.line_ids:
            codesub = str(rootpt.unbuild_sequence + 1001)[-3:]

            # PARA NUEVOS PRODUCTOS:
            if (li.qty > 0) and not (li.part_id.product_id.id):
                newproduct = self.env['product.template'].create({'name': li.name,
                                                             'categ_id': li.part_id.category_id.id,
                                                             'unbuild_type': 'subproduct',
                                                             'sale_ok': True, 'purchase_ok': False, 'type': 'product',
                                                             'parent_id': rootpt.id, 'default_code': rootcode + codesub,
                                                             'income_analytic_account_id': rootpt.income_analytic_account_id.id,
                                                             'expense_analytic_account_id': rootpt.expense_analytic_account_id.id,
                                                             'unbuild_location_id': rootpt.unbuild_location_id.id,
                                                             'standard_price': li.standard_price})
                rootpt['unbuild_sequence'] = rootpt.unbuild_sequence + 1
                newproductproduct = self.env['product.product'].search([('product_tmpl_id', '=', newproduct.id)])

                newsil = self.env['stock.inventory.line'].create(
                    {'inventory_id': newsi.id, 'location_id': location.id, 'product_id': newproductproduct.id,
                    'product_qty': li.qty, 'unbuild_unit_value': li.standard_price})

            # PARA PRODUCTOS GENÉRICOS:
            elif (li.qty > 0) and (li.part_id.product_id.id):
                qty = li.qty
                sq = self.env['stock.quant'].search(
                    [('product_id', '=', li.part_id.product_id.id), ('location_id', '=', location.id)])
                if sq.id: qty += sq.quantity
                newsil = self.env['stock.inventory.line'].create(
                    {'inventory_id': newsi.id, 'location_id': location.id, 'product_id': li.part_id.product_id.id,
                     'product_qty': qty, 'unbuild_unit_value': li.standard_price})

        # Iniciar y validar si procede el registro stock.inventory:
        newsi.action_start()
        if (self.autovalidate == True):
            sleep(2)
            newsi.action_validate()


