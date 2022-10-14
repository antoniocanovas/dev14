odoo.define('skit_pos_restaurant.Orderline', function(require) {
    'use strict';

    const Orderline = require('point_of_sale.Orderline');
    const Registries = require('point_of_sale.Registries');
	const { useListener } = require('web.custom_hooks');

    const SkitPosResOrderline = Orderline =>
        class extends Orderline {
            constructor() {
            	super(...arguments);
				useListener('reverse_btn', this._reverseAction);
				useListener('forward_btn', this._forwardAction);	
			}
			
			/* Kitchen status reverse action */
			async _reverseAction() {
				this.env.pos.get_order().select_orderline(this.props.line);
				this.env.pos.get_order().trigger('new_updates_to_send');
				var selectedLine = this.env.pos.get_order().selected_orderline
				var productCategID = selectedLine.get_product().pos_categ_id[0]
				var categoryData = this.env.pos.db.get_category_by_id(productCategID)
				if (categoryData.self_served && selectedLine.get_Kitchen_State() === 'delivered') {
					selectedLine.set_Kitchen_State('preparing');
				} else if (selectedLine.get_Kitchen_State() === 'preparing') {
					selectedLine.set_Kitchen_State('cancel');
				} else if (selectedLine.get_Kitchen_State() === 'ready') {
					selectedLine.set_Kitchen_State('preparing');
				} else if (selectedLine.get_Kitchen_State() === 'delivered') {
					selectedLine.set_Kitchen_State('ready');
				}
			}

			/* Kitchen status forward action */
			async _forwardAction() {
				this.env.pos.get_order().select_orderline(this.props.line);
				this.env.pos.get_order().trigger('new_updates_to_send');
				var selectedLine = this.env.pos.get_order().selected_orderline
				var productCategID = selectedLine.get_product().pos_categ_id[0]
				var categoryData = this.env.pos.db.get_category_by_id(productCategID)
				if (categoryData.self_served && selectedLine.get_Kitchen_State() === 'preparing') {
					selectedLine.set_Kitchen_State('delivered');
				} else if (selectedLine.get_Kitchen_State() === 'cancel') {
					selectedLine.set_Kitchen_State('preparing');
				} else if (selectedLine.get_Kitchen_State() === 'preparing') {
					selectedLine.set_Kitchen_State('ready');
				} else if (selectedLine.get_Kitchen_State() === 'ready') {
					selectedLine.set_Kitchen_State('delivered');
				}
			}
        };

    Registries.Component.extend(Orderline, SkitPosResOrderline);

    return Orderline;
});
