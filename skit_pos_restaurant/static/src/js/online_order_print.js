odoo.define('skit_pos_restaurant.online_order_print', function (require) {
    'use strict';
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');

   class OnlineOrderPrint extends AbstractAwaitablePopup {
	  constructor() {
	    	super(...arguments);
			useListener('print-online-receipt', this._print_Online_Receipt);
			useListener('Cancel', this._cancel);
	    }
	    
		init(parent, args) {
	        this._super(parent, args);
	        this.options = {};
	    }
		/* Print online receipt order line*/
		async _print_Online_Receipt() {
			var orderId = this.props.order_id
			var sOrder = this.env.pos.db.sorder_by_id[orderId];
			var sOrderLines = this.env.pos.db.get_Orderline_By_Order(orderId);
			var receipt = this.env.qweb.renderToString('OnlineOrderTicket', { 
				widget: this, order: sOrder, sorderlines: sOrderLines
				});
				if (this.env.pos.proxy.printer) {
                    await this._printIoT(receipt);
                } else {
                    await this._printWeb(receipt);
                }

		}
		/* close online receipt order line popup screen*/
		async _cancel() {
			this.cancel();
		}
		/* Print the pos recepit in proxy printer*/
		async _printIoT(receipt) {
            const printResult = await this.env.pos.proxy.printer.print_receipt(receipt);
            if (!printResult.successful) {
                await this.showPopup('ErrorPopup', {
                    title: printResult.message.title,
                    body: printResult.message.body,
                });
            }
        }
		/* Print the pos recepit in web*/
        async _printWeb(receipt) {
            try {
				var newWindow = window.open();
			    newWindow.document.write(receipt);
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
	}
	OnlineOrderPrint.template = 'OnlineOrderPrintPopupWidget';
    OnlineOrderPrint.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        title: 'Confirm ?',
        body: '',
    };

    Registries.Component.add(OnlineOrderPrint);

    return OnlineOrderPrint;

});