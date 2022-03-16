odoo.define('pos_order_priority.models', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var PosDB = require("point_of_sale.DB");
	var utils = require('web.utils');
	var round_pr = utils.round_precision;
	var exports = {};

	models.load_models({
		model: 'pos.order.line.priority',
		fields: ['name', 'value', 'color_code'],
		domain: null,
		loaded: function(self, line_priority) {
			self.line_priority = line_priority;
		},
	});
	models.load_fields('pos.config', 'priority_ids');



});
