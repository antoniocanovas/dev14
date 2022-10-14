odoo.define('skit_pos_restaurant.pos_screen', function (require) {
"use strict";
const Chrome = require('point_of_sale.Chrome');
const Registries = require('point_of_sale.Registries');
const{ Gui }= require('point_of_sale.Gui');
const { useListener } = require('web.custom_hooks');
const models = require('point_of_sale.models');	
var floorScreen = require('pos_restaurant.FloorScreen');
var productScreen = require('point_of_sale.ProductScreen');
var PaymentScreen = require('point_of_sale.PaymentScreen');
var core = require('web.core');
var _t = core._t;
var numberwidget = require('point_of_sale.NumpadWidget');
var orderLineNote = require('pos_restaurant.OrderlineNoteButton');
const { isRpcError } = require('point_of_sale.utils');
var rpc = require('web.rpc');


//To show popup while select product after confirm order.
var superOrder = models.Order.prototype;
models.Order = models.Order.extend({ 	
	initialize: function () {
    	superOrder.initialize.apply(this, arguments);
        this.is_order_confirmed = this.is_order_confirmed;
        this.order_create_date = this.order_create_date || new Date();
		this.order_sequence_no = this.order_sequence_no || 1
    },
       
    export_as_JSON: function () {
		var json = superOrder.export_as_JSON.apply(this,arguments);
	    json.is_order_confirmed = this.get_Is_Order_Confirmed()
		json.order_create_date = this.getOrderCreateDate()
		json.order_sequence_no = this.getOrderSequenceNo()
	    return json;
	},
	init_from_JSON: function (json) {
	   	superOrder.init_from_JSON.apply(this,arguments);
	    this.set_Is_Order_Confirmed(json.is_order_confirmed);
		this.setOrderCreateDate(json.order_create_date)
		this.setOrderSequenceNo(json.order_sequence_no)
	},
	add_product: function (product, options) {
		var self = this;
		var order = self.pos.get_order();
		self.checkOffline(order)
		
		superOrder.add_product.call(this,product,options);
		
		//Enable confirm order button for all cancelled items
		var orderLines = order.get_orderlines(); 
    	if (orderLines[0].get_Kitchen_State() === 'preparing' || orderLines[0].get_Kitchen_State() === 'ready' || orderLines[0].get_Kitchen_State() === 'delivered' || orderLines[0].get_Kitchen_State() === 'cancel') {
    		var order = this.pos.get_order();
    		/*Take away order once you complete the payment - not editable*/
	    	if (order.order_paid) {
	    		Gui.showPopup('ConfirmPopup',{
	                'title': _t('Warning'),
	                'body':  _t('This order is already paid. If you want please create a new order.')
	            });
	    	} else {
	    		self.display_Co_Button(order);
		 		//Display confirm order button when add new line
            	/*Gui.showPopup('ConfirmPopup',{
	                'title': _t('Warning'),
	                'body':  _t('Please "Confirm Order" after editing.'),
	            });*/
	    	}
    	}
	},
	
	async checkOffline(order) {
		try {
			await rpc.query({
                    model: 'pos.order',
                    method: 'check_offline',
                    args: [0],
                })
		}catch (error) {
			var selectedOrderLine = order.get_selected_orderline();
			order.remove_orderline(selectedOrderLine)
            if (isRpcError(error) && error.message.code < 0) {
                Gui.showPopup('ErrorPopup', {
                    title: _t('Network Error'),
                    body: _t('You are offline. You can not add new item.'),
                });
            } else {
                throw error;
            }
        }
		
	},
	
	display_Co_Button: function (order) {
		// Change button style	 
		$('.kitchenorder_confirmed').addClass('kitchen_confirm_button');
		$(".confirm_label").text('Confirm Order');	
		$('.kitchenorder_confirmed').removeClass('kitchenorder_confirmed');
		order.set_Is_Order_Confirmed(false);
	},
	display_Confirmed_Button: function (order, orderlines) {
		// Check order and order lines
		if (order && orderlines.length > 0) {
			 //if (order.get_Is_Order_Confirmed()) {
				 order.set_Is_Order_Confirmed(true);
			// }
			 // Change button style	 
			 $('.kitchen_confirm_button').addClass('kitchenorder_confirmed');
			 $(".confirm_label").text('Confirmed');	
			 $('.kitchen_confirm_button').removeClass('kitchen_confirm_button');
			var localTime  = moment.utc(new Date()).toDate();
			var localDateTime = moment(localTime).format('YYYY-MM-DD HH:mm:ss');	
			order.setOrderSequenceNo(order.sequence_number)
			order.setOrderCreateDate(localDateTime)
		 }
	},
	/*Get and set order comfirmed status*/
	get_Is_Order_Confirmed: function () {
    	return this.is_order_confirmed;
    },
    set_Is_Order_Confirmed: function (is_order_confirmed) {
        this.is_order_confirmed = is_order_confirmed;
    },
    //end
	/*Get and set order create date*/
	getOrderCreateDate: function () {
    	return this.order_create_date;
    },
    setOrderCreateDate: function (order_create_date) {
        this.order_create_date = order_create_date;
    },
	/*Get and set order sequence number */
	getOrderSequenceNo: function () {
    	return this.order_sequence_no;
    },
    setOrderSequenceNo: function (order_sequence_no) {
        this.order_sequence_no = order_sequence_no;
    },
	
});
models.load_models({
 model: 'restaurant.table',
 fields: ['name','width','height','position_h','position_v','shape','floor_id','color','seats','is_take_away'],
 loaded: function (self,tables) {
	 self.tables = tables;
	 self.floor_take_away = {};     
     for (var i = 0; i < tables.length; i++) {
        if (self.tables[i].is_take_away && self.tables[i].floor_id[0]) {
           self.floor_take_away[self.tables[i].floor_id[0]] = self.tables[i].id
        }
        }
 },
});

	const posPaymentScreen = PaymentScreen =>
        class extends PaymentScreen {

		/*If you order status are set into the delivery state - enable payment option*/
		async _finalizeValidation() {
            if (this.currentOrder.is_paid_with_cash() && this.env.pos.config.iface_cashdrawer) {
                this.env.pos.proxy.printer.open_cashbox();
                console.log("Payment");
            }
            this.currentOrder.initialize_validation_date();
            this.currentOrder.finalized = true;
            let syncedOrderBackendIds = [];
			var order = this.currentOrder;
			if (order.table) {
	        	order.set_Order_Paid(true);
	        }
	        var olines = order.get_orderlines()
	        if (order.table) {
		        if (order.table.is_take_away && order.order_paid) {
		        console.log("Payment2");
					/* Comment this line for set perparing state for refund order */
		        	order.set_View_Order('pos_display_block');
		        }
	        }
	        if (order.order_paid) {
	        	order.trigger('new_updates_to_send');
	        	order.set_Hide_Order('pos_display_none');
	        	// first paid and change status order removed correctly.
	        	//but change status and make payment order not removed.so setted the all delivery based on status
	        	var allDeliveryOrder = true;
	        	for (var i = 0, len = olines.length; i < len; i++) {
	        		if (olines[i].get_Kitchen_State() != 'delivered' && olines[i].get_Kitchen_State() != 'cancel') {
	        			allDeliveryOrder = false;
	        		}
	        	}
	        	if (allDeliveryOrder) {
	        		order.set_Delivery(false);
	        	}
	        	if (allDeliveryOrder) {
	        		order.set_All_Delivery(true);
	        	}
	        }
        
            try {
                if (this.currentOrder.is_to_invoice()) {
                    syncedOrderBackendIds = await this.env.pos.push_and_invoice_order(
                        this.currentOrder
                    );
                } else {
                    syncedOrderBackendIds = await this.env.pos.push_single_order(this.currentOrder);
                }
            } catch (error) {
                if (error instanceof Error) {
                    throw error;
                } else {
                    await this._handlePushOrderError(error);
                }
            }
            if (syncedOrderBackendIds.length && this.currentOrder.wait_for_push_order()) {
                const result = await this._postPushOrderResolve(
                    this.currentOrder,
                    syncedOrderBackendIds
                );
                if (!result) {
                    await this.showPopup('ErrorPopup', {
                        title: 'Error: no internet connection.',
                        body: error,
                    });
                }
            }
            this.showScreen(this.nextScreen);

            // If we succeeded in syncing the current order, and
            // there are still other orders that are left unsynced,
            // we ask the user if he is willing to wait and sync them.
            if (syncedOrderBackendIds.length && this.env.pos.db.get_orders().length) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Remaining unsynced orders'),
                    body: this.env._t(
                        'There are unsynced orders. Do you want to sync these orders?'
                    ),
                });
                if (confirmed) {
                    // NOTE: Not yet sure if this should be awaited or not.
                    // If awaited, some operations like changing screen
                    // might not work.
                    this.env.pos.push_orders();
                }
            }
        }
	};
	Registries.Component.extend(PaymentScreen, posPaymentScreen);
	
