# -*- coding: utf-8 -*-
# imports of odoo lib
import xmlrpc.client

url = "http://odoo14.srikeshinfotech.com:8069"
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# While install the addon this def is used to check odoo15 server if this addon is validity or not valid raise exception error
def pre_init_hook(cr):
    email = 'demo@srikeshinfotech.com'
    #partner_id = models.execute_kw('timesheet', 68, 'c6b692fef5f6fe15fcbf8d60e95094f9ec963f42',
    #                                'res.partner','search_read', [[['email', '=', email]]], {'fields': ['name', 'validity_status']})
    #validity = partner_id[0]['validity_status']
    #if (validity != 'valid'):
    #    raise Exception('Unable to install')
    return False 

# After installing the addon write the validity_status not valid 
def post_init_hook(cr, registry):   
   
    email = 'demo@srikeshinfotech.com'
    #partner = models.execute_kw('timesheet', 68, 'c6b692fef5f6fe15fcbf8d60e95094f9ec963f42',
    #                                'res.partner', 'search', [[['email', '=', email]]])
    #partner_id = models.execute_kw('timesheet', 68, 'c6b692fef5f6fe15fcbf8d60e95094f9ec963f42',
    #                                'res.partner', 'write', [partner[0], {'validity_status': 'not valid'}])