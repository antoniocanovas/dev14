odoo.define('skit_pos_restaurant.pos_config_parameter', function (require) {
	'use strict';
	
	const models = require('point_of_sale.models');
	
	//get values in ir.config_parameter model
	models.load_models([
	   {
	        model: 'ir.config_parameter',
	        fields: ['value'],	
	        domain: [['key','=','skit_pos.expiry_date']],
	        loaded: function (self,pos_expiry_date) {
	            self.pos_expiry_date = pos_expiry_date;
	        },
	   },
		  
 	]);
});