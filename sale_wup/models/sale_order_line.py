from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WupSaleOrder(models.Model):
    _inherit = 'sale.order'

    wup_line_ids = fields.One2many('wup.line','sale_id', string='wup')

    def _get_wup_line_count(self):
        results = self.env['wup.line'].search([
            ('sale_id', '=', self.id), ]
        )
        self.wup_line_count = len(results)

    wup_line_count = fields.Integer('wups', compute=_get_wup_line_count)

    def action_view_wup_line(self):
        action = self.env.ref(
            'sale_wup.action_view_wups').read()[0]
        return action


class WupSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    name = fields.Char(string='Name')
    wup_template_id = fields.Many2one('wup.template', string='wup Template', copy=True)
    wup_line_ids = fields.One2many('wup.line', 'sale_line_id', string='wup Line', copy=True)

    def get_wup_cost_amount(self):
        for record in self:
            cost = 0
            for line in record.wup_line_ids:
                cost += line.price_unit_cost * line.product_uom_qty
            record.wup_cost_amount = cost

    wup_cost_amount = fields.Monetary('wup Cost', store=False, compute='get_wup_cost_amount')

    @api.depends('product_id', 'product_uom', 'discount', 'price_unit')
    def get_lst_price(self):
        for record in self:
            lst_price = 0
            if record.product_uom.uom_type == 'reference':
                lst_price = record.product_id.lst_price
            elif record.product_uom.uom_type == 'bigger':
                lst_price = record.product_id.lst_price * record.product_uom.factor_inv
            elif record.product_uom.uom_type == 'smaller':
                lst_price = record.product_id.standard_price / record.product_uom.factor
            record['lst_price'] = lst_price

    lst_price = fields.Monetary('List Price', currency_field='currency_id', compute="get_lst_price",  store=True)

    @api.depends('product_uom_qty', 'product_id')
    def get_lst_price_discount(self):
        for record in self:
            discount = 0
            if (record.product_uom_qty > 0) and (record.lst_price > 0):
                if (record.price_unit < record.lst_price):
                    discount = (1 - (record.price_unit / record.lst_price)) * 100
            record['lst_price_discount'] = discount

    lst_price_discount = fields.Float('List price discount %', currency_field='currency_id',
                                         store=False, compute="get_lst_price_discount")

    @api.depends('product_id')
    def get_price_unit_cost(self):
        for record in self:
            puc = 0
            if record.product_uom.uom_type == 'reference':
                puc = record.product_id.standard_price
            elif record.product_uom.uom_type == 'bigger':
                puc = record.product_id.standard_price * record.product_uom.factor_inv
            elif record.product_uom.uom_type == 'smaller':
                puc = record.product_id.standard_price / record.product_uom.factor
            record['price_unit_cost'] = puc
    price_unit_cost = fields.Monetary('Cost Price', currency_field='currency_id', store=False, compute="get_price_unit_cost")

    @api.depends('product_id')
    def get_wup_cost_amount(self):
        for record in self:
            wup_cost = 0
            for li in record.wup_line_ids:
                wup_cost += li.price_unit_cost * li.product_uom_qty
            record['wup_cost_amount'] = wup_cost

    wup_cost_amount = fields.Monetary('Cost amount', currency_field='currency_id', store=False,
                                      compute="get_wup_cost_amount")

    wup_qty = fields.Integer('wup Qty', copy=True)

    def action_open_sol(self):
        return {
            'name': _('SOL'),
            'view_type': 'tree',
            'view_mode': 'form',
            'res_model': 'sale.order.line',
            'type': 'ir.actions.act_window',
            'view_id':
                self.env.ref('sale_wup.sale_order_line_wup_form').id,
            'context': dict(self.env.context),
            'target': 'new',
            'res_id': self.id,
        }

    @api.depends('product_uom_qty')
    def get_updated_price_unit_if_wup(self):
        for record in self:
            if record.wup_line_ids.ids:
                price_unit, subtotal, discount, cost = 0, 0, 0, 0
                for li in record.wup_line_ids:
                    subtotal += li.price_unit * record.product_uom_qty
                if record.product_uom_qty != 0:
                    record.write({'price_unit': subtotal / record.product_uom_qty, 'discount': 0})
