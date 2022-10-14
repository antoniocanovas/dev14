# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# imports of python lib
from datetime import datetime, date
from re import search
from dateutil.relativedelta import relativedelta
# imports of odoo lib
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DT
import pytz




class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('preparing', 'Preparing'),
                                            ('ready', 'Ready to Pickup'),
                                            ('delivered', 'Delivered'),
                                            ('payment', 'Payment')],
                             string='Status', readonly=True, copy=False,
                             index=True, track_visibility='onchange',
                             track_sequence=3, default='draft'
                             )
    invoice_payment_status = fields.Selection([
                            ('not_paid', 'Not Paid'),
                            ('paid', 'Paid')],default="not_paid")

    @api.depends('state')
    def _compute_type_name(self):
        """ Update the type name based on the state """
        for record in self:
            record.type_name = _('Quotation') if record.state in ('draft', 'sent', 'cancel') else _('Sales Order')

    @api.depends('date_order', 'order_line', 'state', 'partner_id')
    def _compute_abandoned_cart(self):
        # a quotation can be considered as an abandonned cart if it is linked to a website,
        # is in the 'draft' state and has an expiration date
        for orderval in self:
            abandoned_delay = orderval.website_id and orderval.website_id.cart_abandoned_delay or 1.0
            abandoned_datetime = datetime.utcnow() - relativedelta(hours=abandoned_delay)
            for order in self:
                domain = order.date_order <= abandoned_datetime and order.state == 'draft' and order.partner_id.id != self.env.ref('base.public_partner').id and order.order_line
                order.is_abandoned_cart = bool(domain)

    def check_fields_to_send(self, vals):
        """ For checking the fields that updated to sale order """
        fields = self.env["ir.config_parameter"].sudo().get_param("pos_sale_sync.sale_sync_field_ids", default=False)
        if not fields:
            return False
        field_names = self.env['ir.model.fields'].browse([int(x) for x in fields.split(',')]).mapped('name')
        for name in field_names:
            if name in vals:
                return True
        return False

    def write(self, vals):
        """ Check the state value if the state value is cancel then unlink the order """ 
        result = super(SaleOrder, self).write(vals)
        if self.check_fields_to_send(vals):
            if (self.state == 'cancel'):
                self.send_field_updates(self.ids, action='unlink')
            else:
                self.send_field_updates(self.ids)
        return result

    @api.model
    def create(self, vals):
        """ Create the value in sale order """
        partner = super(SaleOrder, self).create(vals)
        if self.check_fields_to_send(vals):
            self.send_field_updates([partner.id])
        return partner

    def unlink(self):
        """ Unlink the record """ 
        res = super(SaleOrder, self).unlink()
        self.send_field_updates(self.ids, action='unlink')
        return res

    @api.model
    def send_field_updates(self, order_ids, action=''):
        """ Send the value for createa nd unlik the record """
        channel_name = "pos_sale_sync"
        data = {'message': 'update_sorder_fields', 'action': action,
                'order_ids': order_ids}
        self.env['pos.config'].send_to_all_poses(channel_name, data)

    def change_order_state(self, order_id, order_state):
        """ Change the sale order status based on the state in the pos order """
        sale_order = self.env['sale.order'].sudo().search([
            ('id', '=', int(order_id))])
        ostate = (order_state).strip()
        if ostate == _("Order Confirm"):
            sale_order.action_confirm()
            for line in sale_order.order_line:
                line.qty_delivered = line.product_uom_qty
            sale_order._create_invoices()
            for invoice in sale_order.invoice_ids:
            #     account = self.env['account.account'].sudo().search([
            #                 ('company_id', '=', sale_order.company_id.id),
            #                 ('internal_type', '=', 'receivable'),
            #                 ('deprecated', '=', False)], limit=1)
            #     for line in invoice.line_ids:
            #         #line.write({'account_id': account.id})
            #         line.account_id = account.id
                invoice._post()
            return True
        elif ostate == _("Preparing"):
            sale_order.write({'state': 'preparing'})
            return True
        elif ostate == _("Ready to Pickup"):
            sale_order.write({'state': 'ready'})
            return True
        elif ostate == _("Delivered"):
            sale_order.write({'state': 'delivered'})
            for picking in sale_order.picking_ids:
                if(picking.state != "cancel"):
                    for smove in picking.move_ids_without_package:
                        smove.write({'quantity_done': smove.product_uom_qty})
                    picking.button_validate()
            for invoice in sale_order.invoice_ids:
                if invoice.state == 'paid':
                    sale_order.write({'state': 'payment'})
            return True
        else:
            sale_order.write({'state': 'payment'})
            return True

    def change_sorder_line_state(self, oline_id, order_id, order_state):
        """ Update State in Order line"""
        print(order_id)
        order_line = self.env['sale.order.line'].sudo().search([
                        ('id', '=', int(oline_id))])
        if order_line:
            order_line.write({'kitchen_state': order_state})

        sale_order = self.env['sale.order'].sudo().search([
                        ('id', '=', int(order_id))])
        print(sale_order)
        if sale_order:
            # Update state based on order line state
            self.update_order_state(sale_order)

    def update_order_state(self, sale_order):
        """ Update state in sale order"""
        # Check when order in draft and sent state
        if sale_order and sale_order.state in ['draft', 'sent']:
            is_lines_confirmed = True
            for line in sale_order.order_line:
                if line.kitchen_state == 'open' or line.kitchen_state == 'cancel':
                    is_lines_confirmed = False
                    break
            if is_lines_confirmed:
                self.change_order_state(sale_order.id, 'Order Confirm')
        # Check when order in sale - confirm 
        elif sale_order and sale_order.state == 'sale':
            for line in sale_order.order_line:
                if line.kitchen_state == 'preparing':
                    self.change_order_state(sale_order.id, 'Preparing')
                    break
        # Check when order in preparing -
        elif sale_order and sale_order.state == 'preparing':
            is_order_ready = True
            for line in sale_order.order_line:
                # Check all line is ready
                if line.kitchen_state != 'ready':
                    is_order_ready = False
                    break
            if is_order_ready:
                self.change_order_state(sale_order.id, 'Ready to Pickup')
        # Check when order in ready -
        elif sale_order and sale_order.state == 'ready':
            is_order_delivery = True
            for line in sale_order.order_line:
                if line.kitchen_state == 'ready':
                    is_order_delivery = False
                    break
            if is_order_delivery:
                self.change_order_state(sale_order.id, 'Delivered')

    def delete_order(self, order_id):
        """ Delete the sale order """
        sale_order = self.env['sale.order'].sudo().search([
            ('id', '=', int(order_id))])
        sale_order.action_cancel()
        #sale_order.write({'state': 'cancel'})
        return True

    def get_invoice_details(self, order_id):
        """ Get the invoice details from the sale order """
        sale_order = self.env['sale.order'].sudo().search([
            ('id', '=', int(order_id))])
        user = self.env['res.users'].sudo().browse(self.env.uid)
        account_journal = self.env['account.journal'].sudo().search([
            ('type', 'in', ['bank', 'cash']),
            ('company_id', '=', user.company_id.id)])
        journals = []
        payment_amount = 0
        date_format = '%Y-%m-%d'
        payment_date = (datetime.today()).strftime(date_format)
        invoice_id = 0
        for journal in account_journal:
            journals.append({'id': journal.id,
                             'name': journal.name})
        for invoice in sale_order.invoice_ids:
            payment_amount += invoice.residual
            invoice_id = invoice.id
        datas = [{'journals': journals,
                  'payment_amount': payment_amount,
                  'payment_date': payment_date,
                  'invoice_id': invoice_id,
                  'order_id': sale_order.id}]
        return datas
    
    def create_payment(self, journal_id, invoice_id, order_id):
        """ Create payment for invoice """
        sale_order = self.env['sale.order'].sudo().search([
            ('id', '=', int(order_id))])
        journal = self.env['account.journal'].sudo().search([
            ('id', '=', int(journal_id))])
        invoice = self.env['account.invoice'].sudo().search([
            ('id', '=', int(invoice_id))])

        invoice_ids = int(invoice_id)
        date_format = '%Y-%m-%d'
        payment_date = (datetime.today()).strftime(date_format)
        payment_val = {'payment_method_id': journal.inbound_payment_method_ids.id,
                       'invoice_ids': [(6, 0, [invoice_ids])],
                       'journal_id': journal.id,
                       'amount': invoice.residual,
                       'payment_date': payment_date,
                       'communication': invoice.number,
                       'payment_type': 'inbound',
                       'partner_type': 'customer',
                       'account_id': invoice.account_id.id,
                       'currency_id': invoice.currency_id.id,
                       'partner_id': invoice.partner_id.id
                       }
        payment = self.env['account.payment'].create(payment_val)
        payment.post()
        sale_order.write({'state': 'payment'})
        return True


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    kitchen_state = fields.Selection(
        [('open', 'Open'),
         ('confirm', 'Confirm'),
         ('preparing', 'Preparing'),
         ('ready', 'Ready'),
         ('delivered', 'Delivered'), ('cancel', 'Cancelled')],
        'Kitchen Status', default='open')

    def write(self, vals):
        """ Update the value in sale order line """
        result = super(SaleOrderLine, self).write(vals)
        if self.order_id.check_fields_to_send(vals):
            self.order_id.send_field_updates(self.order_id.ids)
        return result

    @api.model
    def create(self, vals):
        """ Create the value for sale order line """
        partner = super(SaleOrderLine, self).create(vals)
        if partner.order_id.check_fields_to_send(vals):
            partner.order_id.send_field_updates([partner.order_id.id])
        return partner

    def unlink(self):
        """ Unlink the record from sale order line """
        if self:
            self.order_id.send_field_updates(self.order_id.ids, action='unlink')
        res = super(SaleOrderLine, self).unlink()
        return res


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    kitchen_state = fields.Selection(
        [('preparing', 'Preparing'),
         ('ready', 'Ready'),
         ('delivered', 'Delivered'), ('cancel', 'Cancelled')],
        'Kitchen Status', default='preparing')


