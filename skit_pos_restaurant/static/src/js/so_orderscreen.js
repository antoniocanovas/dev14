odoo.define('skit_pos_restaurant.SOOrderScreen', function (require) {
	'use strict';
	const Registries = require('point_of_sale.Registries');
	const { Gui } = require('point_of_sale.Gui');
	const Chrome = require('point_of_sale.Chrome');
	const IndependentToOrderScreen = require('point_of_sale.IndependentToOrderScreen');
	const models = require('point_of_sale.models');
	const { useListener } = require('web.custom_hooks');
	var core = require('web.core');
	var _t = core._t;
	var QWeb = core.qweb;
	var rpc = require('web.rpc');
	var zoomLevel = 1;
	var SOOrderScreenWidget;
	var PosModelSuper = models.PosModel;
	/*Load Pos models*/
    models.PosModel = models.PosModel.extend({
	    set_start_order: function () {
	    	if (!this.config.iface_floorplan) {
		        var orders = this.get('orders').models;
		        if (orders.length && !this.get('selectedOrder')) {
		            this.set('selectedOrder',orders[0]);
		        } else {
		            this.add_new_order();
		        }
	    	} else {
	    		if (this.config.supplier_view || (this.config.cashier_view && this.db.get_Track_Screen() === "track_status_screen") || (this.config.waiter_view && this.db.get_Track_Screen() === "track_status_screen")) {
					var orders = this.get('orders').models;
	    	        if (orders.length && !this.get('selectedOrder')) {
	    	            this.set('selectedOrder',orders[0]);
	    	        }/* else {
	    	            this.add_new_order();
	    	        }*/
	    		}
	    	}
	    },
	/*Get overall orders*/
		get_order_list: function () {
	        var orders = this.get('orders').models;
	        if (!this.config.iface_floorplan) {
	            return orders;
	        } else if (!this.table && !this.config.supplier_view && (!this.config.cashier_view && !this.db.get_Track_Screen() === "track_status_screen") && (!this.config.waiter_view && !this.db.get_Track_Screen() === "track_status_screen")) {
	        	return [];
	        } else {
	        	if (this.config.supplier_view || (this.config.cashier_view && this.db.get_Track_Screen() === "track_status_screen") || (this.config.waiter_view && this.db.get_Track_Screen() === "track_status_screen")) {
	        		return orders;
	        	} else {
		            var totalOrders = [];
		            for (var i = 0; i < orders.length; i++) {
		                if ( orders[i].table === this.table) {
		                    totalOrders.push(orders[i]);
		                }
		            }
		            return totalOrders;
	        	}
	        }
	    },
	    /*get order status into the waiter view*/
	    get_Waiter_Status: function (table) {
	    	var orders = this.get_table_orders(table);
	        var totalOrders = [];
	        for (var i = 0; i < orders.length; i++) {
	            if (orders[i].table === table) {
	            	var orderlines = orders[i].get_orderlines();
	            	for (var j = 0, len = orderlines.length; j < len; j++) {
		            	if (orderlines[j].get_Kitchen_State() === 'ready') {
		            		totalOrders.push(orders[i]);
		            	}
	            	}
	            }
	        }
	        return totalOrders;
	    },
	/*Update orders in kitchen and cashier view*/
		ms_update_existing_order: function (order, data) {            
	        PosModelSuper.prototype.ms_update_existing_order.apply(this, arguments);
	        var self =this;
			if (self.env.pos.config.supplier_view || (self.env.pos.config.cashier_view && this.env.pos.db.get_Track_Screen() ==="track_status_screen") || (self.env.pos.config.waiter_view && this.env.pos.db.get_Track_Screen() ==="track_status_screen")) {
				if (SOOrderScreenWidget != undefined && SOOrderScreenWidget != null) {
					SOOrderScreenWidget.update_Sorder_Screen();
				}		
			}
	    },    
	});
 /**Load the sale order and order lines model **/
	 models.load_models([
		   {
		        model:  'sale.order',
		        fields: [],	
		        domain: [['state','not in', ['cancel']]],
		        order:  _.map(['id','name'], function (name) { return {name: name}; }),
		        loaded: function (self,orders) {
		            self.orders = orders;
		            self.db.add_Sorders(orders);
		        },
		   },
		   
		   {
		        model:  'sale.order.line',
		        fields: ['product_id', 'product_uom_qty', 'price_subtotal', 'order_id', 'kitchen_state'],
		        order:  _.map(['order_id','name'], function (name) { return {name: name}; }),
		        domain: [['order_id.state','not in',['cancel']]],
		        loaded: function (self,orderlines) {
		            self.orderlines = orderlines;
		            self.db.add_Orderline(orderlines);
		        },
		   },	
	 ]);

	 class SOOrderScreen extends IndependentToOrderScreen {
		constructor() {
            super(...arguments);
			SOOrderScreenWidget = this;
         	useListener('comp_search_box', this._comp_Search_Box);
         	useListener('order_Search', this._order_Search);
         	useListener('payment_Orders', this._payment_Orders);
         	useListener('inprogress_Orders', this._inprogress_Orders);
         	useListener('completed_Orders', this._completed_Orders);
         	useListener('res_Back_Button', this._res_Back_Button);
         	useListener('order_Status', this._order_Status);
         	//useListener('order_Search', this._order_Search);
         	//useListener('comp_search_box', this._comp_Search_Box);
         	//useListener('order_Search', this._order_Search);
     	}
	
	    init(parent, options) {
	        this._super(parent, options);
	        this.editing = false;
	        this.show();
	    }
	    /*get the current date */
    	getCurrnetDate() {
			var date =new Date();
			return moment(date).format('YYYY-MM-DD');
		}
		/*search box in kitchen view - easy to find complete order*/
	   	async _comp_Search_Box() {
	   		if (e.keyCode === 13) {
	    		this.complete_Order();
	        }
	   	}
	   	async _order_Search() {
	   		this.complete_Order();
	   	}
	   	//end
   /******start code - click action for inprogress orders, payment orders,complete orders and tab design code******/
	   	async _payment_Orders() {
	   		this.payment_Order();
	   	}
	   	async _inprogress_Orders() {
	   		this.inprogress_Order();
	   	}
	   	async _completed_Orders() {
	   		this.complete_Order();
	   	}
	   	/*end*/
	   	/*Back button click action*/
	   	async _res_Back_Button() {
	   		this.env.pos.db.set_Track_Screen('');
	        this.showScreen("FloorScreen");
	   	}
	   	/*Get the order status - preparing ,pick upto ready,delivery*/
	   	async _order_Status() {
			var orders = self.pos.db.get_Sorder_Sorted(1000);
			var filteredOrders = orders;
			var openOrders = [];
			var confirmOrders = [];
			var prepareOrders = [];
			var pickupOrders = [];
			var today = new moment().format('YYYY-MM-DD'); 
			/*get inprogress orders, payment orders,complete orders and tab values */
    		if (this.value != "all") {
				$('.checkout_orders').removeClass('pos_display_none')
				$('.all_checkout_orders').addClass('pos_display_none')
				self.$('.arrows').addClass("wet_display_none");
				var openContents = document.querySelector('.all_checkout_orders .open_orders');
				openContents.innerHTML = "";
				var confirmContents = document.querySelector('.all_checkout_orders .confirm_orders');
				confirmContents.innerHTML = "";
				var prepareContents = document.querySelector('.all_checkout_orders .prepare_orders');
				prepareContents.innerHTML = "";
				var readyContents = document.querySelector('.all_checkout_orders .ready_orders');
				readyContents.innerHTML = "";  
					            	  
				var firstContents = document.querySelector('.checkout_orders .first_orders');
				firstContents.innerHTML = "";
				var secondContents = document.querySelector('.checkout_orders .second_orders');
				secondContents.innerHTML = "";
				var thirdContents = document.querySelector('.checkout_orders .third_orders');
				thirdContents.innerHTML = "";
				var fourthContents = document.querySelector('.checkout_orders .fourth_orders');
				fourthContents.innerHTML = "";
				  
				var oState = this.value;
				if (this.value === 'open') {
					filteredOrders = $.grep(orders, function (v) {
					return v.state === "draft" && v.website_id || v.state === "sent" && v.write_date >= today && v.website_id;
					});
				} else {
					filteredOrders = $.grep(orders, function (v) {
					return v.state === oState && v.write_date >= today && v.website_id;
					});
				}
	  			var j = 0;
			  	for (var i = 0, len = Math.min(filteredOrders.length,1000); i < len; i++) {
          			var order    = filteredOrders[i];
	         
		          	if (j === 0) {
	        	  		var contents = document.querySelector('.checkout_orders .first_orders');
		          	}
	          		if (j === 1) {
	        	  		var contents = document.querySelector('.checkout_orders .second_orders');
		          	}
		          	if (j === 2) {
	        	 		var contents = document.querySelector('.checkout_orders .third_orders');
		          	}
		          	if (j === 3) {
		        		var contents = document.querySelector('.checkout_orders .fourth_orders');
		          	}
		          	var orderlines = [];
	       	  	 	if (self.env.pos.db.get_Orderline_By_Order(filteredOrders[i].id) != undefined) {
	          			orderlines = self.env.pos.db.get_Orderline_By_Order(filteredOrders[i].id);
	          		}
	              	var sorderlineHtml = QWeb.render('ShopCartOrders',{
								widget: self,
								sorder:filteredOrders[i],
								sorderlines:orderlines,
								slevel:zoomLevel
							});
	            	var sorderline = document.createElement('div');
	        	  	sorderline.innerHTML = sorderlineHtml;
	              	sorderline = sorderline.childNodes[1];
	              	var stateIcon = sorderline.querySelector('.order_btn');
	              	/*state icon button function*/
	              	if (stateIcon) {
		              	stateIcon.addEventListener('click', (function (e) {		
			              	var orderId = e.target.dataset.item;
			              	var orderState = ($("#"+orderId).text()).trim();
			              	self.update_Order_State(orderId, orderState);
		              	}.bind(self)));
	              	}
	              	var deleteIcon = sorderline.querySelector('.del_btn');
	              	/*delete icon button function*/
	              	if (deleteIcon) {
		        	  	deleteIcon.addEventListener('click', (function (e) {
			              	var orderId = e.currentTarget.dataset.item;
			              	self.delete_Order(orderId);
	              		}.bind(self)));
	              	}
	              	var onlineOrderPrint = sorderline.querySelector('.online_order_print');
	           		if (onlineOrderPrint) {
	            		self.online__Print(onlineOrderPrint);
	            	}
		          	if (j === 3) {
	    				j = 0;
		          	} else {
		        		j++;
		          	}
	          		contents.append(sorderline);
      			}
			} else {
          	  	$('.checkout_orders').addClass('pos_display_none')
          	  	$('.all_checkout_orders').removeClass('pos_display_none')
        	  	self.$('.arrows').removeClass("wet_display_none");
        	  	var openContents = document.querySelector('.all_checkout_orders .open_orders');
        	  	openContents.innerHTML = "";
        	  	var confirmContents = document.querySelector('.all_checkout_orders .confirm_orders');
        	  	confirmContents.innerHTML = "";
        	  	var prepareContents = document.querySelector('.all_checkout_orders .prepare_orders');
        	  	prepareContents.innerHTML = "";
        	  	var readyContents = document.querySelector('.all_checkout_orders .ready_orders');
        	  	readyContents.innerHTML = "";  
	            	  
        	    var firstContents = document.querySelector('.checkout_orders .first_orders');
        	    firstContents.innerHTML = "";
        	    var secondContents = document.querySelector('.checkout_orders .second_orders');
        	    secondContents.innerHTML = "";
        	    var thirdContents = document.querySelector('.checkout_orders .third_orders');
        	    thirdContents.innerHTML = "";
        	    var fourthContents = document.querySelector('.checkout_orders .fourth_orders');
        	    fourthContents.innerHTML = "";
	            	    
  	        	openOrders = $.grep(filteredOrders, function (v) {
  	                return v.state === "draft" && v.website_id || v.state === "sent" && v.write_date >= today && v.website_id;
  	            });
  	        	confirmOrders = $.grep(filteredOrders, function (v) {
  	                return v.state === "sale" && v.write_date >= today && v.website_id;
  	            });
  	        	prepareOrders = $.grep(filteredOrders, function (v) {
  	                return v.state === "preparing" && v.write_date >= today && v.website_id ;
  	            });
  	        	pickupOrders = $.grep(filteredOrders, function (v) {
  	                return v.state === "ready" && v.write_date >= today && v.website_id;
  	            });
  	        	var contents = document.querySelector('.all_checkout_orders .open_orders'); 
  	        	/*get open orders count in pos*/
  	        	for (var i = 0, len = Math.min(openOrders.length,1000); i < len; i++) {
  	                var order    = openOrders[i];
                	var orderlines = [];
                	if (self.env.pos.db.get_Orderline_By_Order(openOrders[i].id) != undefined) {
                		orderlines = self.env.pos.db.get_Orderline_By_Order(openOrders[i].id);
                	}
                    var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: self, sorder:order, sorderlines:orderlines, slevel:zoomLevel});
                    var sorderline = document.createElement('div');
                    sorderline.innerHTML = sorderlineHtml;
                    sorderline = sorderline.childNodes[1];
                    var stateIcon = sorderline.querySelector('.order_btn');
                    if (stateIcon) {
                    	stateIcon.addEventListener('click', (function (e) {
                        	var orderId = e.target.dataset.item;
                        	var orderState = ($("#"+orderId).text()).trim();
                        	self.update_Order_State(orderId, orderState);
                        }.bind(self)));
                    }
                    var deleteIcon = sorderline.querySelector('.del_btn');
                    if (deleteIcon) {
                    	deleteIcon.addEventListener('click', (function (e) {
                        	var orderId = e.currentTarget.dataset.item;
                        	self.delete_Order(orderId);
                        }.bind(self)));
                    }	  	                
                	contents.append(sorderline);
	    		}
	        	var contents = document.querySelector('.all_checkout_orders .confirm_orders'); 
	        	for (var i = 0, len = Math.min(confirmOrders.length,1000); i < len; i++) {
		    		var order = confirmOrders[i];
		        	var orderlines = [];
		        	if (self.env.pos.db.get_Orderline_By_Order(confirmOrders[i].id) != undefined) {
		        		orderlines = self.env.pos.db.get_Orderline_By_Order(confirmOrders[i].id);
		        	}
		            var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: this, sorder:order, sorderlines:orderlines, slevel:zoomLevel});
		            var sorderline = document.createElement('div');
		            sorderline.innerHTML = sorderlineHtml;
		            sorderline = sorderline.childNodes[1];
		            var stateIcon = sorderline.querySelector('.order_btn');
		            if (stateIcon) {
		            	stateIcon.addEventListener('click', (function (e) {
		                	var orderId = e.target.dataset.item;
		                	var orderState = ($("#"+orderId).text()).trim();
		                	self.update_Order_State(orderId, orderState);
		                }.bind(self)));
		            }
	                var deleteIcon = sorderline.querySelector('.del_btn');
	                if (deleteIcon) {
	                	deleteIcon.addEventListener('click', (function (e) {
	                    	var orderId = e.currentTarget.dataset.item;
	                    	self.delete_Order(orderId);
	                    }.bind(self)));
	                }
	                var onlineOrderPrint = sorderline.querySelector('.online_order_print');
	                if (onlineOrderPrint) {
	                	self.online__Print(onlineOrderPrint);
	                }
	                contents.append(sorderline);
	            }
	            /*get preparing orders count in pos*/
  	        	var contents = document.querySelector('.all_checkout_orders .prepare_orders'); 
  	        	for (var i = 0, len = Math.min(prepareOrders.length,1000); i < len; i++) {
  	                var order    = prepareOrders[i];
                	var orderlines = [];
                	if (self.env.pos.db.get_Orderline_By_Order(prepareOrders[i].id) != undefined) {
                		orderlines = self.env.pos.db.get_Orderline_By_Order(prepareOrders[i].id);
                	}
                    var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: this, sorder:order, sorderlines:orderlines, slevel:zoomLevel});
                    var sorderline = document.createElement('div');
                    sorderline.innerHTML = sorderlineHtml;
                    sorderline = sorderline.childNodes[1];
                    var stateIcon = sorderline.querySelector('.order_btn');
                    if (stateIcon) {
                    	stateIcon.addEventListener('click', (function (e) {
                        	var orderId = e.target.dataset.item;
                        	var orderState = ($("#"+orderId).text()).trim();
                        	self.update_Order_State(orderId, orderState);
                        }.bind(self)));
                    }
                    var deleteIcon = sorderline.querySelector('.del_btn');
                    if (deleteIcon) {
                    	deleteIcon.addEventListener('click', (function (e) {
                    		
                        	var orderId = e.currentTarget.dataset.item;
                        	self.delete_Order(orderId);
                        	
                        }.bind(self)));
                    }
                    var onlineOrderPrint = sorderline.querySelector('.online_order_print');
                    if (onlineOrderPrint) {
                    	self.online__Print(onlineOrderPrint);
                    }
				 contents.append(sorderline);
  	            }
  	            /*get pickup orders count in pos*/
  	        	var contents = document.querySelector('.all_checkout_orders .ready_orders'); 
  	        	for (var i = 0, len = Math.min(pickupOrders.length,1000); i < len; i++) {
  	                var order    = pickupOrders[i];
                	var orderlines = [];
                	if (self.env.pos.db.get_Orderline_By_Order(pickupOrders[i].id) != undefined) {
                		orderlines = self.env.pos.db.get_Orderline_By_Order(pickupOrders[i].id);
                	}
                    var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: this, sorder:order, sorderlines:orderlines, slevel:zoomLevel});
                    var sorderline = document.createElement('div');
                    sorderline.innerHTML = sorderlineHtml;
                    sorderline = sorderline.childNodes[1];
                    var stateIcon = sorderline.querySelector('.order_btn');
                    if (stateIcon) {
                    	stateIcon.addEventListener('click', (function (e) {
                        	var orderId = e.target.dataset.item;
                        	var orderState = ($("#"+orderId).text()).trim();
                        	self.update_Order_State(orderId, orderState);
                        }.bind(self)));
                    }
                    var deleteIcon = sorderline.querySelector('.del_btn');
                    if (deleteIcon) {
                    	deleteIcon.addEventListener('click', (function (e) {
                        	var orderId = e.currentTarget.dataset.item;
                        	self.delete_Order(orderId);
                        }.bind(self)));
                    }
                    var onlineOrderPrint = sorderline.querySelector('.online_order_print');
                    if (onlineOrderPrint) {
                    	self.online__Print(onlineOrderPrint);
                    }
  	                contents.append(sorderline);
            	}
          	}
	   	}
	    
    	hide() {
        	this._super();
	        if (this.editing) {
	            this.toggle_editing();
	        }
		}
		/*default calling function start*/
	   	mounted() {
	   		var self =this;
   		 	var orders = self.env.pos.db.get_Sorder_Sorted(1000);
	       	this.render_Sorder(orders);
	       	this.order_Timer();
	   	}
		
		willStart() {
	        if (this.env.pos.config.supplier_view || (this.env.pos.config.cashier_view &&  this.startScreen === "SOOrderScreen") || (this.env.pos.config.waiter_view &&  this.startScreen === "SOOrderScreen")) {
	
	        } else {
	        	$('.select-order').css({'visibility': 'hidden'});
	        	$('.neworder-button').css({'visibility': 'hidden'});
	        	$('.deleteorder-button').css({'visibility': 'hidden'});
	        }
	        if (this.env.pos.config.supplier_view) {
	        	$('.top_home_btn').hide();
	        }
       
	        /** Expand and collapse */
	        var acc = document.getElementsByClassName("accordion");
			var i;
			for (i = 0; i < acc.length; i++) {
				acc[i].addEventListener("click", function () {
				    this.classList.toggle("active");
				    var panel = this.nextElementSibling;
				    if (panel.style.display === "inline-flex") {
				      panel.style.display = "none";
				    } else {
				      panel.style.display = "inline-flex";
				    }
				    var total_acc = document.getElementsByClassName("accordion active");
				    if (total_acc.length < 2) {
				    	$('.panel').css({'height': '60vh'})
				    } else {
				    	$('.panel').css({'height': '30vh'})
				    }
			  });
			}       
    	}
    	/*end*/
    	
        /*Set timer for the orders in kitchen and cashier view*/
    	order_Timer() {
		var self = this;
		var orders = this.env.pos.get_order_list();
		setTimeout(function () {
			for (var j = 0; j < orders.length; j++) {
				var seconds = orders[j].get_Order_Sec();
				var minutes = orders[j].get_Order_Min();
				var hours = orders[j].get_Order_Hour();
				seconds++;
			    if (seconds >= 60) {
			    	seconds = 0;
			        minutes++;
			        if (minutes >= 60) {
			            minutes = 0;
			            hours++;
			        }
			    }
			    orders[j].set_Order_Sec(seconds);
				orders[j].set_Order_Min(minutes);
				orders[j].set_Order_Hour(hours);
			    var uid = orders[j].uid;
			   
			    var cHours = (hours ? (hours > 9 ? hours : "0" + hours) : "00")
			    var cMin = (minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00")
			    var cSec = (seconds > 9 ? seconds : "0" + seconds)
	            $('#output'+uid).text(cHours + ":" + cMin + ":" + cSec);
	        }
			self.order_Timer();
		},1000);
        
	}
	    /*Online order details print function*/  
    	online__Print(onlineOrderPrint) {
    		onlineOrderPrint.addEventListener('click', (function (e) {
	        	var orderId = e.target.dataset.order_id;
				var sorder = this.env.pos.db.sorder_by_id[orderId];
				var sorderlines = this.env.pos.db.get_Orderline_By_Order(orderId);
	            Gui.showPopup('OnlineOrderPrint',{
	                    'title': 'Online Order Receipt',
	                    'order_id': orderId,
						'sorder': sorder,
						'sorderlines': sorderlines
                });
			}.bind(this)));
		}
    /*Update the order status function*/  
	    update_Order_State(order_id, order_state) {
	    	var self = this;
	    	if (order_state === "Payment") {
	    		this.rpc({
					model: 'sale.order',
					method: 'get_invoice_details',
					args: [0, order_id],
				}).then(function (result) { 
					self.pos.gui.show_popup('popuppaymentwidget', {
		                'title': _t('Payment'),
		                'journals':result,	
		            });
				});
	    	} else {
		    	this.rpc({
					model: 'sale.order',
					method: 'change_order_state',
					args: [0, order_id, order_state],
				}).then(function () { 
					console.log("Order confirmed");
				});
	    	}
	    }
    /*Update sale order state reverse button function*/  
	    update_Sol_State_Reverse(oline_id,order_id,kitchen_state,e) {
	    	var self = this;
	    	if (oline_id && order_id && kitchen_state) {
	    		if (kitchen_state === 'Confirm' || kitchen_state === 'Open') {
						$(e.currentTarget).closest('li').find('.kitchen_status').text("Cancelled");
						$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("blue-color");
				    	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("confirm_color");
				    	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("red-color");
				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("blue-bgcolor");
				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("confirm_bgcolor");
				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("red-bgcolor");
				    	self.update_Kitchen_State(oline_id,order_id,'cancel');
				} else if (kitchen_state === 'Preparing') {
					$(e.currentTarget).closest('li').find('.kitchen_status').text("Confirm");
			    	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("blue-color");
			    	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("confirm_color");
			    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("blue-bgcolor");
			    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("confirm_bgcolor");
			    	self.update_Kitchen_State(oline_id,order_id,'confirm');
	    		} else if (kitchen_state === 'Ready to Pickup') {
						$(e.currentTarget).closest('li').find('.kitchen_status').text("Preparing");
				    	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("yellow-color");
				    	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("blue-color");
				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("yellow-bgcolor");
				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("blue-bgcolor");
				    	self.update_Kitchen_State(oline_id,order_id,'preparing');
		        } else if (kitchen_state === 'delivered') {
						$(e.currentTarget).closest('li').find('.kitchen_status').text("Ready to Pickup");
				    	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("green-color");
				    	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("yellow-color");
				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("green-bgcolor");
				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("yellow-bgcolor");
				    	self.update_Kitchen_State(oline_id,order_id,'ready');
		        }
	    	}
	    }
	     /*Update sale order state forward button function*/ 
	    update_Sol_State_Forward(oline_id,order_id,kitchen_state,e) {
			/** Change the state comparing value */
	    	var self = this;
	    	if (oline_id && order_id && kitchen_state) {
	    		if (kitchen_state === 'cancel') {
					$(e.currentTarget).closest('li').find('.kitchen_status').text("Open");
	            	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("red-color");
	            	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("blue-color");
	            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("red-bgcolor");
	            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("blue-bgcolor");
	            	self.update_Kitchen_State(oline_id, order_id, 'open');
	        	} else if (kitchen_state === 'open') {
					$(e.currentTarget).closest('li').find('.kitchen_status').text("Confirm");
	            	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("blue-color");
	            	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("confirm_color");
	            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("blue-bgcolor");
	            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("disable_confirm");
	            	self.update_Kitchen_State(oline_id, order_id, 'confirm');
	        	} else if (kitchen_state === 'confirm') {
					$(e.currentTarget).closest('li').find('.kitchen_status').text("Preparing");
	            	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("confirm_color");
	            	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("blue-color");
	            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("confirm_bgcolor");
	            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("blue-bgcolor");
	            	self.update_Kitchen_State(oline_id, order_id, 'preparing');
	        	} else if (kitchen_state === 'preparing') {
					$(e.currentTarget).closest('li').find('.kitchen_status').text("Ready to Pickup");
	            	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("blue-color");
	            	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("yellow-color");
	            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("blue-bgcolor");
	            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("yellow-bgcolor");
	            	self.update_Kitchen_State(oline_id, order_id, 'ready');
	        	} else if (kitchen_state === 'ready' || kitchen_state === 'Ready to Pickup') {
	    			$(e.currentTarget).closest('li').find('.kitchen_status').text("Delivered");
	            	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("yellow-color");
	            	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("green-color");
	            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("yellow-bgcolor");
	            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("green-bgcolor");
	            	self.update_Kitchen_State(oline_id, order_id, 'delivered');
	    		}
	    	}
	    	
	    }
	     /*Update sale order kitchen state function*/ 
	    update_Kitchen_State( oline_id, order_id,sol_state) {
	    	if (oline_id && sol_state) {
	    		
	    		this.rpc({
	    			model: 'sale.order',
	    			method: 'change_sorder_line_state',
	    			args: [0, oline_id,order_id,sol_state],
	    		}).then(function () { 
	    			console.log("Order confirmed");
	    		});
	    	}
	    }
	     /*delete sale orders function*/ 
	    delete_Order(order_id) {
	    	var self = this;
	    	this.gui.show_popup('confirm',{
				'title': _t('Warning'),
				'body': _t('Are you sure want to cancel this order?'),
				confirm: function () {
					self.rpc({
						model: 'sale.order',
						method: 'delete_order',
						args: [0, order_id],
					}).then(function () { 
						console.log("Order Deleted.");
					});
				},
			});
	    }
   
	     /*Update every secound once in kitchen view function*/ 
		update_Sorder_Screen() {
		    this.render_Sorder(this.env.pos.db.get_Sorder_Sorted(1000));
		}
    
    /*****************************/
     /*Update pos order state reverse button function*/ 
    set_Kitchen_Reverse(oline_id,order,e) {
       	var orders = this.env.pos.get_order_list();
  	  	for (var j = 0; j < orders.length; j++) {
  		  var getOrder = orders[j];
  		  getOrder.trigger('new_updates_to_send');
  		  if (getOrder.uid === order) {
  			var orderlines = getOrder.get_orderlines()
  			for (var i = 0; i < orderlines.length; i++) {
  				var getOrderLine = orderlines[i];
  				if (parseInt(getOrderLine.id) === parseInt(oline_id)) {
  					var kitchenState = getOrderLine.get_Kitchen_State();
  					if (kitchenState === 'preparing') {
  						$(e.currentTarget).closest('li').find('.kitchen_status').text("Cancelled");
  				    	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("blue-color");
  				    	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("red-color");
  				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("blue-bgcolor");
  				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("red-bgcolor");
  				    	getOrderLine.set_Kitchen_State('cancel');
  				    	var olines = getOrder.get_orderlines()
  				    	var allCancelOrder = true;
  		        		var cancelOrder = true;
  		        		var cancelOrderLine = false;
  		        		for (var i = 0, len = olines.length; i < len; i++) {
  		        			if (olines[i].get_Kitchen_State() === 'cancel') {
  				            	cancelOrderLine = true;
  				            }
  				            if (olines[i].get_Kitchen_State() != 'cancel') {
  				            	allCancelOrder = false;
  				            	cancelOrder = false;
  				            }
  		        		}
  		        		if (allCancelOrder) {
  		        			getOrder.set_Delivery(false);
  				        }
  				        if (cancelOrderLine) {
  				        	getOrder.set_Cancel_Order_Line(true);
  				        } else {
  				        	getOrder.set_Cancel_Order_Line(false);
  				        }
  				        
  				        if (cancelOrder) {
  				        	$('.orderlines'+getOrder.uid).css({'display': 'none'})
  				        }
  				        /** Finalize the paid delivered order */
  				        if (allCancelOrder) {
  				        	getOrder.set_All_Delivery(true);
  				        }
  					}
  					if (kitchenState === 'ready') {
  						$(e.currentTarget).closest('li').find('.kitchen_status').text("Preparing");
  				    	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("yellow-color");
  				    	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("blue-color");
  				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("yellow-bgcolor");
  				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("blue-bgcolor");
  						getOrderLine.set_Kitchen_State('preparing');
  		        	}
  					if (kitchenState === 'delivered') {
  						$(e.currentTarget).closest('li').find('.kitchen_status').text("Ready to Pickup");
  				    	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("green-color");
  				    	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("yellow-color");
  				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("green-bgcolor");
  				    	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("yellow-bgcolor");
  						getOrderLine.set_Kitchen_State('ready');
  		        	}
  				}
  			}
  		  }
  	  	}
    }
     /*Update pos order state forward button function*/ 
    set_Kitchen_Forward(oline_id,order,e) {
    	var orders = this.env.pos.get_order_list();
    	for (var j = 0; j < orders.length; j++) {
    		  var getOrder = orders[j];
    		  getOrder.trigger('new_updates_to_send');
    		  if (getOrder.uid === order) {
    			var updateDate = false;
	        	if (!getOrder.get_Delivery()) {
	        		updateDate = true;
	        		getOrder.set_Delivery(true);
	        	}
    			var orderlines = getOrder.get_orderlines()
    			for (var i = 0; i < orderlines.length; i++) {
    				var getOrderLine = orderlines[i];
    				if (parseInt(getOrderLine.id) === parseInt(oline_id)) {
    					var kitchenState = getOrderLine.get_Kitchen_State();
    					if (kitchenState === 'cancel') {
    						$(e.currentTarget).closest('li').find('.kitchen_status').text("Preparing");
    		            	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("red-color");
    		            	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("blue-color");
    		            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("red-bgcolor");
    		            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("blue-bgcolor");
    						getOrderLine.set_Kitchen_State('preparing');
    		        	}
    					if (kitchenState === 'preparing') {
    						$(e.currentTarget).closest('li').find('.kitchen_status').text("Ready to Pickup");
    		            	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("blue-color");
    		            	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("yellow-color");
    		            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("blue-bgcolor");
    		            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("yellow-bgcolor");
    						getOrderLine.set_Kitchen_State('ready');
    		        	}
    		        	if (kitchenState === 'ready') {
    		        		$(e.currentTarget).closest('li').find('.kitchen_status').text("Delivered");
    		            	$(e.currentTarget).closest('li').find('.kitchen_status').removeClass("yellow-color");
    		            	$(e.currentTarget).closest('li').find('.kitchen_status').addClass("green-color");
    		            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').removeClass("yellow-bgcolor");
    		            	$(e.currentTarget).closest('li').find('.reverse_view_btn,.forward_view_btn').addClass("green-bgcolor");
    		        		getOrderLine.set_Kitchen_State('delivered');
    		        		var olines = getOrder.get_orderlines()
    		        		var allDeliveryOrder = true;
    			        	var deliveryOrder = true;
    			        	var cancelOrderLine = false;
    		        		for (var i = 0, len = olines.length; i < len; i++) {
					        	var posCategId = olines[i].get_product().pos_categ_id[0];
					            var posCategIds = this.env.pos.config.pos_categ_ids
					            if ($.inArray(posCategId, posCategIds) > -1) {
					            	if (olines[i].get_Kitchen_State() != 'delivered' && olines[i].get_Kitchen_State() != 'cancel') {
					            		deliveryOrder = false;
						            }
					            }
					            if (olines[i].get_Kitchen_State() === 'cancel') {
					            	cancelOrderLine = true;
					            }
					            if (olines[i].get_Kitchen_State() != 'delivered' && olines[i].get_Kitchen_State() != 'cancel') {
					            	allDeliveryOrder = false;
					            }
					            if (updateDate) {
					            	olines[i].set_Delivered_Date(new Date);
					            }
					        }
    		        		if (allDeliveryOrder) {
    		        			getOrder.set_Delivery(false);
    				        }
    		        		if (cancelOrderLine) {
    		        			getOrder.set_Cancel_Order_Line(true);
    				        } else {
    				        	getOrder.set_Cancel_Order_Line(false);
    				        }
    		        		if (deliveryOrder) {
    				        	$('.orderlines'+getOrder.uid).css({'display': 'none'})
    				        }
    		        		/** Finalize the paid delivered order */
    				        if (allDeliveryOrder) {
    				        	getOrder.set_All_Delivery(true);
    				        }
		        	 	}
    				}
    			}
		  	}
	  	}
    }
    /****************************/
     /*render sale order and pos order function*/ 
   	render_Sorder(sorders) {
    	var self = this;
        var stateValue = $("#order_status option:selected").val();
        var orders = sorders;
        var openOrders = [];
        var confirmOrders = [];
        var prepareOrders = [];
        var pickupOrders = [];
        var today = new moment().format('YYYY-MM-DD');
        if (stateValue != undefined && stateValue != "") {
		/*get all tab values- payment orders,inprogress orders and complete orders */
	        if (stateValue === "all") {
	        	var openContents = document.querySelector('.all_checkout_orders .open_orders');
          	    openContents.innerHTML = "";
          	    var confirmContents = document.querySelector('.all_checkout_orders .confirm_orders');
          	    confirmContents.innerHTML = "";
          	    var prepareContents = document.querySelector('.all_checkout_orders .prepare_orders');
          	    prepareContents.innerHTML = "";
          	    var readyContents = document.querySelector('.all_checkout_orders .ready_orders');
          	    readyContents.innerHTML = "";

	        	var firstContents = document.querySelector('.checkout_orders .first_orders');
	        	firstContents.innerHTML = "";
          	    var secondContents = document.querySelector('.checkout_orders .second_orders');
          	    secondContents.innerHTML = "";
          	    var thirdContents = document.querySelector('.checkout_orders .third_orders');
          	    thirdContents.innerHTML = "";
          	    var fourthContents = document.querySelector('.checkout_orders .fourth_orders');
          	    fourthContents.innerHTML = "";
	        	
	        	openOrders = $.grep(sorders, function (v) {
	                return ((v.state === "draft" && v.website_id && v.write_date >= today) || (v.state === "sent" && v.write_date >= today && v.website_id));
	            });
	        	confirmOrders = $.grep(sorders, function (v) {
	                return v.state === "sale" && v.write_date >= today && v.website_id;
	            });
	        	prepareOrders = $.grep(sorders, function (v) {
	                return v.state === "preparing" && v.write_date >= today && v.website_id;
	            });
	        	pickupOrders = $.grep(sorders, function (v) {
	                return v.state === "ready" && v.write_date >= today && v.website_id;
	            });
	        	
	        	/*********************/
	        	var restaurantContents = document.querySelector('.all_pos_orders .restaurant_orders');
        	    restaurantContents.innerHTML = "";
        	    
        	    
          	  /*******************/
        	    var orders = self.env.pos.get_order_list();
        	    /*Get the pos orders lines one by one to push cashier, waiter and kitchen view*/
          	  	for (var j = 0; j < orders.length; j++) {
          		  var order = orders[j];
          		  var contents = document.querySelector('.all_pos_orders .restaurant_orders');
          		  var orderlines = order.get_orderlines();
          		  var categOrderlines = []
          		  var showOrder = true;
          		  var isState = false;
          		  	for (var i = 0, len = orderlines.length; i < len; i++) {
            			var posCategId = orderlines[i].get_product().pos_categ_id[0];
		            	var posCategIds = this.env.pos.config.pos_categ_ids
		            	if ($.inArray(posCategId, posCategIds) > -1) {
		            		if (orderlines[i].get_Kitchen_State() != undefined) {
			            		if (orderlines[i].get_Kitchen_State() != 'delivered' && orderlines[i].get_Kitchen_State() != 'cancel') {
				            		categOrderlines.push(orderlines[i])
				            	}
		            		}
		            		if (orderlines[i].get_Kitchen_State()=== undefined && !isState) {
		            			showOrder = false;
		            		} else {
		            			isState = true;
		            		}
		                }
			        }
	          		  // Display only confirmed order and lines
          		    if (showOrder) {
          		  		var porderlineHtml  = QWeb.render('RestaurantOrders',{widget:this, order:order, orderlines:categOrderlines, slevel:zoomLevel});
	          		  	var porderline = document.createElement('div');
	          		 	porderline.innerHTML = porderlineHtml;
		          		porderline = porderline.childNodes[1];
		          		var reverseIcon  = porderline.querySelectorAll('.reverse_view_btn');
		          		if (reverseIcon) {
				  		  	for (var i = 0; i < reverseIcon.length; i++) {
		    	        	reverseIcon[i].addEventListener('click', (function (e) {
		    	        		e.preventDefault();
		    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
		    	        		var order = $(e.currentTarget).closest('ul').attr('data-uid');
		    	        		this.set_Kitchen_Reverse(olineID,order,e);
		    	            }.bind(this)));
	          			}
	          		}
		          		  
          		  	var posLinePrint = porderline.querySelectorAll('.pos_orderline_print');
          		  	/*Print pos order lines*/
      		 	 	if (posLinePrint) {
          		  		for (var i = 0; i < posLinePrint.length; i++) {
          					posLinePrint[i].addEventListener('click', (function (e) {
		    	        		e.preventDefault();
		    	        		var lineId = $(e.currentTarget).attr('line_id');
		    	        		var orderUid = $(e.currentTarget).attr('order_uid');
	    	        			this.showPopup('POSLinePrintPopupWidget',{
				    	            'title': _t('POS Order Line Receipt '),
				    	            'line_id': lineId,
				    	            'order_uid': orderUid,
				    	    	});
	    	            	}.bind(this)));
          				}
          		  	}
		          		  
          		  	var forwardIcon = porderline.querySelectorAll('.forward_view_btn');
          		  	/*pos order forwardIcon function*/
          			if (forwardIcon) {
          				for (var i = 0; i < forwardIcon.length; i++) {
	          				forwardIcon[i].addEventListener('click', (function (e) {
		    	        		e.preventDefault();
		    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
		    	        		var order = $(e.currentTarget).closest('ul').attr('data-uid');
		    	        		this.set_Kitchen_Forward(olineID,order,e);
		    	            }.bind(this)));
          				}
          		  	}
          		  	contents.append(porderline);
          		  	var isCategOrder = false;
      		  		for (var i = 0, len = orderlines.length; i < len; i++) {
          				if (orderlines[i].get_Kitchen_State() != 'delivered' && orderlines[i].get_Kitchen_State() != 'cancel') {
            				isCategOrder = true;
	            		}
          		  	}
	          	  	if (!isCategOrder) {
          		  		if (porderline.querySelector('.orderlines'+orders[j].uid) != null) {
	          				porderline.querySelector('.orderlines'+orders[j].uid).remove();
          		  		}
		          	}
      		  	}
      	  	}

      	   /* Open Order */
        	var contents = document.querySelector('.all_checkout_orders .open_orders'); 
        	for (var i = 0, len = Math.min(openOrders.length,1000); i < len; i++) {
                var order    = openOrders[i];
                if (order.website_id) {
					orderlines = this.env.pos.db.get_Orderline_By_Order(openOrders[i].id);
            		var categOrderlines = []
            		/*Open Order - Get the sale orders lines one by one to push cashier, waiter and kitchen view*/
            		for (var j = 0; j < orderlines.length; j++) {
            			var productId = orderlines[j].product_id[0];
            			var product = this.env.pos.db.get_product_by_id(productId);
            			var posCategId = 0
            			// Check product available in POS
						if (this.env.pos.db.get_product_by_id(productId) === undefined || this.env.pos.db.get_product_by_id(productId) == null) {
							if (orderlines[j].kitchen_state != 'delivered') {
			            		categOrderlines.push(orderlines[j])
			            	}
						} else {
							var posCategId = this.env.pos.db.get_product_by_id(productId).pos_categ_id[0];
			            	var posCategIds = this.env.pos.config.pos_categ_ids
			            	if ($.inArray(posCategId, posCategIds) > -1) {
			            		if (orderlines[j].kitchen_state != 'delivered') {
				            		categOrderlines.push(orderlines[j])
				            	}
							}
						}
						
  		            }
                    var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: this, sorder:order, sorderlines:categOrderlines, slevel:zoomLevel});
                    var sorderline = document.createElement('div');
                    sorderline.innerHTML = sorderlineHtml;
                    sorderline = sorderline.childNodes[1];
                    var stateIcon = sorderline.querySelector('.order_btn');
                    /*Open Order - order state icon button in sale order*/
                    if (stateIcon) {
                    	stateIcon.addEventListener('click', (function (e) {
                        	var orderId = e.target.dataset.item;
                        	var orderState = ($("#"+orderId).text()).trim();
                        	this.update_Order_State(orderId, orderState);
                        }.bind(this)));
                    }
                    var deleteIcon = sorderline.querySelector('.del_btn');
                    /*Open Order -order delete icon button in sale order*/
                    if (deleteIcon) {
                    	deleteIcon.addEventListener('click', (function (e) {
                        	var orderId = e.currentTarget.dataset.item;
                        	this.delete_Order(orderId);
                        }.bind(this)));
                    }
                    var soReverseIcon  = sorderline.querySelectorAll('.reverse_view_btn');
                    /*Open Order - Reverse icon button click action in sale order*/
            		if (soReverseIcon) {
            			for (var k = 0; k < soReverseIcon.length; k++) {
            				soReverseIcon[k].addEventListener('click', (function (e) {
	  	    	        		e.preventDefault();
	  	    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
	  	    	        		var orderID = $(e.currentTarget).closest('ul').attr('data-uid');
    	    	        		var olState = ($(e.currentTarget).closest('li').find('.kitchen_status').text()).trim();
	  	    	        		this.update_Sol_State_Reverse(olineID,orderID,olState,e);
  	    	            	}.bind(this)));
            			}
            		}
            		/*Open Order - Forward icon button click action in sale order*/
                    var soForwardIcon = sorderline.querySelectorAll('.forward_view_btn'); 
            		if (soForwardIcon) {
            			for (var l = 0; l < soForwardIcon.length; l++) {
            				soForwardIcon[l].addEventListener('click', (function (e) {
	  	    	        		e.preventDefault();
	  	    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
	  	    	        		var orderId = $(e.currentTarget).closest('ul').attr('data-uid');
	  	    	        		var olState = ($(e.currentTarget).closest('li').find('.kitchen_status').attr('data-state')); //change the statua value
	  	    	        		this.update_Sol_State_Forward(olineID,orderId,olState,e);
	  	    	            }.bind(this)));
            			}
            		}
                }
                contents.append(sorderline);
            }
        	/* Confirm Order */
        	var contents = document.querySelector('.all_checkout_orders .confirm_orders'); 
        	for (var i = 0, len = Math.min(confirmOrders.length,1000); i < len; i++) {
                var order = confirmOrders[i];
                if (order.website_id) {
                	var orderlines = [];
                	if (this.env.pos.db.get_Orderline_By_Order(confirmOrders[i].id) != undefined) {
                		orderlines = this.env.pos.db.get_Orderline_By_Order(confirmOrders[i].id);
                	}
                	var categOrderlines = []
                	/*Get confirm order list count in sale order*/
            		for (var j = 0; j < orderlines.length; j++) {
            			var productId = orderlines[j].product_id[0];
            			var product = this.env.pos.db.get_product_by_id(productId);
            			var posCategId = 0
            			// Check product available in POS
						if (this.env.pos.db.get_product_by_id(productId) === undefined || this.env.pos.db.get_product_by_id(productId) == null) {
							if (orderlines[j].kitchen_state != 'delivered') {
				            	categOrderlines.push(orderlines[j])
				            }
						} else {
							var posCategId = this.env.pos.db.get_product_by_id(productId).pos_categ_id[0];
			            	var posCategIds = this.env.pos.config.pos_categ_ids
			            	if ($.inArray(posCategId, posCategIds) > -1) {
			            		if (orderlines[j].kitchen_state != 'delivered') {
				            		categOrderlines.push(orderlines[j])
				            	}
							}
						}
  		            }
                    var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: this, sorder:order, sorderlines:categOrderlines, slevel:zoomLevel});
                    var sorderline = document.createElement('div');
                    sorderline.innerHTML = sorderlineHtml;
                    sorderline = sorderline.childNodes[1];
                    var stateIcon = sorderline.querySelector('.order_btn');
                    /*confirm order  - order state icon button in sale order*/
                    if (stateIcon) {
                    	stateIcon.addEventListener('click', (function (e) {
                        	var orderId = e.target.dataset.item;
                        	var orderState = ($("#"+orderId).text()).trim();
                        	this.update_Order_State(orderId, orderState);
                        }.bind(this)));
                    }
                    var deleteIcon = sorderline.querySelector('.del_btn');
                    /*confirm order  - delete order icon button in sale order*/
                    if (deleteIcon) {
                    	deleteIcon.addEventListener('click', (function (e) {
                        	var orderId = e.currentTarget.dataset.item;
                        	this.delete_Order(orderId);
                        }.bind(this)));
                    }
                    var onlineOrderPrint = sorderline.querySelector('.online_order_print');
                    /*confirm order  - order lines print in sale order*/
                    if (onlineOrderPrint) {
                    	self.online__Print(onlineOrderPrint);
                    }
                    /*confirm order  - reverse icon button in sale order*/
                    var soReverseIcon  = sorderline.querySelectorAll('.reverse_view_btn');
            		if (soReverseIcon) {
            			for (var k = 0; k < soReverseIcon.length; k++) {
            				soReverseIcon[k].addEventListener('click', (function(e) {
	  	    	        		e.preventDefault();
	  	    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
	  	    	        		var orderID = $(e.currentTarget).closest('ul').attr('data-uid');
	  	    	        		var olState = ($(e.currentTarget).closest('li').find('.kitchen_status').text()).trim();
	  	    	        		this.update_Sol_State_Reverse(olineID,orderID,olState,e);
	  	    	            }.bind(this)));
            			}
            		}

                    var soForwardIcon = sorderline.querySelectorAll('.forward_view_btn');
                     /*confirm order  - Forward icon button in sale order*/
            		if (soForwardIcon) {
            			for (var l = 0; l < soForwardIcon.length; l++) {
            				soForwardIcon[l].addEventListener('click', (function (e) {
	  	    	        		e.preventDefault();
  	    	        		    var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
	  	    	        		var orderId = $(e.currentTarget).closest('ul').attr('data-uid');
	  	    	        		var olState = ($(e.currentTarget).closest('li').find('.kitchen_status').attr('data-state')); //change the statua value
	  	    	        		this.update_Sol_State_Forward(olineID,orderId,olState,e);
	  	    	            }.bind(this)));
            			}
            		}
                }
                contents.append(sorderline);
            }
	        	/* Preparing Order */
        	var contents = document.querySelector('.all_checkout_orders .prepare_orders'); 
        	for (var i = 0, len = Math.min(prepareOrders.length,1000); i < len; i++) {
                var order    = prepareOrders[i];               
                if (order.website_id) {
                	var orderlines = [];
                	if (this.env.pos.db.get_Orderline_By_Order(prepareOrders[i].id) != undefined) {
                		orderlines = this.env.pos.db.get_Orderline_By_Order(prepareOrders[i].id);
                	}
                	var categOrderlines = []
                	/*Get Preparing order list count in  order*/
            		for (var j = 0; j < orderlines.length; j++) {
            			var productId = orderlines[j].product_id[0];
            			var product = this.env.pos.db.get_product_by_id(productId);
            			var posCategId = 0
            			// Check product available in POS
						if (this.env.pos.db.get_product_by_id(productId) === undefined || this.env.pos.db.get_product_by_id(productId) == null) {
							if (orderlines[j].kitchen_state != 'delivered') {
	  			            	categOrderlines.push(orderlines[j])
	  			            }
						} else {
							var posCategId = this.env.pos.db.get_product_by_id(productId).pos_categ_id[0];
			            	var posCategIds = this.env.pos.config.pos_categ_ids
			            	if ($.inArray(posCategId, posCategIds) > -1) {
	  		            		if (orderlines[j].kitchen_state != 'delivered') {
	  			            		categOrderlines.push(orderlines[j])
	  			            	}
							}
						}
  		            }
                    var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: this, sorder:order, sorderlines:categOrderlines, slevel:zoomLevel});
                    var sorderline = document.createElement('div');
                    sorderline.innerHTML = sorderlineHtml;
                    sorderline = sorderline.childNodes[1];
                    var stateIcon = sorderline.querySelector('.order_btn');
                    /*Preparing order  - order state icon button in order*/
                    if (stateIcon) {
                    	stateIcon.addEventListener('click', (function (e) {
                        	var orderId = e.target.dataset.item;
                        	var orderState = ($("#"+orderId).text()).trim();
                        	this.update_Order_State(orderId, orderState);
	                    }.bind(this)));
                    }
                    var deleteIcon = sorderline.querySelector('.del_btn');
                    /*Preparing order  - delete order icon button in order*/
                    if (deleteIcon) {
                    	deleteIcon.addEventListener('click', (function (e) {
                        	var orderId = e.currentTarget.dataset.item;
                        	this.delete_Order(orderId);
                        }.bind(this)));
                    }
                    var onlineOrderPrint = sorderline.querySelector('.online_order_print');
                    /*Preparing order  - order lines print in order*/
                    if (onlineOrderPrint) {
                    	self.online__Print(onlineOrderPrint);
                    }
                    var soReverseIcon  = sorderline.querySelectorAll('.reverse_view_btn');
                    /*Preparing order  - reverse icon button in order*/
            		if (soReverseIcon) {
            			for (var k = 0; k < soReverseIcon.length; k++) {
            				soReverseIcon[k].addEventListener('click', (function (e) {
	  	    	        		e.preventDefault();
	  	    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
	  	    	        		var orderID = $(e.currentTarget).closest('ul').attr('data-uid');
	  	    	        		var olState = ($(e.currentTarget).closest('li').find('.kitchen_status').text()).trim();
	  	    	        		this.update_Sol_State_Reverse(olineID,orderID,olState,e);
	  	    	            }.bind(this)));
            			}
            		}
                    
                    var soForwardIcon = sorderline.querySelectorAll('.forward_view_btn');
                    /*Preparing order  - Forward icon button in order*/
            		if (soForwardIcon) {
            			for (var l = 0; l < soForwardIcon.length; l++) {
            				soForwardIcon[l].addEventListener('click', (function (e) {
	  	    	        		e.preventDefault();
	  	    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
	  	    	        		var orderId = $(e.currentTarget).closest('ul').attr('data-uid');
	  	    	        		var olState = ($(e.currentTarget).closest('li').find('.kitchen_status').attr('data-state')); //change the statua value
	  	    	        		this.update_Sol_State_Forward(olineID,orderId,olState,e);
	  	    	            }.bind(this)));
            			}
        		 	}
                }
            	contents.append(sorderline);
        	}
	        	
        	/* Ready to Pickeup Order */
        	var contents = document.querySelector('.all_checkout_orders .ready_orders'); 
        	for (var i = 0, len = Math.min(pickupOrders.length,1000); i < len; i++) {
                var order= pickupOrders[i];	               
                if (order.website_id) {
                	var orderlines = [];
                	if (this.env.pos.db.get_Orderline_By_Order(pickupOrders[i].id) != undefined) {
                		orderlines = this.env.pos.db.get_Orderline_By_Order(pickupOrders[i].id);
                	}
                	var categOrderlines = []
                	/*Get Ready to Pickeup order list count in order*/
            		for (var j = 0; j < orderlines.length; j++) {
            			var productId = orderlines[j].product_id[0];
            			var product = this.env.pos.db.get_product_by_id(productId);
            			var posCategId = 0
            			// Check product available in POS
						if (this.env.pos.db.get_product_by_id(productId) === undefined || this.env.pos.db.get_product_by_id(productId) == null) {
							if (orderlines[j].kitchen_state != 'delivered') {
				            	categOrderlines.push(orderlines[j])
				            }
						} else {
							var posCategId = this.env.pos.db.get_product_by_id(productId).pos_categ_id[0];
			            	var posCategIds = this.env.pos.config.pos_categ_ids
			            	if ($.inArray(posCategId, posCategIds) > -1) {
			            		if (orderlines[j].kitchen_state != 'delivered') {
				            		categOrderlines.push(orderlines[j])
				            	}
							}
						}
  		            }
                    var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: this, sorder:order, sorderlines:categOrderlines, slevel:zoomLevel});
                    var sorderline = document.createElement('div');
                    sorderline.innerHTML = sorderlineHtml;
                    sorderline = sorderline.childNodes[1];
                    var stateIcon = sorderline.querySelector('.order_btn');
                    /*Preparing order  - order state icon button in order*/
                    if (stateIcon) {
                    	stateIcon.addEventListener('click', (function (e) {
                        	var orderId = e.target.dataset.item;
                        	var orderState = ($("#"+orderId).text()).trim();
                        	this.update_Order_State(orderId, orderState);
                        }.bind(this)));
                    }
                    var deleteIcon = sorderline.querySelector('.del_btn');
                    /*Ready to Pickeup order  - delete order icon button in order*/
                    if (deleteIcon) {
                    	deleteIcon.addEventListener('click', (function (e) {
                        	var orderId = e.currentTarget.dataset.item;
                        	this.delete_Order(orderId);
                        }.bind(this)));
                    }
                    var onlineOrderPrint = sorderline.querySelector('.online_order_print');
                    /*Ready to Pickeup order  - order lines print in order*/
                    if (onlineOrderPrint) {
                    	self.online__Print(onlineOrderPrint);
                    }
                    var soReverseIcon  = sorderline.querySelectorAll('.reverse_view_btn');
                    /*Ready to Pickeup order  - reverse icon button in order*/
            		if (soReverseIcon) {
            			for (var k = 0; k < soReverseIcon.length; k++) {
            				soReverseIcon[k].addEventListener('click', (function (e) {
		    	        		e.preventDefault();
		    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
		    	        		var orderID = $(e.currentTarget).closest('ul').attr('data-uid');
		    	        		var olState = ($(e.currentTarget).closest('li').find('.kitchen_status').text()).trim();
		    	        		this.update_Sol_State_Reverse(olineID,orderID,olState,e);
		    	            }.bind(this)));
            			}
        			}
                    
                    var soForwardIcon = sorderline.querySelectorAll('.forward_view_btn');
                    /*Ready to Pickeup order  - Forward icon button in order*/
            		if (soForwardIcon) {
            			for (var l = 0; l < soForwardIcon.length; l++) {
            				soForwardIcon[l].addEventListener('click', (function (e) {
	  	    	        		e.preventDefault();
	  	    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
	  	    	        		var orderId = $(e.currentTarget).closest('ul').attr('data-uid');
	  	    	        		var olState = ($(e.currentTarget).closest('li').find('.kitchen_status').attr('data-state')); //change the statua value
	  	    	        		this.update_Sol_State_Forward(olineID,orderId,olState,e);
	  	    	            }.bind(this)));
            			}
        		 	}
                }
                contents.append(sorderline);
			}
        } else {
        	var firstContents = document.querySelector('.checkout_orders .first_orders');
        	firstContents.innerHTML = "";
      	    var secondContents = document.querySelector('.checkout_orders .second_orders');
      	    secondContents.innerHTML = "";
      	    var thirdContents = document.querySelector('.checkout_orders .third_orders');
      	    thirdContents.innerHTML = "";
      	    var fourthContents = document.querySelector('.checkout_orders .fourth_orders');
      	    fourthContents.innerHTML = "";

        	var openContents = document.querySelector('.all_checkout_orders .open_orders');
      	    openContents.innerHTML = "";
      	    var confirmContents = document.querySelector('.all_checkout_orders .confirm_orders');
      	    confirmContents.innerHTML = "";
      	    var prepareContents = document.querySelector('.all_checkout_orders .prepare_orders');
      	    prepareContents.innerHTML = "";
      	    var readyContents = document.querySelector('.all_checkout_orders .ready_orders');
      	    readyContents.innerHTML = "";
        	if (stateValue != undefined && stateValue != "") {
	/*not get all tab values- payment orders,inprogress orders and complete orders */
    	        if (stateValue != "all") {
    	      	  	if (stateValue === 'open') {
    	      		orders = $.grep(sorders, function (v) {
                		return v.state === "draft" || v.state === "sent" && v.write_date >= today;
	                });
	      	  		} else {
    	      		orders = $.grep(sorders, function (v) {
	                    return v.state === stateValue && v.write_date >= today;
	                });
    	      	  	}
    	        }
            }
        	var j = 0;
            for (var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
                var order    = orders[i];
                var sorderline = this.sorder_cache.get_node(order.id);
               
                if (j === 0) {
            	  	var contents = document.querySelector('.checkout_orders .first_orders');
              	}
              	if (j === 1) {
            		var contents = document.querySelector('.checkout_orders .second_orders');
	            }
	            if (j === 2) {
	            	var contents = document.querySelector('.checkout_orders .third_orders');
	            }
                if (j === 3) {
                	var contents = document.querySelector('.checkout_orders .fourth_orders');
                 }
            	if (!sorderline) {
            		var orderlines = [];
                	if (this.pos.db.get_Orderline_By_Order(orders[i].id) != undefined) {
                		orderlines = this.pos.db.get_Orderline_By_Order(orders[i].id);
                	}
                	var categOrderlines = []
            		for (var k = 0; k < orderlines.length; k++) {
            			var productId = orderlines[k].product_id[0];
            			var product = this.pos.db.get_product_by_id(productId);
            			var posCategId = 0
            			// Check product available in POS
            			if (product !=undefined) {
            				posCategId = 	product.pos_categ_id[0];
            			}
  		            	var posCategIds = this.pos.config.pos_categ_ids;
  		            	if ($.inArray(posCategId, posCategIds) > -1) {
  		            		if (orderlines[k].kitchen_state != 'delivered') {
  			            		categOrderlines.push(orderlines[k])
  			            	}
  		                }
  		            }
                    var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: this, sorder:orders[i], sorderlines:categOrderlines, slevel:zoomLevel});
                    var sorderline = document.createElement('div');
                    sorderline.innerHTML = sorderlineHtml;
                    sorderline = sorderline.childNodes[1];
                    this.sorder_cache.cache_node(order.id,sorderline);
                    var stateIcon = sorderline.querySelector('.order_btn');
                    /*State Icon button function*/
                    if (stateIcon) {
                    	stateIcon.addEventListener('click', (function (e) {
                        	var orderId = e.target.dataset.item;
                        	var orderState = ($("#"+orderId).text()).trim();
                        	this.update_Order_State(orderId, orderState);
                        	
                        }.bind(this)));
                    }
                    var deleteIcon = sorderline.querySelector('.del_btn');
                    /*delete Icon button function*/
                    if (deleteIcon) {
                    	deleteIcon.addEventListener('click', (function(e) {
                        	var orderId = e.currentTarget.dataset.item;
                        	this.delete_Order(orderId);
                        }.bind(this)));
                    }
                    var onlineOrderPrint = sorderline.querySelector('.online_order_print');
                    /*print order lines function*/
                    if (onlineOrderPrint) {
                    	self.online__Print(onlineOrderPrint);
                    }
                    var soReverseIcon  = sorderline.querySelectorAll('.reverse_view_btn');
                    /*reverse Icon button function*/
            		if (soReverseIcon) {
            			for (var l = 0; l < soReverseIcon.length; l++) {
            				soReverseIcon[l].addEventListener('click', (function (e) {
	  	    	        		e.preventDefault();
	  	    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
	  	    	        		var orderID = $(e.currentTarget).closest('ul').attr('data-uid');
	  	    	        		var olState = ($(e.currentTarget).closest('li').find('.kitchen_status').text()).trim();
	  	    	        		this.update_Sol_State_Reverse(olineID,orderID,olState,e);
	  	    	            }.bind(this)));
            			}
            		}
                    
                    var soForwardIcon = sorderline.querySelectorAll('.forward_view_btn');
                    /*Forward Icon button function*/
            		if (soForwardIcon) {
            			for (var m = 0; m < soForwardIcon.length; m++) {
            				soForwardIcon[m].addEventListener('click', (function(e) {
	  	    	        		e.preventDefault();
	  	    	        		var olineID = $(e.currentTarget).closest('li').attr('data-line-id');
	  	    	        		var orderId = $(e.currentTarget).closest('ul').attr('data-uid');
	  	    	        		var olState = ($(e.currentTarget).closest('li').find('.kitchen_status').attr('data-state')) //change the statua value
	  	    	        		this.update_Sol_State_Forward(olineID,orderId,olState,e);
	  	    	            }.bind(this)));
        				}
        		 	}
                  
    			}
                if (j === 3) {
            	  	j = 0;
                } else {
            	  	j++;
                }
                contents.append(sorderline);
        	}
    	}
		} else {
	    	var activeTab = this.env.pos.db.get_Active_Tab();
	    	if (activeTab === 'complete') {
	    		this.complete_Order();
	    	} else if (activeTab === 'inprogress') {
	    		this.inprogress_Order();
	    	} else {
	    		$("#payment_orders_span").css('background-color', '#4a90cc');
	            $("#inprogress_orders_span").css('background-color', '#ffffff');
	            $("#completed_orders_span").css('background-color', '#ffffff');
	            this.payment_Order();
	    	}
    	}
    }
    /******start code - inprogress orders and tab design code******/
    inprogress_Order() {
    	var self = this;
    	$('.comp_search').addClass('wet_display_none');
    	$('.comp_search_box').val('');
    	var deliveredContents = document.querySelector('.all_pos_orders .cashier_orders');
		if (deliveredContents != null && deliveredContents != undefined) {
			deliveredContents.innerHTML = "";
		}
    	var inprogressContents = document.querySelector('.all_pos_orders .restaurant_orders');
		if (inprogressContents != null && inprogressContents != undefined) {
			inprogressContents.innerHTML = "";
		}
    	$("#payment_orders_span").css('background-color', '#FFFFFF');
    	$("#completed_orders_span").css('background-color', '#ffffff');
    	$("#payment_orders_span").removeClass('com_active');
    	$("#completed_orders_span").removeClass('com_active');
    	$("#inprogress_orders_span").css('background-color', '#4a90cc');
    	self.env.pos.db.set_Active_Tab('inprogress');
    	$('.cashier_orders').css({'width': '0%'});
    	$('.restaurant_orders').css({'width': '100%'});
    	var inprogressOrders = self.env.pos.get_order_list();
    	/*Get inprogress order lines count*/
    	for (var k = 0; k < inprogressOrders.length; k++) {
    		var inprogressOrder = inprogressOrders[k];
    		var inprogressOlines = inprogressOrder.get_orderlines();
    		var inprogressOrderlines = []
    		var showInprogressOrder = true;
    		var isPendingState = false;
    		for (var m = 0; m < inprogressOlines.length; m++) {
    			var lnState = inprogressOlines[m];
    			var olineState = lnState.get_Kitchen_State();
    			if (olineState != undefined) {
	    			if (olineState != 'delivered' && olineState != 'cancel') {
	    				inprogressOrderlines.push(inprogressOlines[m])
			        }
    			}
    			if (olineState === undefined && !isPendingState) {
    				showInprogressOrder = false;
        		} else {
        			isPendingState = true;
        		}
    		}
    		/*Show inprogress order lines */
    		if (showInprogressOrder) {
    			var porderlineHtml  = QWeb.render('RestaurantOrders',{widget:self, order:inprogressOrder, orderlines:inprogressOrderlines, slevel:zoomLevel});
    			var porderLine = document.createElement('div');
    			if (porderlineHtml != null && porderlineHtml != undefined) {
					porderLine.innerHTML = porderlineHtml;
	    			porderLine = porderLine.childNodes[1];
					if (inprogressContents != null && inprogressContents != undefined) {
						inprogressContents.append(porderLine);
					}
				}
    		}
    	}
    	//start
    	var firstContents = document.querySelector('.checkout_orders .first_orders');
		if (firstContents != null && firstContents != undefined) {
			firstContents.innerHTML = "";
		}
  	    var secondContents = document.querySelector('.checkout_orders .second_orders');
		if (secondContents != null && secondContents != undefined) {
			secondContents.innerHTML = "";
		}
  	    var thirdContents = document.querySelector('.checkout_orders .third_orders');
		if (thirdContents != null && thirdContents != undefined) {
			thirdContents.innerHTML = "";
		}
  	    var fourthContents = document.querySelector('.checkout_orders .fourth_orders');
		if (fourthContents != null && fourthContents != undefined) {
			fourthContents.innerHTML = "";
		}

    	var openContents = document.querySelector('.all_checkout_orders .open_orders');
		if (openContents != null && openContents != undefined) {
			openContents.innerHTML = "";
		}
  	    var confirmContents = document.querySelector('.all_checkout_orders .confirm_orders');
		if (confirmContents != null && confirmContents != undefined) {
			confirmContents.innerHTML = "";
		}
  	    var prepareContents = document.querySelector('.all_checkout_orders .prepare_orders');
		if (prepareContents != null && prepareContents != undefined) {
			prepareContents.innerHTML = "";
		}
  	    var readyContents = document.querySelector('.all_checkout_orders .ready_orders');
		if (readyContents != null && readyContents != undefined) {
			readyContents.innerHTML = "";
		}
    	
  	    var j = 0;
	  	var orders = self.env.pos.db.get_Sorder_Sorted(1000);
	  	var filteredOrders = orders;
	    var today = new moment().format('YYYY-MM-DD');   	  	
	  	filteredOrders = $.grep(orders, function (v) {
	  		return v.state != "payment" && v.state != 'delivered' && v.write_date >= today && v.website_id;
	    });
	  	for (var i = 0, len = Math.min(filteredOrders.length,1000); i < len; i++) {
		  	if (j === 0) {
			  	var contents = document.querySelector('.checkout_orders .first_orders');
		  	}
		  	if (j === 1) {
			  	var contents = document.querySelector('.checkout_orders .second_orders');
		  	}
		  	if (j === 2) {
		 	 	var contents = document.querySelector('.checkout_orders .third_orders');
		  	}
		  	if (j === 3) {
			  	var contents = document.querySelector('.checkout_orders .fourth_orders');
		  	}
		  	var orderlines = [];
		  	if (self.env.pos.db.get_Orderline_By_Order(filteredOrders[i].id) != undefined) {
			 	orderlines = self.env.pos.db.get_Orderline_By_Order(filteredOrders[i].id);
		  	}      	
	      	var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: self, sorder:filteredOrders[i], sorderlines:orderlines, slevel:zoomLevel});
	  		var sorderline = document.createElement('div');
	      	if (sorderline != null && sorderline != undefined){
				sorderline.innerHTML = sorderlineHtml;
		      	sorderline = sorderline.childNodes[1];
		      	var stateIcon = sorderline.querySelector('.order_btn');
		      	/*Inprogress order - State icon button click action*/
		      	if (stateIcon) {
		      		stateIcon.addEventListener('click', (function (e) {
			          	var orderId = e.target.dataset.item;
			          	var orderState = ($("#"+orderId).text()).trim();
			          	self.update_Order_State(orderId, orderState);
		          	
		          	}.bind(this)));
		      	}
		      	var deleteIcon = sorderline.querySelector('.del_btn');
		      	/*Inprogress order - delete icon button click action*/
		      	if (deleteIcon) {
		      		deleteIcon.addEventListener('click', (function (e) {
		          		var orderId = e.currentTarget.dataset.item;
		          		self.delete_Order(orderId);
		          	
		          	}.bind(this)));
		      	}
			}
			
	  		if (self.env.pos.db.get_Orderline_By_Order(filteredOrders[i].id) === undefined) {
	  			j--;
	  		}
		          
	      	if (j === 3) {
	    		j = 0;
	      	} else {
	    	  	j++;
	      	}
	      	contents.append(sorderline);
		}
	  	    
	}
    /*Cashier view payment button click action*/
    set_Cashier_Payment(order, orderTableId) {
    	var self = this;
    	var orders = this.env.pos.get_order_list();
    	var tables = self.env.pos.tables_by_id[orderTableId];
  	  	for (var j = 0; j < orders.length; j++) {
  	  		var getOrder = orders[j];
  	  		if (getOrder.uid === order) {
  	  			var currentOrder = getOrder;
  	  			//Removed cancelled orderline from order
  	  			var orderlines = currentOrder.get_orderlines();
  	  			var removeLines = [];
	  	  		for (var i = 0; i < orderlines.length; i++) {
	    			if (orderlines[i].get_Kitchen_State() === 'cancel') {
	    				removeLines.push(orderlines[i])
	    			}
	    		}
		  	  	for (var i = 0; i < removeLines.length; i++) {
	    			removeLines[i].order.remove_orderline(removeLines[i]);
	    		}
  	  			if (order) {
  	  				//this.env.pos.set_table(tables);
					this.env.pos.table = tables;
  	  				this.env.pos.set_order(currentOrder);
  	  				this.showScreen('PaymentScreen');
  	  			}
  	  		}
  	  	}
    }
    /******start code - Payment orders and tab design code******/
        payment_Order () {
    	var self = this;
    	$('.comp_search').addClass('wet_display_none');
    	$('.comp_search_box').val('');
    	var inprogressContents = document.querySelector('.all_pos_orders .restaurant_orders');
    	if (inprogressContents != null && inprogressContents != undefined) {
			inprogressContents.innerHTML = "";
		}
    	var deliveredContents = document.querySelector('.all_pos_orders .cashier_orders');
		if (deliveredContents != null && deliveredContents != undefined) {
			deliveredContents.innerHTML = "";
		}
    	$("#inprogress_orders_span").css('background-color', '#ffffff');
    	$("#completed_orders_span").css('background-color', '#ffffff');
    	$("#inprogress_orders_span").removeClass('com_active');
    	$("#completed_orders_span").removeClass('com_active');
    	$("#payment_orders_span").css('background-color', '#4a90cc');
    	
    	self.env.pos.db.set_Active_Tab('payment');
    	$('.restaurant_orders').css({'width': '0%'});
    	$('.cashier_orders').css({'width': '100%'});
    	/******start code - to show delivered orders in cashier view********/
    	var kitchenOrders = self.env.pos.get_order_list();
    	/*Payment order - get kitchen orders count in paymnet orders.*/
    	for (var k = 0; k < kitchenOrders.length; k++) {
    		var kitchenOrder = kitchenOrders[k];
    		var kitchenOrderlines = kitchenOrder.get_orderlines();
    		var isDeliveredState = true;
    		for (var m = 0; m < kitchenOrderlines.length; m++) {
    			var lnState = kitchenOrderlines[m];
    			var olineState = lnState.get_Kitchen_State();
    			if (olineState != 'delivered' && olineState != 'cancel') {
    				isDeliveredState = false;
		        }
    		}
    		if (isDeliveredState) {
    			var porderlineHtml  = QWeb.render('CashierOrders',{widget:self, order:kitchenOrder, orderlines:kitchenOrderlines, slevel:zoomLevel});
        		var porderline = document.createElement('div');
        		if (porderlineHtml != null && porderlineHtml != undefined) {
					porderline.innerHTML = porderlineHtml;
	        		porderline = porderline.childNodes[1];
	        		var posPaymentIcon  = porderline.querySelectorAll('.pos_payment_btn');
	        		  if (posPaymentIcon) {
	        			for (var i = 0; i < posPaymentIcon.length; i++) {
	        				posPaymentIcon[i].addEventListener('click', (function (e) {
		    	        		e.preventDefault();
		    	        		var order = $(e.currentTarget).closest('.pos_payment_btn').attr('data-uid');
		    	        		var orderTableId = $(e.currentTarget).closest("li.first_li_head").next().find('.pos-table-no').attr('data-tbl-id');
		    	        		this.set_Cashier_Payment(order, orderTableId);
		    	            }.bind(this)));
	        			}
	        		  }
					if (deliveredContents != null && deliveredContents != undefined) {
						deliveredContents.prepend(porderline);
					}
				}
    		}
    	}
    	/******end code - to show delivered orders in cashier view********/
    	//start
    	var firstContents = document.querySelector('.checkout_orders .first_orders');
		if (firstContents != null && firstContents != undefined) {
			firstContents.innerHTML = "";
		}
  	    var secondContents = document.querySelector('.checkout_orders .second_orders');
		if (secondContents != null && secondContents != undefined) {
			secondContents.innerHTML = "";
		}
  	    var thirdContents = document.querySelector('.checkout_orders .third_orders');
  	    if (thirdContents != null && thirdContents != undefined) {
			thirdContents.innerHTML = "";
		}
  	    var fourthContents = document.querySelector('.checkout_orders .fourth_orders');
		if (fourthContents != null && fourthContents != undefined) {
			fourthContents.innerHTML = "";
		}

    	var openContents = document.querySelector('.all_checkout_orders .open_orders');
		if (openContents != null && openContents != undefined) {
			openContents.innerHTML = "";
		}
  	    var confirmContents = document.querySelector('.all_checkout_orders .confirm_orders');
		if (confirmContents != null && confirmContents != undefined) {
			confirmContents.innerHTML = "";
		}
  	    var prepareContents = document.querySelector('.all_checkout_orders .prepare_orders');
		if (prepareContents != null && prepareContents != undefined) {
			prepareContents.innerHTML = "";
		}
  	    var readyContents = document.querySelector('.all_checkout_orders .ready_orders');
		if (readyContents != null && readyContents != undefined) {
			readyContents.innerHTML = "";
		}

    	var j = 0;
    	var orders = self.env.pos.db.get_Sorder_Sorted(1000);
    	var filteredOrders = orders;
    	var today = new moment().format('YYYY-MM-DD');
    	filteredOrders = $.grep(orders, function (v) {
    		return v.state === "delivered" && v.write_date >= today && v.website_id;
        });
    	for (var i = 0, len = Math.min(filteredOrders.length,1000); i < len; i++) {
            if (j === 0) {
          	  var contents = document.querySelector('.checkout_orders .first_orders');
            }
            if (j === 1) {
          	  var contents = document.querySelector('.checkout_orders .second_orders');
            }
            if (j === 2) {
          	  var contents = document.querySelector('.checkout_orders .third_orders');
            }
            if (j === 3) {
          	  var contents = document.querySelector('.checkout_orders .fourth_orders');
            }
            	var orderlines = [];
            	if (self.env.pos.db.get_Orderline_By_Order(filteredOrders[i].id) != undefined) {
            		orderlines = self.env.pos.db.get_Orderline_By_Order(filteredOrders[i].id);
            	}
                var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: self, sorder:filteredOrders[i], sorderlines:orderlines, slevel:zoomLevel});
                var sorderline = document.createElement('div');
				if (sorderline != null && sorderline != undefined) {
					 sorderline.innerHTML = sorderlineHtml;
	                sorderline = sorderline.childNodes[1];
	                var stateIcon = sorderline.querySelector('.order_btn');
	                 /*Payment orders - state Icon button function*/
	                if (stateIcon) {
	                	stateIcon.addEventListener('click', (function (e) {
	                    	var orderId = e.target.dataset.item;
	                    	var orderState = ($("#"+orderId).text()).trim();
	                    	self.update_Order_State(orderId, orderState);
	                    }.bind(this)));
	                }
	                var deleteIcon = sorderline.querySelector('.del_btn');
	                 /*Payment orders - delete Icon button function*/
	                if (deleteIcon) {
	                	deleteIcon.addEventListener('click', (function (e) {
	                    	var orderId = e.currentTarget.dataset.item;
	                    	self.delete_Order(orderId);
	                    }.bind(this)));
	                }
				}
              
            if (j === 3) {
          	  j = 0;
            } else {
              j++;
            }
            
            contents.prepend(sorderline);
        }
    	//end
    
    }
    /******start code - Complete orders and tab design code******/
    complete_Order () {
    	$('.comp_search').removeClass('wet_display_none');
    	var self = this;
    	var searchVal = $('.comp_search_box').val();
		var inprogressContents = document.querySelector('.all_pos_orders .restaurant_orders');
		if (inprogressContents != null && inprogressContents != undefined) {
			inprogressContents.innerHTML = "";
		}
    	var deliveredContents = document.querySelector('.all_pos_orders .cashier_orders');
		if (deliveredContents != null && deliveredContents != undefined) {
			deliveredContents.innerHTML = "";
		}
    	$("#inprogress_orders_span").css('background-color', '#ffffff');
    	$("#payment_orders_span").css('background-color', '#ffffff');
    	$("#inprogress_orders_span").removeClass('com_active');
    	$("#payment_orders_span").removeClass('com_active');
    	$("#completed_orders_span").css('background-color', '#4a90cc');
    	
    	self.env.pos.db.set_Active_Tab('complete');
    	$('.restaurant_orders').css({'width': '0%'});
    	$('.cashier_orders').css({'width': '100%'});
    	/******start code - to show delivered orders in cashier view********/
    	var datas = [];
    	
    	rpc.query({
            model: 'pos.order',
            method: 'get_complete_order',
            args: [searchVal],
        }).then(function (result) {
        	datas = result;
        	for (var j=0; j < datas.length; j++) {
            	var porderlineHtml  = QWeb.render('CashierCompOrders',{widget:self, data:datas[j]});
        		var porderline = document.createElement('div');
        		if (porderlineHtml != null && porderlineHtml != undefined) {
					porderline.innerHTML = porderlineHtml;
	        		porderline = porderline.childNodes[1];
					if (deliveredContents != null && deliveredContents != undefined) {
						deliveredContents.prepend(porderline);
					}
				}
        	}
        });
    	
    	var firstContents = document.querySelector('.checkout_orders .first_orders');
		if (firstContents != null && firstContents != undefined) {
			firstContents.innerHTML = "";
		}
  	    var secondContents = document.querySelector('.checkout_orders .second_orders');
		if (secondContents != null && secondContents != undefined) {
			secondContents.innerHTML = "";
		}
  	    var thirdContents = document.querySelector('.checkout_orders .third_orders');
		if (thirdContents != null && thirdContents != undefined) {
			thirdContents.innerHTML = "";
		}
  	    var fourthContents = document.querySelector('.checkout_orders .fourth_orders');
		if (fourthContents != null && fourthContents != undefined) {
			fourthContents.innerHTML = "";
		}

    	var openContents = document.querySelector('.all_checkout_orders .open_orders');
		if (openContents != null && openContents != undefined) {
			openContents.innerHTML = "";
		}
  	    var confirmContents = document.querySelector('.all_checkout_orders .confirm_orders');
		if (confirmContents != null && confirmContents != undefined) {
			confirmContents.innerHTML = "";
		}
  	    var prepareContents = document.querySelector('.all_checkout_orders .prepare_orders');
		if (prepareContents != null && prepareContents != undefined) {
			prepareContents.innerHTML = "";
		}
  	    var readyContents = document.querySelector('.all_checkout_orders .ready_orders');
		if (readyContents != null && readyContents != undefined) {
			readyContents.innerHTML = "";
		}

    	var j = 0;
    	var orders = self.env.pos.db.get_Sorder_Sorted(1000);
    	var filteredOrders = orders;
        var today = new moment().format('YYYY-MM-DD'); 
        
    	filteredOrders = $.grep(orders, function (v) {
    		if (searchVal != '' && searchVal != undefined) {
    			return v.state === "payment" && v.write_date >= today && v.website_id && (v.name).toUpperCase().includes(searchVal.toUpperCase()) ;
    		} else {
    			return v.state === "payment" && v.write_date >= today && v.website_id;
    		}
        });
    	for (var i = 0, len = Math.min(filteredOrders.length,1000); i < len; i++) {
            var order    = filteredOrders[i];
            var sorderline = self.sorder_cache.get_node(order.id);
            if (j === 0) {
          	  var contents = document.querySelector('.checkout_orders .first_orders');
            }
            if (j === 1) {
          	  var contents = document.querySelector('.checkout_orders .second_orders');
            }
            if (j === 2) {
          	  var contents = document.querySelector('.checkout_orders .third_orders');
            }
            if (j === 3) { 
          	  var contents = document.querySelector('.checkout_orders .fourth_orders');
            }
            if (!sorderline) {
            	var orderlines = [];
            	if (self.env.pos.db.get_Orderline_By_Order(filteredOrders[i].id) != undefined) {
            		orderlines = self.env.pos.db.get_Orderline_By_Order(filteredOrders[i].id);
            	}
                var sorderlineHtml = QWeb.render('ShopCartOrders',{widget: self, sorder:filteredOrders[i], sorderlines:orderlines, slevel:zoomLevel});
                var sorderline = document.createElement('div');
				if (sorderline != null && sorderline != undefined) {
					sorderline.innerHTML = sorderlineHtml;
	                sorderline = sorderline.childNodes[1];
	                self.sorder_cache.cache_node(order.id, sorderline);
	                var stateIcon = sorderline.querySelector('.order_btn');
	                /*Cashier orders - state Icon button function*/
	                if (stateIcon) {
	                	stateIcon.addEventListener('click', (function (e) {
	                    	var orderId = e.target.dataset.item;
	                    	var orderState = ($("#"+orderId).text()).trim();
	                    	self.update_Order_State(orderId, orderState);
	                    }.bind(this)));
	                }
	                var deleteIcon = sorderline.querySelector('.del_btn');
	                /*Cashier orders - delete Icon button function*/
	                if (deleteIcon) {
	                	deleteIcon.addEventListener('click', (function (e) {
	                    	var orderId = e.currentTarget.dataset.item;
	                    	self.delete_Order(orderId);
	                    }.bind(this)));
	                }
				}
               
            }
            if (j === 3) {
          	  j = 0;
            } else {
              j++;
            }
            contents.prepend(sorderline);
        }
    } 
}
	SOOrderScreen.template = 'SOOrderScreen';
	Registries.Component.add(SOOrderScreen);
	return SOOrderScreen;
});