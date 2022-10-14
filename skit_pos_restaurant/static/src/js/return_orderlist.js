odoo.define('skit_pos_restaurant.return_orderlist', function (require) {
	'use strict';
	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const models = require('point_of_sale.models');	
	const { useListener } = require('web.custom_hooks');
	var core = require('web.core');
	var QWeb = core.qweb;
	
	/*Load the models*/
	models.load_models({
    model:  'pos.order',
    fields: ['name', 'partner_id','date_order','amount_total', 'amount_tax',
        'pos_reference','lines','state','session_id','company_id','return_ref','return_status','is_order_confirmed'],
    	loaded: function (self, return_orders){
        	self.return_orders = return_orders;
        }
    },
    {
    model: 'pos.order.line',
    fields: ['product_id','qty','price_unit','price_subtotal_incl','order_id','discount','returned_qty'],
    loaded: function (self,return_order_lines){
	    self.return_order_line = [];
	    for (var i = 0; i < return_order_lines.length; i++) {
	        self.return_order_line[i] = return_order_lines[i];
	    }
	    }
	});
	/*return OrderList screen  */
	class returnOrderList extends PosComponent {
		constructor(parent, options) {
	        super(parent, options);
	        useListener('button_Back', this._button_Back);
		}
    	mounted() {
	        var returnOrders = this.env.pos.return_orders;
	        this.render_list(returnOrders);	
	    }

		async _button_Back() {
			this.showScreen("ProductScreen")
		}
		return_Order() {
			var order = $(e.target).closest("tr").data('id');
		    self.return_order(order);
		}
	    get_orders() {
	        return this.gui.get_current_screen_param('orders');
	    }
	    perform_search(query) {
	        var orders;
	        if (query) {
	            orders = this.search_order(query);
	            this.render_list(orders);
	        } else {
	        	returnOrders = this.pos.return_orders;
	            this.render_list(returnOrders);
	        }
	    }
	    search_order(query) {
	        try {
	            var re = RegExp(query, 'i');
	        } catch(e) {
	            return [];
	        }
	        var results = [];
	        for (var order_id in this.pos.return_orders) {
	            var r = re.exec(this.pos.orders[order_id]['name']+ '|'+ this.pos.return_orders[order_id]['partner_id'][1]);
	            if (r) {
	            results.push(this.pos.return_orders[order_id]);
	            }
	        }
	        return results;
	    }
	    clear_search() {
	        var returnOrders = this.pos.return_orders;
	        this.render_list(returnOrders);
	        this.$('.searchbox input')[0].value = '';
	        this.$('.searchbox input').focus();
	    }
	    render_list(orders) {    
	        var contents = document.querySelector('.order-list-contents');
	        contents.innerHTML = "";
	        for (var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
	            var order    = orders[i];
	            var orderline_html = QWeb.render('ReturnOrderLine',{widget: this, order:order});
	            var orderline = document.createElement('tbody');
	            orderline.innerHTML = orderline_html;
	            orderline = orderline.childNodes[1];
	            contents.appendChild(orderline);
	        }
	    }
	    return_order(order_id) {
	        var self = this;
	        var order = this.get_Order_By_Id(order_id);
	        var client = ''
	        if (order.partner_id) {
	             client = order.partner_id[0];
	        }
	        if (order && order.return_status ==='fully_return') {
	                  self.gui.show_popup('error',_t('This is a fully returned order'));
	        } else if (order && order.return_ref) {
	            self.gui.show_popup('error',_t('This is a returned order'));
	        } else {
	            console.log(order.pos_reference,client)
	            self.gui.show_popup('ReturnWidget',{ref: order.pos_reference,client:client});
	        }
	    }
	    get_Order_By_Id(id) {
	        var orders = this.pos.return_orders;
	        for (var i in orders) {
	            if (orders[i].id === id) {
	                return orders[i];
	            }
	        }
	
	    }
    }
	returnOrderList.template = 'returnOrderList';

    Registries.Component.add(returnOrderList);

    return returnOrderList;
    
});
