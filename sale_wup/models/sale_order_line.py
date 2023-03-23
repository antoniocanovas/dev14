from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class WupSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    wup_template_id = fields.Many2one('wup.template', string='wup Template', copy=True)
    wup_line_ids = fields.One2many('wup.line', 'sale_line_id', string='wup Line', copy=True)
    wup_line_note_id = fields.Many2one('sale.order.line')

    @api.depends('wup_line_ids','wup_line_ids.product_uom_qty','wup_line_ids.price_unit_cost')
    def get_wup_cost_amount(self):
        for record in self:
            cost = 0
            for line in record.wup_line_ids:
                cost += line.price_unit_cost * line.product_uom_qty
            record.wup_cost_amount = cost

    wup_cost_amount = fields.Monetary('wup Cost', store=True, compute='get_wup_cost_amount')

    @api.depends('product_uom_qty','wup_cost_amount', 'wup_price_unit')
    def update_sol_price_unit(self):
        for record in self:
            # Change default behaviour when change QYT on SOL with WUP, and update purchase_price on SOL:
            if record.wup_line_ids.ids:
                wup_price, wup_cost_amount = 0, 0
                for li in record.wup_line_ids:
                    wup_price += li.price_unit * li.product_uom_qty
                    wup_cost_amount += li.price_unit_cost * li.product_uom_qty

                if not (record.wup_line_note_id.id) and (record.wup_template_id.id) and (record.wup_template_id.description):
                    # Create a line note from wup template description:
                    new_note = env['sale.order.line'].create(
                        {'sequence': record.sequence, 'name': record.wup_template_id.description, 'display_type': 'line_note',
                         'order_id': record.order_id.id})
                    record.write({'price_unit': wup_price, 'purchase_price': wup_cost_amount,
                                  'wup_line_note_id': new_note.id})
                else:
                    record.write({'price_unit': wup_price, 'purchase_price': wup_cost_amount})




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

    def wup_lines_from_wup_template(self):
        for record in self:
            price_unit = 0
            if record.wup_qty > 0:
                for li in record.wup_template_id.line_ids:
                    newline = self.env['wup.line'].create(
                        {'sale_line_id': record.id, 'product_id': li.product_id.id, 'name': li.name,
                         'product_uom_qty': li.product_uom_qty * record.wup_qty, 'product_uom': li.product_uom,
                         'price_unit_cost': li.product_id.standard_price, 'lst_price': li.product_id.lst_price,
                         'price_unit': (1 - record.discount / 100) * li.product_id.list_price
                         })
                    price_unit += newline.product_uom_qty * newline.price_unit
                record['price_unit'] = price_unit
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