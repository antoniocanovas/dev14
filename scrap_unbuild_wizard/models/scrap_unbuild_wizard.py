from odoo import _, api, fields, models

TYPE = [
    ('services', 'Final price applying discounts on services'),
    ('discount', 'Discount'),
]


class ScrapUnbuildWizard(models.TransientModel):
    _name = 'scrap.unbuild.wizard'
    _description = 'Scrap Unbuild Wizard'

#VOY POR AQUÍ:

    #Campos con duda
    name = fields.Char('Name')
    #Campos
    discount = fields.Float('Discount')
    childs = fields.Boolean('Childs')
    products = fields.Boolean('Products')
    services = fields.Boolean('Services')
    all_quotation = fields.Boolean('All Quotation')
    price = fields.Float('Price')
    sale_id = fields.Many2one('sale.order')
    type = fields.Selection(selection=TYPE, string="Type")
    section_id = fields.Many2one('sale.order.line', string='Section')



