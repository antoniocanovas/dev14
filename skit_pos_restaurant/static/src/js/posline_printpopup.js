odoo.define('skit_pos_reservation.POSLinePrintPopupWidget', function (require) {
    'use strict';
    const abstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
    var core = require('web.core');
	var QWeb = core.qweb;

    // formerly ConfirmPopupWidget
        class POSLinePrintPopupWidget extends abstractAwaitablePopup {
            constructor() {
	            super(...arguments);
	            useListener('button_close', this._button_Close);           
	            useListener('button_print', this._button_Print);             
            }
    		mounted() {       
		        var olineId = this.props.line_id
		        var orderUid = this.props.order_uid
		        var posOrder = this.env.pos.get_order();
		        var posOrderLine = [];
		        var orders = this.env.pos.get_order_list();
				for (var j = 0; j < orders.length; j++) {
					var getOrder = orders[j];
					if (getOrder.uid === orderUid) {
					    posOrder = getOrder;
						var orderlines = getOrder.get_orderlines()
						for (var i = 0; i < orderlines.length; i++) {
							var getOrderline = orderlines[i];
							if (getOrderline.id === parseInt(olineId)) {
								posOrderLine =  getOrderline;
							}
						}
					}
				}
		        $('.pos-receipt-container').html(QWeb.render('PosOrderLineTicket', { widget: this, pos: this.pos, order: posOrder, orderline: posOrderLine}));
    		}
    		/*Kitchen view - particular order only print function */
		    async _button_Print() {
		        var olineId = this.props.line_id
		        var orderUid = this.props.order_uid
		        var posOrder = this.env.pos.get_order();
		        var posOrderLine = [];
		        var orders = this.env.pos.get_order_list();
				for (var j = 0; j < orders.length; j++) {
					var getOrder = orders[j];
					if (getOrder.uid === orderUid) {
					    posOrder = getOrder;
						var orderlines = getOrder.get_orderlines()
						for (var i = 0; i < orderlines.length; i++) {
							var getOrderline = orderlines[i];
							if (getOrderline.id === parseInt(olineId)) {
								posOrderLine =  getOrderline;
								var posOrderLines = QWeb.render('PosOrderLineTicket', {
									 widget: this, 
									 pos: this.pos, 
									 order: posOrder, 
									 orderline: posOrderLine
								});
								if (this.env.pos.proxy.printer) {
				                    await this._printIoT(posOrderLines);
				                } else {
				                    await this._printWeb();
				                }
							}
						}
					}
				}  
		    }
		    /*print the order line in proxy printer*/
			async _printIoT(receipt) {
		        const printResult = await this.env.pos.proxy.printer.print_receipt(receipt);
		        if (!printResult.successful) {
		            await this.showPopup('ErrorPopup', {
		                title: printResult.message.title,
		                body: printResult.message.body,
		            });
		        }
		     }
		   /*print the order line in printer*/
		    async _printWeb() {
	            try {
					var newWindow = window.open();
				    newWindow.document.write(document.getElementById("output").innerHTML);
				    newWindow.print();
				    newWindow.close();
	             } catch (err) {
	                await this.showPopup('ErrorPopup', {
	                    title: this.env._t('Printing is not supported on some browsers'),
	                    body: this.env._t(
	                        'Printing is not supported on some browsers due to no default printing protocol ' +
	                            'is available. It is possible to print your tickets by making use of an IoT Box.'
	                    ),
	                });
	            }
	        }
			/*Close button in popup*/
		   async _button_Close() {	 
		    	this.cancel();
		    }
    	}
	    POSLinePrintPopupWidget.template = 'POSLinePrintPopupWidget';
	    POSLinePrintPopupWidget.defaultProps = {
	        confirmText: 'Ok',
	        cancelText: 'Cancel',
	        title: 'Confirm ?',
	        body: '',
	    };

    Registries.Component.add(POSLinePrintPopupWidget);

    return POSLinePrintPopupWidget;
});
       
        
        
        
