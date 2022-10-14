# -*- coding: utf-8 -*-
# imports of odoo lib
from odoo import models, fields
#from odoo.exceptions import UserError

class RestaurantFloor(models.Model):
    _inherit = 'restaurant.floor'
    # Inherit restaurant floor table add pos_multi_session_ids field
    pos_multi_session_ids = fields.Many2many('pos.multi_session', 'pos_multi_session_floor_rel', 'floor_id', 'pos_multi_session_id')
    
#     def write(self, vals):
#         for floor in self:
#             if floor.pos_config_id.has_active_session and (vals.get('pos_config_id') or vals.get('active')) :
#                 raise UserError(
#                     'Please close and validate the following open PoS Session before modifying this floor.\n'
#                     'Open session: %s' % (' '.join(floor.pos_config_id.mapped('name')),))
#             print(vals.get('pos_config_id'))
#             print(floor.pos_config_id.ids)
#             print(vals.get('pos_config_id') != floor.pos_config_id.id)
#             if vals.get('pos_config_id') and floor.pos_config_id.id and vals.get('pos_config_id') == floor.pos_config_id.id:
#                 raise UserError('The %s is already used in another Pos Config.' % floor.name)
#         return super(RestaurantFloor, self).write(vals)

class PosMultiSession(models.Model):
    _inherit = 'pos.multi_session'
    # Inherit pos multi session table add fields
    floor_ids = fields.Many2many('restaurant.floor', 'pos_multi_session_floor_rel', 'pos_multi_session_id', 'floor_id',
                                 string='Restaurant Floors', help='The restaurant floors served by this point of sale',
                                 ondelete="restrict")
    table_blocking = fields.Boolean('One Waiter per Table')


class PosConfig(models.Model):
    _inherit = 'pos.config'
    # Inherit pos config session table add fields
    ms_floor_ids = fields.Many2many(related='multi_session_id.floor_ids', string='Multi-Session Restaurant Floors')
    table_blocking = fields.Boolean(related='multi_session_id.table_blocking')
