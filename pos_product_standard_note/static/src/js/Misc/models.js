odoo.define('pos_product_standard_note.models', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var PosDB = require("point_of_sale.DB");
	var utils = require('web.utils');
	var round_pr = utils.round_precision;
	var exports = {};

	models.load_fields('product.template', ['pos_note_type_id']);
	models.load_fields('pos.order', ['order_note']);

	models.load_models({
		model: 'pos.note.type',
		fields: ['name', 'note_ids'],
		domain: null,
		loaded: function(self, note_ids) {
			self.note_ids = note_ids;
			self.note_by_nodes = {};
			self.note_ids.forEach(function(note_id) {
                self.note_by_nodes[note_id.id] = note_id.note_ids;
            });
		},
	});

	models.load_models({
		model: 'pos.note',
		fields: ['id', 'name'],
		domain: null,
		loaded: function(self, note_id) {
			self.note_id = note_id;
		},
	});


	var OrderlineSuper = models.Orderline.prototype;
	models.Orderline = models.Orderline.extend({

		initialize: function(attr, options) {
			this.order_note = this.order_note || false;
			OrderlineSuper.initialize.call(this,attr,options);
		},

		set_order_note: function(order_note){
			this.order_note = order_note;
		},

		get_order_note: function(){
			return this.order_note;
		},

		export_as_JSON: function() {
			var json = OrderlineSuper.export_as_JSON.apply(this,arguments);
			json.order_note = this.order_note || false;
			return json;
		},

		init_from_JSON: function(json){
			OrderlineSuper.init_from_JSON.apply(this,arguments);
			this.order_note = json.order_note;
		},
	});



});