class PosOrder(models.Model):
    _inherit = 'pos.order'

    date_deliverd = fields.Datetime(string='Delivered Date', readonly=True,
                                    index=True, default=fields.Datetime.now)
    date_order_take = fields.Datetime(string='Order Take Date', readonly=True,
                                      index=True, default=fields.Datetime.now)
    is_order_confirmed = fields.Boolean(string='is_order_confirmed',
                                        default=False)


    @api.model
    def get_table_draft_orders_test(self, table_id):
        """Generate an object of all draft orders for the given table.

        Generate and return an JSON object with all draft orders for the given table, to send to the
        front end application.

        :param table_id: Id of the selected table.
        :type table_id: int.
        :returns: list -- list of dict representing the table orders
        """
        table_orders = self.search_read(
                domain = [('state', '=', 'draft'), ('table_id', '=', table_id)],
                fields = self._get_fields_for_draft_order())
        #=======================================================================
        # if table_orders:
        #     table_reference = table_orders[0]['pos_reference']
        #     table_ref = table_reference.split(' ')
        #     print(table_ref[1])
        #     table_ord = self.env['pos_multi_session_sync.order'].search_read( domain= [('order_uid' , '=',table_ref[1])])
        #     if table_ord:
        #         taes = table_ord[0]["order_uid"]
        #         tables = table_ord[0]["revision_ID"]
        #=======================================================================
        self._get_order_lines(table_orders)
        self._get_payment_lines(table_orders)
        for order in table_orders:
            #===================================================================
            # table_reference = order['pos_reference']
            # table_ref = table_reference.split(' ')
            # print(table_ref[1])
            #===================================================================
            order['pos_session_id'] = order['session_id'][0]
            order['uid'] = search(r"\d{5,}-\d{3,}-\d{4,}", order['pos_reference']).group(0)
            order['name'] = order['pos_reference']
            order['creation_date'] = order['create_date']
            order['server_id'] = order['id']
            table_ord = self.env['pos_multi_session_sync.order'].search_read( domain= [('order_uid' , '=', search(r"\d{5,}-\d{3,}-\d{4,}", order['pos_reference']).group(0))])
            if table_ord:
                tables = table_ord[0]["revision_ID"]
                order['revision_ID'] = tables
            if order['fiscal_position_id']:
                order['fiscal_position_id'] = order['fiscal_position_id'][0]
            if order['pricelist_id']:
                order['pricelist_id'] = order['pricelist_id'][0]
            if order['partner_id']:
                order['partner_id'] = order['partner_id'][0]
            if order['table_id']:
                order['table_id'] = order['table_id'][0]

            if not 'lines' in order:
                order['lines'] = []
            if not 'statement_ids' in order:
                order['statement_ids'] = []

            del order['id']
            del order['session_id']
            del order['pos_reference']
            del order['create_date']
        return table_orders

    @api.model
    def _order_fields(self, ui_order):
        """" Update the ui order in pos order fields """
        #last_line = len(ui_order['lines']) - 1
        order_fields = super(PosOrder, self)._order_fields(ui_order)