const posNumberWidget = (numberwidget) =>
    class extends numberwidget {
	
	sendInput(key) {
		var order = this.env.pos.get_order();
    	var selectedOrderLine = order.get_selected_orderline();
    	//Check order line there
    	if (selectedOrderLine) {
	    	if (selectedOrderLine.get_Kitchen_State() === 'preparing'|| selectedOrderLine.get_Kitchen_State() === 'ready' || selectedOrderLine.get_Kitchen_State() === 'delivered') {
	    		order.display_Co_Button(order); //Display confirm order button when changes in line
	    		this.showPopup('ConfirmPopup',{
	                'title': _t('Warning'),
	                'body':  _t('Please "Confirm Order" after editing.')
	            });
	    	}
    	}
    	/*Take away order once you complete the payment - not editable*/	
    	var order = this.env.pos.get_order();
    	if (order.order_paid) {
    		this.showPopup('ConfirmPopup',{
                'title': _t('Warning'),
                'body':  _t('This order is already paid. If you want please create a new order.')
            });
    	} else {
    		this.trigger('numpad-click-input', { key });
    	}
    }
};
Registries.Component.extend(numberwidget, posNumberWidget);
	
	const posResChrome = (Chrome) =>
        class extends Chrome {
		/* start up screen based on config settings*/
			get startScreen() {
                if ((this.env.pos.config.iface_floorplan) && ((this.env.pos.config.cashier_view ) || (this.env.pos.config.waiter_view ))) {
                    const table = this.env.pos.table;
                    return { name: 'FloorScreen', props: { floor: table ? table.floor : null } };
                } else if (this.env.pos.config.supplier_view) {
                	return { name: 'SOOrderScreen'};
                } else {
                	return { name: 'ProductScreen' };
                }
            }
            /*set the constant screen */
            _setScreenData(name) {
				var self = this;
				if (self.env.pos.config.supplier_view || (self.env.pos.config.cashier_view && this.env.pos.db.get_Track_Screen() ==="track_status_screen") || (self.env.pos.config.waiter_view && this.env.pos.db.get_Track_Screen() ==="track_status_screen")) {
					if (name === "PaymentScreen") {
					    console.log("Payment4");
						//self.env.pos.db.set_Payment_Screen('PaymentScreen');
					 	return;
					}
					this.showScreen('SOOrderScreen');
				}
                if (name === 'FloorScreen') return;
                super._setScreenData(...arguments);
            }
            /* Repace the this method for redirect the floor screen in kitchen view */
 			_actionAfterIdle() {
				var self = this;
                if (this.tempScreen.isShown) {
                    this.trigger('close-temp-screen');
                }
				if (self.env.pos.config.supplier_view || (self.env.pos.config.cashier_view && this.env.pos.db.get_Track_Screen() ==="track_status_screen") || (self.env.pos.config.waiter_view && this.env.pos.db.get_Track_Screen() ==="track_status_screen")) {
					this.showScreen('SOOrderScreen');
				} else {
					const table = this.env.pos.table;
                	this.showScreen('FloorScreen', { floor: table ? table.floor : null });
				}
                
           }
			_setActivityListeners() {
				if (this.env.pos.config.iface_floorplan) {
					this.checkNetworkConnection = setInterval(this.checkNetWork.bind(this), 5000);
				}
				
				super._setActivityListeners(...arguments);
            }
			clearBlockUI() {
				clearTimeout(this.showBlockTimer);
				$.unblockUI();
			}
		   async checkNetWork() {
				try {
	                // ping the server, if no error, show the screen
	                await this.rpc({
	                    model: 'pos.order',
	                    method: 'check_offline',
	                    args: [[]],
	                });
					if (this.env.pos.db.isNetwork === 'inactive'){
							this.showBlockTimer = setInterval(this.clearBlockUI.bind(this), 10000);
							if ($.blockUI) {
					        	var msg = _t("Synchronize the Orders");
					            $.blockUI({
					                'message': '<h2 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/>' +
					                         '    <br />' + msg +
					                     '</h2>'
					            });
					        }
							this.env.pos.db.isNetwork = "active"
							var orders = this.env.pos.get_order_list();
							for (var i = 0; i <orders.length; i++) {
								orders[i].new_updates_to_send();
							}
					}
				}catch (error) {
	                if (isRpcError(error) && error.message.code < 0) {
						this.env.pos.db.isNetwork = "inactive"
						const table = this.env.pos.table;
                		this.showScreen('FloorScreen', { floor: table ? table.floor : null });
						$.blockUI()
						if ($.blockUI) {
					    	var msg = _t("Synchronize the Orders");
					        $.blockUI({
					            'message': '<h2 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/>' +
					                 '    <br />' + 
					             '</h2>'
					        });
					     }
	                } else {
	                    throw error;
	                }
	            }
     	   }
           /*if you click close button in pos - close the session */
           async _closePos() {
				var self =this;
	            // If pos is not properly loaded, we just go back to /web without
	            // doing anything in the order data.
	            if (!this.env.pos || this.env.pos.db.get_orders().length === 0) {
					var url = '/web#action=point_of_sale.action_client_pos_menu';
					if (self.env.pos.wet_user.pos_config_id != false && self.env.pos.wet_user.pos_config_id != undefined && self.env.pos.user.pos_config_id != '') {
	            		url = "/web/session/logout"
	        		}
	                window.location = url;
	            }

	            if (this.env.pos.db.get_orders().length) {
	                // If there are orders in the db left unsynced, we try to sync.
	                // If sync successful, close without asking.
	                // Otherwise, ask again saying that some orders are not yet synced.
	                try {
	                    await this.env.pos.push_orders();
	                    var url = '/web#action=point_of_sale.action_client_pos_menu';
	                    if (self.env.pos.wet_user.pos_config_id != false && self.env.pos.wet_user.pos_config_id != undefined && self.env.pos.user.pos_config_id != '') {
			        		url = "/web/session/logout"
			    		}
			            window.location = url;
	                	} catch (error) {
	                    console.warn(error);
	                    const reason = this.env.pos.get('failed')
	                        ? this.env._t(
	                              'Some orders could not be submitted to ' +
	                                  'the server due to configuration errors. ' +
	                                  'You can exit the Point of Sale, but do ' +
	                                  'not close the session before the issue ' +
	                                  'has been resolved.'
	                          )
	                        : this.env._t(
	                              'Some orders could not be submitted to ' +
	                                  'the server due to internet connection issues. ' +
	                                  'You can exit the Point of Sale, but do ' +
	                                  'not close the session before the issue ' +
	                                  'has been resolved.'
	                          );
	                    	const { confirmed } = await this.showPopup('ConfirmPopup', {
	                        title: this.env._t('Offline Orders'),
	                        body: reason,
	                    	});
	                    	if (confirmed) {
		                        this.state.uiState = 'CLOSING';
		                        this.loading.skipButtonIsShown = false;
		                        this.setLoadingMessage(this.env._t('Closing ...'));
		                        var url = '/web#action=point_of_sale.action_client_pos_menu';
		                        if (self.env.pos.wet_user.pos_config_id != false && self.env.pos.wet_user.pos_config_id != undefined && self.env.pos.user.pos_config_id != '') {
		            				url = "/web/session/logout"
		        				}
		                		window.location = url;
		                    }
               	 		}
            		}
        		}
        	};
	Registries.Component.extend(Chrome, posResChrome);

	const skitPosFloorScreen = (floorScreen) =>
        class extends floorScreen {
	        constructor() {
	            super(...arguments);
	         	useListener('button_Track_Status', this._button_Track_Status);
	         	useListener('button_Take_Away', this._button_Take_Away);
         	}
         	/*Track status button click action*/
         	async _button_Track_Status() {
         		$('.all_checkout_orders').hide();
         		$('#checkout_all_orders').hide();
         		this.env.pos.db.set_Track_Screen('track_status_screen');
        	    this.showScreen('SOOrderScreen');
         	}
			/*Take away button click action*/
         	async _button_Take_Away() {
         		var self = this;
         		var tableId = this.env.pos.floor_take_away[this.activeFloor.id]
       			if (tableId) {
	       		var tableKey = Object.keys(self.activeFloor.table_ids).filter(function (key) {return self.activeFloor.table_ids[key] === tableId})[0];	     
	       		var tables = self.activeFloor.tables[tableKey]
	       		self.env.pos.set_table(tables);
	       		} else {
	       			this.showPopup('ConfirmPopup',{
                		'title': _t('Warning'),
                		'body':  _t('Please contact the Administrator to setup TakeAway order.')
            		});
	       		}
         	}
        };
        Registries.Component.extend(floorScreen, skitPosFloorScreen);

	const skitPosProductScreen = (productScreen) =>
        class extends productScreen {
        	constructor() {
	            super(...arguments);
	         	useListener('button_Confirm', this._button_Confirm);
	         	useListener('button_Return', this._button_Return);
/*Expand & Collapse Click Function*/
	         	useListener('products_expand_collapse', this._products_expand_collapse);
	         	var self =this;
	         	setInterval(function () {
	        			self.orderConfirmed();
	       				},10000)
         	}
/*POS Cart Page Collapse Button Click Function*/
         	async _products_expand_collapse() {
				$(".control-buttons").toggle();
			}
         	/*set confirm button in product screen*/
        	orderConfirmed() {
        		if (this.env.pos.get_order()) {
            		return this.env.pos.get_order().is_order_confirmed;
        		} else {
		            return false;
		        }
    		}
    		/* once you complete the payment - not editable*/
		    _onClickPay() {
				var order = this.env.pos.get_order();
				if (order.table) {
		        	if (order.order_paid) {
		        		this.showPopup('ConfirmPopup',{
		                    'title': _t('Warning'),
		                    'body':  _t('This order is already paid. If you want please create a new order.')
		                });
		        	} else {
		        		/** Remove cancelled lines */
		        		var orderlines = order.get_orderlines();
		        		var removeLines = []
		        		for (var i = 0; i < orderlines.length; i++) {
		        			if (orderlines[i].get_Kitchen_State() === 'cancel') {
		        				removeLines.push(orderlines[i])
		        			}
		        		}
		        		for (var i = 0; i < removeLines.length; i++) {
		        			removeLines[i].order.remove_orderline(removeLines[i]);
		        		}
		        		var confirmOrder;
		        		for (var i = 0; i < orderlines.length; i++) {
		                	if (orderlines[i].get_Kitchen_State() === '' || orderlines[i].get_Kitchen_State() === undefined) {
		                		confirmOrder = false;
		                	} else {
		                		confirmOrder = true;
		                	}
		                }
		        		if (confirmOrder) {
		        			this.showScreen('PaymentScreen');
                            console.log("Payment5");
		        		} else {
		        		    console.log("Payment6");
		        			this.showPopup('ConfirmPopup',{
				        		'title': _t('Confirm Order'),
				        	});
		        		}
		        	}
		    	} else {
		    	    console.log("Payment7");
		    		this.showScreen('PaymentScreen');

		    	}
			}
			/*Confirm button click action -  confirm the order upload record in kitchen view and set status*/
		    async _button_Confirm() {
				 try {
	                // ping the server, if no error, show the screen
	                await this.rpc({
	                    model: 'pos.order',
	                    method: 'check_offline',
	                    args: [[]],
	                   // kwargs: { context: this.env.session.user_context },
	                });
					 var kitchenOrders = [];
		    	 	 var self = this;
		    		 var order = self.env.pos.get_order();
		    		 var orderlines = order.get_orderlines();
		    		 order.trigger('new_updates_to_send');
		    		 for (var i = 0; i < orderlines.length; i++) {
		    	        	if (orderlines[i].get_Kitchen_State() === '' || orderlines[i].get_Kitchen_State() === undefined) {
		    	        		orderlines[i].set_Kitchen_State('preparing')
		    	        		kitchenOrders.push(orderlines[i])
		    	        	}
		    	     }
		    		 //Display confirmed button after confirm new line
		    		 if (order && orderlines.length > 0) {
		    			 order.display_Confirmed_Button(order, orderlines);
		    		 }
	            } catch (error) {
	                if (isRpcError(error) && error.message.code < 0) {
	                    this.showPopup('ErrorPopup', {
	                        title: this.env._t('Network Error'),
	                        body: this.env._t('You are offline. You can not add new item.'),
	                    });
	                } else {
	                    throw error;
	                }
	            }

		    }
    		/*Confirm button click action - if you complete the order details -refund are available*/
		    _button_Return() {
		        var orders = this.env.pos.return_orders;
		        /** Refund for current order */
		        var order = this.env.pos.get_order();
		        var orderlines = order.get_orderlines();
		        var cancelLines = []
		        var delivered = true;
		        for (var i = 0; i < orderlines.length; i++) {
		        	if (orderlines[i].get_Kitchen_State() === 'cancel') {
		        		cancelLines.push(orderlines[i])
		        	}
		        	if (orderlines[i].get_Kitchen_State() === 'preparing') {
		        		delivered = false;
		        	}
		        }
		        if (order.order_paid && cancelLines.length > 0 && !delivered) {
		        	this.gui.show_popup('alert',{
		                'title': _t('Warning'),
		                'body':  _t('This order items preparing in kitchen. Please wait for refund...')
		            });
		        } else {
			        if (order.order_paid && cancelLines.length > 0 && delivered) {
			        	order.remove_Paid_Orders(order);
			        	OrderSelectorWidget.pos.add_new_order(); // create a new order
			        	for (var i = 0; i < cancelLines.length; i++) {
			        		var jsonval = cancelLines[i].export_as_JSON();
			        		var product   = this.pos.db.get_product_by_id(jsonval.product_id);
			                if (!product) {
			                    return;
			                }
			        		this.pos.get_order().add_product(product, {
			                    price: jsonval.price_unit,
			                    quantity: -(jsonval.qty),
			                    discount: jsonval.discount,
			                    merge: false,
			                    kitchen_state: 'delivered',
			                    extras: {return_ref: order.uid,
			                            label:jsonval.id},
			                    });
			        	}
			        } else {
			        	this.showScreen('returnOrderList',{orders:orders});
			        }
		        }
		    }
        };
        Registries.Component.extend(productScreen, skitPosProductScreen);

	/** Add confirm order popup while click note button*/
	/*const posOrderLineNote = orderLineNote =>
        class extends orderLineNote {
			constructor() {
	            super(...arguments);
			}
			async onClick() {
	            if (!this.selectedOrderline) return;
	
	            const { confirmed, payload: inputNote } = await this.showPopup('TextAreaPopup', {
	                startingValue: this.selectedOrderline.get_note(),
	                title: this.env._t('Add Note'),
	            });
	
	            if (confirmed) {
					var order = this.env.pos.get_order();
					order.display_Co_Button(order);
	                this.selectedOrderline.set_note(inputNote);
	            }
	        }
	};  
	Registries.Component.extend(orderLineNote, posOrderLineNote); */
});