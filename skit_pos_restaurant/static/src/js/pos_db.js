odoo.define('skit_pos_restaurant.pos_db', function (require) {
    "use strict";
    var posDB = require('point_of_sale.DB'); // To extend db.js file 
    posDB.include({
		name: 'openerp_pos_db', //the prefix of the localstorage data
	    limit: 100,  // the maximum number of results returned by a search
	    init: function (options) {
	    	this._super(options);
	    	this.sorder_by_id = {};
	    	this.sorder_write_date = null;
	    	this.sorder_sorted = [];
	    	this.orderline_by_order = {};
	    	this.sorderline_by_id = {};
	    	this.active_tab = 'payment';
	    	this.track_screen ='';
	    	this.payment_valid_name = "";
	    	this.isNetWork = "active"
	    },
	    
	     /*Get and set the active tab value in cashier and waiter view*/
	    get_Active_Tab: function () {
	    	return this.active_tab;
	    },
	    set_Active_Tab: function (tab) {
	    	this.active_tab = tab;
	    },
	    //end 
	    /*get and set - Track the order status  in cashier and waiter view*/
	    get_Track_Screen: function () {
	    	return this.track_screen;
	    },
	    set_Track_Screen: function (t_screen) {
	    	this.track_screen = t_screen;
	    },
	     /*get_Payment_Screen: function () {
	    	return this.payment_valid_name;
	    },
	    set_Payment_Screen: function (Pay_screen) {
	    	this.payment_valid_name = Pay_screen;
	    },*/
	    //end
	    /*Remove unpaid orders in waiter view */
	    remove_unpaid_order: function (order) {
	        var orders = this.load('unpaid_orders',[]);
	        orders = _.filter(orders, function () {
	        	var lines = order.lines
	        	var state = 'delivered';
	        	if (lines != undefined && lines != '') {
	        		for (var i = 0, len = (lines).length; i < len; i++) {
	            		if (lines[i][2].kitchen_state === 'preparing') {
	            			state = 'preparing';
	            		}
	            	}
	        	}
	            return state !== 'delivered';
	        });
	        this.save('unpaid_orders',orders);
	    },
	    /* sale orders are store in temporary */
	    add_Sorders: function (orders) {
	        var updatedCount = 0;
	        var newWriteDate = '';
	        var order;
	        for (var i = 0, len = orders.length; i < len; i++) {
	            order = orders[i];

	            var localOrderDate = (this.sorder_write_date || '').replace(/^(\d{4}-\d{2}-\d{2}) ((\d{2}:?){3})$/, '$1T$2Z');
	            var distOrderDate = (order.write_date || '').replace(/^(\d{4}-\d{2}-\d{2}) ((\d{2}:?){3})$/, '$1T$2Z');
	            if (this.sorder_write_date &&
                    this.sorder_by_id[order.id] &&
                    new Date(localOrderDate).getTime() + 1000 >=
                    new Date(distOrderDate).getTime() ) {
	                // FIXME: The write_date is stored with milisec precision in the database
	                // but the dates we get back are only precise to the second. This means when
	                // you read partners modified strictly after time X, you get back partners that were
	                // modified X - 1 sec ago. 
	                continue;
	            } else if ( newWriteDate < order.write_date ) { 
	                newWriteDate  = order.write_date;
	            }
	            if (!this.sorder_by_id[order.id]) {
	                this.sorder_sorted.push(order.id);
	            }
	            this.sorder_by_id[order.id] = order;

	            updatedCount += 1;
	        }
	        this.sorder_write_date = newWriteDate || this.sorder_write_date;
	        return updatedCount;
	    },
	    /*get the sale order write date*/
	    get_Sorder_Write_Date: function () {
	        return this.partner_write_date || "1970-01-01 00:00:00";
	    },
	    /*get the sale order Id*/
	    get_Sorder_By_Id: function (id) {
	        return this.sorder_by_id[id];
	    },
	    /*get the sale order - orders*/
	    get_Sorder_Sorted: function (max_count) {
	        max_count = max_count ? Math.min(this.sorder_sorted.length, max_count) : this.sorder_sorted.length;
	        var orders = [];
	        for (var i = 0; i < max_count; i++) {
	            orders.push(this.sorder_by_id[this.sorder_sorted[i]]);
	        }
	        return orders;
	    },
	    /*add and get the sale order lines into the orders*/
	    get_Orderline_By_Order: function (order_id) {
	        return this.orderline_by_order[order_id];
	    },
	    add_Orderline_By_Order: function (order_id, orderline) {
	    	if (!this.orderline_by_order[order_id]) {
    			this.orderline_by_order[order_id] = [];
            }
	    	var olines = this.orderline_by_order[order_id];
	    	var isExist = false;
	    	for (var i = 0, len = olines.length; i < len; i++) {
	    		
	    		if (olines[i]['id'] === orderline.id) {
	    			isExist = true;
	    		}
	    	}
	    	if (isExist) {
	    		this.orderline_by_order[order_id] = [];
	    		isExist = false;
	    	}
	    	if (!isExist) {
	    		this.orderline_by_order[order_id].push(orderline);
	    	}
    		
	    },
	    //end
	    /*add the every order lines into temporary*/
	    add_Orderline: function (orderlines) {
	    	for (var i = 0, len = orderlines.length; i < len; i++) {
	    		var orderId = orderlines[i].order_id[0];
	    		this.add_Orderline_By_Order(orderId, orderlines[i])
	    	}
	    },
	});
	return posDB;	
});