##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class PurchasePriceUpdate(models.Model):
    _inherit = "purchase.order.line"

    # Invisible icon in purchase_order_line standard_price:
    @api.depends('price_subtotal','price_unit')
    def get_price_control(self):
        control = False
        if (self.product_qty) and (self.price_subtotal / self.product_qty) == self.product_id.standard_price:
            control = True
        self.price_control = control
    price_control = fields.Boolean(string='Price Control', compute='get_price_control')

    # Invisible icon in purchase_order_line with supplierinfo:
    @api.depends('price_subtotal','price_unit')
    def get_supplierinfo_control(self):
        control = False
        supplier_price = self.env['product.supplierinfo'].search([
            ('name', '=', self.partner_id.id),
            ('product_id', '=', self.product_id.id),
            ('product_uom', '=', self.product_uom.id),
            ('min_qty', '=', 0),
        ])
        if (supplier_price.id) and (self.product_qty) and \
                (self.price_subtotal / self.product_qty) == (supplier_price.price / (1 - supplier_price.discount/100)):
            control = True
        self.price_supplierinfo_control = control
    price_supplierinfo_control = fields.Boolean(string='Supplierinfo Control', compute='get_supplierinfo_control')

    @api.depends('product_id')
    def get_standard_price(self):
        self.standard_price = self.product_id.standard_price
    standard_price = fields.Float(string='Prev. Price', store=True, compute="get_standard_price")

    def update_supplier_price(self):
        supplier_price = self.env['product.supplierinfo'].search([
            ('name','=',self.partner_id.id),
            ('product_id','=',self.product_id.id),
            ('product_uom','=',self.product_uom.id),
            ('min_qty','=',0),
        ])
        control = False
        if (supplier_price.id) and (supplier_price.price != self.price_unit):   control = True
        if (supplier_price.id) and (supplier_price.discount != self.discount):  control = True
        if (control == True):
            supplier_price.write({'price':self.price_unit, 'discount':self.discount})
        if not (supplier_price.id):
            self.env['product.supplierinfo'].create({'name':self.partner_id.id,
                                                     'product_id':self.product_id.id,
                                                     'product_uom':self.product_uom.id,
                                                     'price':self.price_unit,
                                                     'discount':self.discount,
                                                     'min_qty':0,
                                                     'product_tmpl_id':self.product_id.product_tmpl_id.id,
                                                     'delay':1})
        self.price_supplierinfo_control = True

    def update_product_standard_price(self):
        monetary_precision = self.env['decimal.precision'].sudo().search([('id', '=', 1)]).digits
        ratio = 1
        if self.product_uom.id != self.product_id.uom_id.id:
            # uom_type: bigger, reference, smaller
            if self.product_id.uom_id.uom_type == 'smaller':
                ratio = ratio / self.product_id.uom_po_id.factor
            elif self.product_id.uom_id.uom_type == 'bigger':
                ratio = ratio * self.product_id.uom_po_id.factor_inv
            if self.product_uom.uom_type == 'smaller':
                ratio = ratio * self.product_uom.factor
            elif self.product_uom.uom_type == 'bigger':
                ratio = ratio / self.product_uom.factor_inv
        new_purchase_price = round((self.price_subtotal / self.product_qty * ratio), monetary_precision)
        if new_purchase_price != self.product_id.standard_price:
            self.product_id.standard_price = new_purchase_price
        self.price_control = True

    @api.onchange('price_subtotal')
    def price_unit_wizard(self):
        message = ''
        # Purchase price_unit in SOL:
        # Unique parameter for all companies:
        monetary_precision = self.env['decimal.precision'].sudo().search([('id', '=', 1)]).digits
        if self.price_subtotal != 0 and self.product_qty != 0:
            price_unit = round(self.price_subtotal / self.product_qty, monetary_precision)
        else:
            price_unit = self.product_id.standard_price

        # CASE Different UOM in purchase_order_line and product_id:
        if self.product_uom.id != self.product_id.uom_id.id:
            ratio = 1
            # uom_type: bigger, reference, smaller
            if self.product_id.uom_id.uom_type == 'smaller': ratio = ratio / self.product_id.uom_po_id.factor
            elif self.product_id.uom_id.uom_type == 'bigger': ratio = ratio * self.product_id.uom_po_id.factor_inv
            if self.product_uom.uom_type == 'smaller': ratio = ratio * self.product_uom.factor
            elif self.product_uom.uom_type == 'bigger': ratio = ratio / self.product_uom.factor_inv
            price_unit = round(price_unit * ratio, monetary_precision)

        # Case: product_id without standard_price assigned:
        if price_unit != self.product_id.standard_price and self.standard_price == 0:
            message = 'Producto sin precio de coste asignado!' + "\n" + 'Recuerde pulsar el botón para asignar este.'

        # Case: New purchase price and standard_price assigned:
        elif price_unit != self.product_id.standard_price and self.product_id.standard_price != 0:
            message = "Precio de coste actual: " + str(round(self.standard_price, monetary_precision)) + self.product_id.uom_id.name + "\n" + \
                      "Precio de venta actual: " + str(round(self.product_id.lst_price, monetary_precision)) + "\n" + \
                      "NUEVO PRECIO DE COSTE: " + str(round(price_unit,monetary_precision)) + " " + self.product_id.uom_id.name + "\n" + \
                      " !!  Recuerde pulsar el botón para actualizar, si procede el cambio !!"

        if message != '':
            return {
                'warning': {
                    'title': 'Standard price and Price unit is not the same!',
                    'message': message,
                }
            }
