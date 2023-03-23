from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WupLine(models.Model):
    _name = 'wup.line'
    _description = 'WUP Line'

    product_id = fields.Many2one('product.product', string='Product')
    product_uom_qty = fields.Float(string='Quantity')
    product_uom = fields.Many2one('uom.uom', string='Unit', related='product_id.uom_id')
    currency_id = fields.Many2one('res.currency')
    sale_line_id = fields.Many2one('sale.order.line', string='SO Line')
    sale_id = fields.Many2one('sale.order', related='sale_line_id.order_id', string='Sale')
    sale_discount = fields.Float('Disc.(%)', related='sale_line_id.discount', store=False)
    task_id = fields.Many2one('project.task', string='WU Task')
    effective_hours = fields.Float(string="Eff. Hours", related='task_id.effective_hours', store=False)
    #Modificado 09/09/2022 por formato de impresión sin respetar formato, puede hacerse calculado para pasar a char.
    sale_line_name = fields.Text(string='Sale line', related='sale_line_id.name')

    service_tracking = fields.Selection('Service tracking', store=False, related='product_id.service_tracking')
    state = fields.Selection('State', store=True, related='sale_line_id.state')

    @api.depends('sale_line_id.product_uom_qty', 'product_uom_qty')
    def get_wup_product_sale_qty(self):
        for record in self:
            record.product_sale_qty = record.product_uom_qty * record.sale_line_id.product_uom_qty
    product_sale_qty = fields.Float(string='Sale Qty', compute='get_wup_product_sale_qty')

    # Set default name from product_id:
    @api.depends('product_id')
    def get_product_id_name(self):
        for record in self:
            record.name = record.product_id.name
    name = fields.Char(string='Description', readonly=False, store=True, compute='get_product_id_name')

    # Set wup_line subtotal main form, not in window action o2m wup_lines (replaced by subtotal_sale):
    @api.depends('price_unit', 'product_uom_qty')
    def get_subtotal(self):
        for record in self:
            record.subtotal = record.price_unit * record.product_uom_qty

    subtotal = fields.Monetary('Subtotal', currency_field='currency_id', compute="get_subtotal",  store=True )

    # Set lst_price now, from product_id as readonly to estimate discounts:
    @api.depends('product_id')
    def get_lst_price(self):
        for record in self:
            record.lst_price = record.product_id.lst_price

    lst_price = fields.Monetary('List Price', currency_field='currency_id', compute="get_lst_price", store=True)

    # Get discount from standar lst_price:
    @api.depends('product_id', 'price_unit')
    def get_lst_price_discount(self):
        for record in self:
            discount = 0
            if (record.lst_price > 0) and (record.price_unit < record.lst_price):
                discount = (1 - (record.price_unit / record.lst_price)) * 100
            record['lst_price_discount'] = discount

    lst_price_discount = fields.Monetary('List price discount %', currency_field='currency_id',
                                         store=False, compute="get_lst_price_discount")

    # Get default cost from product_id on creation:
    @api.depends('product_id')
    def get_price_unit_cost(self):
        for record in self:
            record.price_unit_cost = record.product_id.standard_price

    price_unit_cost = fields.Monetary('Unit Cost', currency_field='currency_id',
                                      readonly=False, store=True, compute="get_price_unit_cost")

    # Get subtotal cost:
    @api.depends('product_id','product_uom_qty')
    def get_wupline_cost(self):
        for record in self:
            record.price_cost = record.price_unit_cost * record.product_uom_qty

    price_cost = fields.Monetary('Cost', currency_field='currency_id',
                                      readonly=False, store=True, compute="get_wupline_cost")

    # Get standard lst_price from product_id as NO READONLY:
    @api.depends('product_id')
    def get_price_unit(self):
        for record in self:
            record.price_unit = record.product_id.lst_price

    price_unit = fields.Monetary('Price Unit', currency_field='currency_id',
                                 store=True, readonly=False, compute="get_price_unit")

    # Get SALE Sutotal line, para mostrar y totalizar sólo en Acción de ventana o2m WUP_LINES::
    @api.depends('sale_line_id.discount', 'sale_line_id.product_uom_qty', 'subtotal')
    def get_subtotal_sale(self):
        for record in self:
            total = record.subtotal * record.sale_line_id.product_uom_qty * (1 - record.sale_line_id.discount/100)
            record.subtotal_sale = total

    subtotal_sale = fields.Monetary('Sale subtotal', currency_field='currency_id',
                                 store=True, readonly=True, compute="get_subtotal_sale")

    # Recalcular wup si se borran líneas o modifican las actuales:
#    @api.onchange('price_unit','price_unit_cost','product_uom_qty', 'sale_line_id.wup_line_ids')
    @api.onchange('price_unit','price_unit_cost','product_uom_qty')
    def update_sol_prices_from_wup(self):
        for record in self:
            sol_price_unit, sol_purchase_price = 0,0
            sol = record.sale_line_id
            for li in sol.wup_line_ids:
                sol_price_unit += li.product_uom_qty * li.price_unit
                sol_purchase_price += li.product_uom_qty * li.price_unit_cost
            sol.write({'price_unit':sol_price_unit, 'purchase_price':sol_purchase_price})