#         order_fields['date_deliverd'] = ui_order['lines'][last_line][2].get('delivered_date')
#         order_fields['date_order_take'] = ui_order.get('order_take_date')
#         order_fields['is_order_confirmed'] = ui_order.get('is_order_confirmed')
        return order_fields

    @api.model
    def get_complete_order(self, search_val):
        """ Get the paid and invoice order """
        pos_order = self.env['pos.order'].sudo().search([
            ('date_order', '>=', date.today()),
            ('state', 'in', ['paid','invoiced'])], order='id')
        result = []
        for order in pos_order:
            if(search_val !=''):
                if(search_val.capitalize() in (order.table_id.name).capitalize()):
                    result.append(self.get_order_details(order))
            else:
                result.append(self.get_order_details(order))
        return result

    def get_order_details(self, order):
        """ Get the order details from the completed orders"""
        no = order.pos_reference
        ono = int(no[-4:])
        data = []
        line_model = self.env['ir.model'].search([('model', '=', 'pos.order.line')], limit=1)
        line_field = self.env['ir.model.fields'].search([('model_id', '=', line_model.id),
                                                         ('name', '=', 'priority')])
        for line in order.lines:
            data_val = {'prod_name': line.product_id.display_name,
                        'qty': line.qty,
                        'status': order.state,
                        }
            # append priority values for complete orders
            if line_field:
                data_val['priority'] = line.priority or ''
            else:
                data_val['priority'] = ''
            data.append(data_val)
        user_time_zone = pytz.UTC
        if self.env.user.partner_id.tz:
            user_time_zone = pytz.timezone(self.env.user.partner_id.tz)
        odate_utc = order.date_order
        odate_utc = odate_utc.replace(tzinfo=pytz.UTC)
        odate_user_time = odate_utc.astimezone(user_time_zone).strftime(DT)
        odate_date = datetime.strptime(odate_user_time, DT)
        return {'customer_name': order.partner_id.name or '',
                'table_name': order.table_id.name,
                'floor_name': order.table_id.floor_id.name,
                'date': odate_date,
                'order_no': ono,
                'lines': data}
        
    """ Check the server is offline or not """
    def check_offline(self):
        return True

    
class RestaurantTable(models.Model):

    _inherit = 'restaurant.table'
    _description = 'Restaurant Table'

    is_take_away = fields.Boolean(string='Take Away', default=False)
    
class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_invoice_paid(self):
        """ While create the payment make the invoice payment status as paid """
        res = super(AccountMove, self).action_invoice_paid()
        for invoice in self:
            sale_order = self.env['sale.order'].sudo().search([
                ('name', '=', invoice.invoice_origin)])
            sale_order.update({'invoice_payment_status': 'paid'})
        return res
