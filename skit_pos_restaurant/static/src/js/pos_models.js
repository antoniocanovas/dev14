odoo.define('pos_models', function (require) {

    const models = require('point_of_sale.models');	
    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var _super_posmodel = models.PosModel.prototype;

    
	/** Load self served field in POS Category */
	models.load_fields('pos.category', ['self_served']);
        /** Order Line */
    var OrderlineSuper = models.Orderline;
    models.Orderline = models.Orderline.extend({
        initialize: function () {
            OrderlineSuper.prototype.initialize.apply(this, arguments);
            this.kitchen_state = this.kitchen_state;
            this.delivered_date  = this.delivered_date || new Date();
            /*Add priority value in order lines*/
			this.priority = this.priority || ''
			this.priority_value = this.priority_value || '';
			/* Line_stamp addons_id */
			this.line_stamp = this.line_stamp || ''
			this.addons_id = this.addons_id || '';
        },
        clone: function () {
	        var orderline = OrderlineSuper.prototype.clone.apply(this,arguments);
	        orderline.kitchen_state = this.kitchen_state;
	        orderline.delivered_date = this.delivered_date;
			orderline.priority = this.priority
			orderline.priority_value = this.priority_value
			orderline.line_stamp = this.line_stamp
			orderline.addons_id = this.addons_id
	        return orderline;
	    },
        export_as_JSON: function () {
	        var json = OrderlineSuper.prototype.export_as_JSON.apply(this,arguments);
	        json.kitchen_state = this.get_Kitchen_State()
	        json.delivered_date = this.get_Delivered_Date()
			json.order_priority = this.getOrderPriority()
			json.priority_value = this.getOrderPriorityValue()
			json.line_stamp = this.line_stamp;
            json.addons_id = this.addons_id;
	        return json;
	    },
	    init_from_JSON: function (json) {
	    	OrderlineSuper.prototype.init_from_JSON.apply(this,arguments);
	        this.set_Kitchen_State(json.kitchen_state);
	        this.set_Delivered_Date(json.delivered_date);
			this.setOrderPriority(json.priority);
			this.setOrderPriorityValue(json.priority_value);
			this.line_stamp = json.line_stamp;
            this.addons_id = json.addons_id;
	    },
		/* ---- Kitchen Status  --- */
	    set_Kitchen_State: function (state) {
	        this.kitchen_state = state;
	        this.trigger('change',this);
	    },
	    get_Kitchen_State: function () {
	        return this.kitchen_state;
	    },
	    /*Kitchen delivery date status */
	    set_Delivered_Date: function (date) {
	        this.delivered_date = date;
	        this.trigger('change',this);
	    },
	    get_Delivered_Date: function () {
	        return this.delivered_date;
	    },
		/*Get and set order priority*/
		getOrderPriority: function () {
	    	return this.priority;
	    },
	    setOrderPriority: function (priority) {
	        this.priority = priority;
	    },
		getOrderPriorityValue: function () {
	    	return this.priority_value;
	    },
		setOrderPriorityValue: function (priority_value) {
	        this.priority_value = priority_value;
	    },
	    /*Get and set Addon lineStampy*/
		getAddonId: function () {
	    	return this.addons_id;
	    },
	    setAddonId: function (addons_id) {
	        this.addons_id = addons_id;
	    },
		getLineStamp: function () {
	    	return this.line_stamp;
	    },
		setLineStamp: function (line_stamp) {
	        this.line_stamp = line_stamp;
	    },
		/** Inherit and return false for product is same */
		can_be_merged_with: function(orderline) {
	        if (this.get_product().id === orderline.get_product().id && (this.get_Kitchen_State() === 'preparing' || this.get_Kitchen_State() === 'ready' || this.get_Kitchen_State() === 'delivered' || this.get_Kitchen_State() === 'cancel')) {
	            return false;
	        } else {
	            return OrderlineSuper.prototype.can_be_merged_with.apply(this,arguments);
	        }
	    },  
    });
    
    /** Change the Account Bank Statement domain for get all statements */
    models.PosModel = models.PosModel.extend({
	    initialize: function (session, attributes) {        
	        var restaurant_table_model = _.find(this.models, function (model) {
	            return model.model === 'restaurant.table';
	        });
	        restaurant_table_model.fields.push('is_take_away');
	        
	         _super_posmodel.initialize.call(this, session, attributes);
	        
	         this.models.push({
            model:  'res.users',
            fields: ['name', 'pos_config_id'],
            ids:    function (self) { return [self.session.uid]; },
            loaded: function (self,users) {
                self.wet_user = users[0];
            },
        })
	         return this;
	    }
    });

    /** Order */
    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (options) {
            _super_order.initialize.apply(this,arguments);
            options  = options || {};
            this.order_hour = this.order_hour || 0;
            this.order_min = this.order_min || 0;
            this.order_sec = this.order_sec || 0;
            this.order_take_date  = this.order_take_date || new Date();
            this.delivery = false;
            this.order_paid = this.order_paid || false;
            this.all_delivery = this.all_delivery || false;
            this.cancel_order_line = this.cancel_order_line || false;
            this.view_order = 'pos_display_none'
            this.hide_order = 'pos_display_block'
            this.save_to_db();
            return this;
        },
        export_as_JSON: function () {
            var json = _super_order.export_as_JSON.apply(this,arguments);
            json.order_hour = this.order_hour;
            json.order_min = this.order_min;
            json.order_sec = this.order_sec;
            json.order_take_date = this.order_take_date;
            json.delivery = this.delivery;
            json.order_paid = this.order_paid;
            json.view_order = this.view_order;
            json.hide_order = this.hide_order;
            json.all_delivery = this.all_delivery;
            json.cancel_order_line = this.cancel_order_line;
            return json;
        },
        init_from_JSON: function (json) {
            _super_order.init_from_JSON.apply(this,arguments);
            this.order_hour = json.order_hour;
            this.order_min = json.order_min;
            this.order_sec = json.order_sec;
            this.order_take_date = json.order_take_date;
            this.delivery = json.delivery;
            this.order_paid = json.order_paid;
            this.view_order = json.view_order;
            this.hide_order = json.hide_order;
            this.all_delivery = json.all_delivery;
            this.cancel_order_line = json.cancel_order_linel
        },
        export_for_printing: function () {
            var json = _super_order.export_for_printing.apply(this,arguments);
            json.order_hour = this.get_Order_Hour();
            json.order_min = this.get_Order_Min();
            json.order_sec = this.get_Order_Sec();
            json.order_take_date = this.get_Order_Take_Date();
            json.delivery = this.get_Delivery();
            json.order_paid = this.get_Order_Paid();
            json.view_order = this.get_View_Order();
            json.hide_order = this.get_Hide_Order();
            json.all_delivery = this.get_All_Delivery();
            json.cancel_order_line = this.get_Cancel_Order_Line();
            return json;
        },
      /*set order hours,minute and secounds*/
        get_Order_Hour: function () {
            return this.order_hour;
        },
        set_Order_Hour: function (hour) {
            this.order_hour = hour;
        },    
        get_Order_Min: function () {
            return this.order_min;
        },
        set_Order_Min: function (min) {
            this.order_min = min;
        },
        get_Order_Sec: function () {
            return this.order_sec;
        },
        set_Order_Sec: function (sec) {
            this.order_sec = sec;
        },
      //end
      
      	/*get and set the order take date */
        get_Order_Take_Date: function () {
            return this.order_take_date;
        },
        set_Order_Take_Date: function (date) {
            this.order_take_date = date;
        },
        //end
        
        /*get and set order devlivery*/
        get_Delivery: function () {
            return this.delivery;
        },
        set_Delivery: function (delivery) {
            this.delivery = delivery;
        },
        //end
        
        /*get and set order paid details */
        get_Order_Paid: function () {
            return this.order_paid;
        },
        set_Order_Paid: function (order_paid) {
            this.order_paid = order_paid;
        },
        //end
        
        /*get and set the every orders delivery statues*/
        get_All_Delivery: function () {
        	return this.all_delivery;
        },
        set_All_Delivery: function (all_delivery) {
            this.all_delivery = all_delivery;
        },
        //end 
        
        /*get and set the view the orders details*/
        get_View_Order: function () {
            return this.order_paid;
        },
        set_View_Order: function (view_order) {
            this.view_order = view_order;
        },
        //end 
        
        /*get and set the Hide order details*/
        get_Hide_Order: function () {
            return this.order_paid;
        },
        set_Hide_Order: function (hide_order) {
            this.hide_order = hide_order;
        },
        //end
        
        /*get and set the cancel order lines*/
        get_Cancel_Order_Line: function () {
        	return this.cancel_order_line;
        },
        set_Cancel_Order_Line: function (cancel_order_line) {
        	this.cancel_order_line = cancel_order_line;
        },
        //end
        
        /** Remove paid order from waiter view */
        remove_Paid_Orders: function (order) {
	            order.finalize()
	            this.pos.set_table(null);
	    },
        
        /** Inherit and replace the Total and Tax method for 
         * reduce amount for cancel state */
         /*Get product without tax amount details*/
        get_total_without_tax: function () {
            return round_pr(this.orderlines.reduce((function (sum, orderLine) {
                if (orderLine.kitchen_state != 'cancel') {
                	return sum + orderLine.get_price_without_tax();
                } else {
                	return sum;
                }
            	
            }), 0), this.pos.currency.rounding);
        },
        /*Get product total discount details*/
        get_total_discount: function () {
            return round_pr(this.orderlines.reduce((function (sum, orderLine) {
            	if (orderLine.kitchen_state != 'cancel') {
            		return sum + (orderLine.get_unit_price() * (orderLine.get_discount()/100) * orderLine.get_quantity());
            	} else {
            		return sum;
            	}
            }), 0), this.pos.currency.rounding);
        },
        /*Get product total details*/
        get_total_tax: function () {
            if (this.pos.company.tax_calculation_rounding_method === "round_globally") {
                // As always, we need:
                // 1. For each tax, sum their amount across all order lines
                // 2. Round that result
                // 3. Sum all those rounded amounts
                var groupTaxes = {};
                this.orderlines.each(function (line) {
                    var taxDetails = line.get_tax_details();
                    var taxIds = Object.keys(taxDetails);
                    for (var t = 0; t<taxIds.length; t++) {
                        var taxId = taxIds[t];
                        if (!(taxId in groupTaxes)) {
                            groupTaxes[taxId] = 0;
                        }
                        groupTaxes[taxId] += taxDetails[taxId];
                    }
                });

                var sum = 0;
                var taxIds = Object.keys(groupTaxes);
                for (var j = 0; j<taxIds.length; j++) {
                    var taxAmount = groupTaxes[taxIds[j]];
                    sum += round_pr(taxAmount, this.pos.currency.rounding);
                }
                return sum;
            } else {
                return round_pr(this.orderlines.reduce((function (sum, orderLine) {
                    if (orderLine.kitchen_state != 'cancel') {
                    	return sum + orderLine.get_tax();
                    } else {
                    	return sum;
                    }
                }), 0), this.pos.currency.rounding);
            }
        },
        /*Get product tax details*/
        get_tax_details: function () {
            var details = {};
            var fulldetails = [];

            this.orderlines.each(function (line) {
            	if (line.kitchen_state != 'cancel') {
	                var ldetails = line.get_tax_details();
	                for (var id in ldetails) {
	                    if (ldetails.hasOwnProperty(id)) {
	                        details[id] = (details[id] || 0) + ldetails[id];
	                    }
	                }
            	}
            });

            for (var id in details) {
                if (details.hasOwnProperty(id)) {
                    fulldetails.push({amount: details[id], tax: this.pos.taxes_by_id[id], name: this.pos.taxes_by_id[id].name});
                }
            }

            return fulldetails;
        },
    });
});