odoo.define('pos_product_standard_note.ReceiptScreen', function(require) {
	"use strict";
	const OrderReceipt = require('point_of_sale.OrderReceipt');
	const Registries = require('point_of_sale.Registries');

	const ReceiptScreen = OrderReceipt =>
		class extends OrderReceipt {
			constructor() {
				super(...arguments);
			}
			get receipt() {
				let order = this.env.pos.get_order();
				let receipt = this.receiptEnv.receipt;
				let orderline = this.receiptEnv.receipt.orderlines
				for (var i =0; i < this.orderlines.length; i++) {
                    if (this.orderlines[i].note){
                        for (var x =0; x < orderline.length; x++) {
                            if (orderline[x].id == this.orderlines[i].id) {
                                orderline[x]['order_note'] = this.orderlines[i].note
                            }
                        }
                    }
				}

				return receipt;
			}
	};
	Registries.Component.extend(OrderReceipt, ReceiptScreen);
	return OrderReceipt;
});
