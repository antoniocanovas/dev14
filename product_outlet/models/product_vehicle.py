from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

TYPE = [
    ('gasolina', 'Gasolina'),
    ('diesel', 'Diesel'),
    ('glp', 'GLP'),
    ('electric', 'Eléctrico'),
    ('h_gasoline', 'Híbrido Gasolina'),
    ('h_gasoil', 'Híbrido Gasoil'),
]
TAX_TYPE = [
    ('rebu', 'REBU'),
    ('iva', 'IVA'),
]
GEARBOX = [
    ('manual', 'Manual'),
    ('auto', 'Automático'),
]
VEHICLE_STATE = [
    ('used', 'Usado'),
    ('new', 'Nuevo'),
    ('km0', 'Kilómetro 0'),
    ('accident', 'Accidentando'),
    ('scrap', 'Para chatarra'),
]

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    outlet = fields.Boolean('Outlet')

    vehicle_km = fields.Integer(string='KM')
    vehicle_code = fields.Char(string='Code')
    vehicle_date = fields.Date(string="Date")
    vehicle_date2 = fields.Date(string="2ª Matriculación")
    vehicle_model_id = fields.Many2one("fleet.vehicle.model", string="Model")
    vehicle_brand_id = fields.Many2one("fleet.vehicle.model.brand",
                                       related="vehicle_model_id.brand_id",
                                       string="Brand")
    vehicle_category_id = fields.Many2one("fleet.vehicle.category", string="Category")
    vehicle_id = fields.Many2one("fleet.vehicle", string="My company car")

    vehicle_energy = fields.Selection(selection=TYPE, string="Energy type")
    vehicle_gearbox = fields.Selection(selection=GEARBOX, string="Gearbox")
    vehicle_color = fields.Char(string="Color")
    vehicle_power = fields.Char(string="Power")
    vehicle_door = fields.Char(string="Doors")
    vehicle_last_itv = fields.Date(string="Last ITV")
    vehicle_next_itv = fields.Date(string="Next ITV")
    vehicle_chasis = fields.Char(string="Chasis")
    vehicle_description = fields.Text(string="Description")

    vehicle_estimation_ids = fields.One2many('product.vehicle.estimation', 'product_outlet_id', string="Estimation")
    vehicle_serie_id = fields.Many2one('fleet.vehicle.serie')
    vehicle_price = fields.Float(string="Price", store=True)
    outlet_tax_type = fields.Selection(selection=TAX_TYPE, string='Tax Type')

    vehicle_supplier_id = fields.Many2one('res.partner', string="Proveedor")
    vehicle_customer_id = fields.Many2one('res.partner', string="Comprador")
    vehicle_legal_customer_id = fields.Many2one('res.partner', string="Represent. legal")
    vehicle_use = fields.Char(string="Uso anterior")
    vehicle_state = fields.Selection(selection=VEHICLE_STATE, string="Estado")

    @api.depends('vehicle_estimation_ids')
    def get_total_estimations(self):
        for record in self:
            total = 0
            for line in record.vehicle_estimation_ids:
                if not line.invoiced:
                    total += line.amount
            record.vehicle_subtotal_estimation = total

    vehicle_subtotal_estimation = fields.Float(string="Total estimation", store=False, compute="get_total_estimations")

    def get_total_analytic(self):
        for record in self:
            total = 0
            lines = self.env['account.analytic.line'].search([(
                'account_id', 'in', [record.income_analytic_account_id.id, record.expense_analytic_account_id.id])])

            for line in lines:
                if (line.product_id.product_tmpl_id.id == record.id) and (
                        line.move_id.move_id.move_type in ['out_invoice', 'out_refund']):
                    total += 0
                else:
                    total += line.amount
            record.vehicle_subtotal_analytic = total
    vehicle_subtotal_analytic = fields.Float(string="Total Analytic", store=False, compute="get_total_analytic")

    @api.depends('vehicle_price', 'outlet_tax_type')
    def get_vehicle_rebu_iva(self):
        for record in self:
            tax, rebu_amount = 0, 0
            if (record.outlet_tax_type == 'rebu'):
                analytic = self.env['account.analytic.line'].search(
                    [('account_id', '=', record.expense_analytic_account_id.id),
                     ('move_id.move_id.move_type', '=', 'in_invoice'),
                     ('product_id.product_tmpl_id', '=', record.id)])
                if analytic:
                    for li in analytic.ids:
                        rebu_amount += analytic.amount
                else:
                    for li in record.vehicle_estimation_ids:
                        if (li.product_id.product_tmpl_id.id == record.id):
                            rebu_amount += li.amount
                if (record.vehicle_price > -rebu_amount):
                    tax = (record.vehicle_price + rebu_amount) * (1- 1/1.21)
            elif (record.outlet_tax_type != 'rebu'):
                tax = record.vehicle_price * (1- 1/1.21)
            record.vehicle_rebu_iva = -tax
    vehicle_rebu_iva = fields.Float(string="REBU/IVA (€)", store=False, compute="get_vehicle_rebu_iva")

    @api.depends('vehicle_estimation_ids', 'vehicle_price', 'outlet_tax_type')
    def get_vehicle_margin(self):
        for record in self:
            price = record.vehicle_price
            estimations = record.vehicle_subtotal_estimation
            analytics = record.vehicle_subtotal_analytic
            record.vehicle_margin = price + estimations + analytics + record.vehicle_rebu_iva
    vehicle_margin = fields.Float(string="Margin (€)", store=False, compute="get_vehicle_margin")

    def get_analytic_lines(self):
        for record in self:
            lines = self.env['account.analytic.line'].search([(
                'account_id', 'in', [record.income_analytic_account_id.id, record.expense_analytic_account_id.id])])
            record.analytic_line_ids = [(6, 0, lines.ids)]
    analytic_line_ids = fields.Many2many('account.analytic.line', store=False, readonly=True, string="Analytic",
                                         compute="get_analytic_lines")
