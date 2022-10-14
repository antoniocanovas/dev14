# -*- coding: utf-8 -*-
# imports of python lib
from datetime import date
# imports of odoo lib
from odoo import http
from odoo.http import request
# imports of odoo addons
from odoo.addons.point_of_sale.controllers.main import PosController
     
class ExpiryDate(PosController):
    
    @http.route(['/pos/web', '/pos/ui'], type='http', auth='user')
    def pos_web(self, **k):
        #     search and get the values in ir.config_parameter form.
        pos_web = super(ExpiryDate, self).pos_web(**k)
        expiry_date = request.env['ir.config_parameter'].sudo().get_param('skit_pos.expiry_date')
        encryption_key = request.env['ir.config_parameter'].sudo().get_param('skit_pos.encryption_key')
        today = str(date.today())
        domain = [
                ('state', 'in', ['opening_control', 'opened']),
                ('user_id', '=', request.session.uid),
                ('rescue', '=', False)
                ]
        session_info = request.env['ir.http'].session_info()
        pos_session = request.env['pos.session'].sudo().search(domain, limit=1)
        context = {
            'session_info': session_info,
            'login_number': pos_session.login(),
            'expiry_date': expiry_date,
            'encryption_key': encryption_key,
            'today': today,
        }
        return request.render('point_of_sale.index', qcontext=context)



