from odoo import models, fields, api


class PosOrderP(models.Model):
	_inherit = 'pos.order'

	priority = fields.Char(string='Priority')
	priority_value = fields.Integer(string='Priority Value')

	def _get_fields_for_order_line(self):
		result = super(PosOrderP, self)._get_fields_for_order_line()
		result.append('priority')
		result.append('priority_value')
		return result

	def _get_fields_for_draft_order(self):
		fields = super(PosOrderP, self)._get_fields_for_draft_order()
		fields.append('priority')
		fields.append('priority_value')
		return fields

	@api.model
	def _order_fields(self, ui_order):
		result = super(PosOrderP, self)._order_fields(ui_order)
		result['priority'] = ui_order['priority'] or ''
		result['priority_value'] = ui_order['priority_value'] or ''
		return result