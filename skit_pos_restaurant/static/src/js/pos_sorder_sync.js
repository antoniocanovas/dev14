odoo.define('pos_sorder_sync.pos', function (require) {
    const models = require('point_of_sale.models');	
    const registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc');
	var SOOrderScreen = require('skit_pos_restaurant.SOOrderScreen');
	
    var SOOrderScreenWidget;
	const posSOOrderScreen = (SOOrderScreen) =>
        class extends SOOrderScreen {
        	constructor() {
            super(...arguments);
            SOOrderScreenWidget = this;
            }
        };
   		registries.Component.extend(SOOrderScreen, posSOOrderScreen); 

    var PosModelSuper = models.PosModel;
    models.PosModel = models.PosModel.extend({
        initialize: function () {
            PosModelSuper.prototype.initialize.apply(this, arguments);
            var self = this;
            this.ready.then(function () {
                self.bus.add_channel_callback("pos_sale_sync", self.on_sorder_updates, self);
            });
        },
        /*update the sale order and sync the orders*/
        on_sorder_updates: function (data) {
            var self = this;
            console.log('datas:'+JSON.stringify(data))
            if (data.message === 'update_sorder_fields' && data.order_ids && data.order_ids.length) {
            	
            	if (data.action && data.action === 'unlink') {
                    this.remove_unlinked_sorders(data.order_ids);
                    this.update_templates_with_sorder(data.order_ids);
                } else {
                    this.load_new_sorders_force_update(data.order_ids).then(function () {
                       self.update_templates_with_sorder(data.order_ids);
                    });
                }
            }
        },
		/*updates, renders order details, renders order*/
        update_templates_with_sorder: function (order_ids) {
			var self = this;
            if (!order_ids) {
                return;
            }
            // updates order cache
			if (self.env.pos.config.supplier_view || (self.env.pos.config.cashier_view && this.env.pos.db.get_Track_Screen() ==="track_status_screen") || (self.env.pos.config.waiter_view && this.env.pos.db.get_Track_Screen() ==="track_status_screen")) {
				if (SOOrderScreenWidget != undefined && SOOrderScreenWidget != null) {
					SOOrderScreenWidget.update_Sorder_Screen()
				}
			}
            
        },
		updateRemovedOrder: function () {
			var self = this;
			if (self.env.pos.config.supplier_view || (self.env.pos.config.cashier_view && this.env.pos.db.get_Track_Screen() ==="track_status_screen") || (self.env.pos.config.waiter_view && this.env.pos.db.get_Track_Screen() ==="track_status_screen")) {
				if (SOOrderScreenWidget != undefined && SOOrderScreenWidget != null) {
					SOOrderScreenWidget.update_Sorder_Screen()
				}
			}
		},
		/*Load new sale order lines and update the kitchen view*/
        load_new_sorders_force_update: function (ids) {
            // quite similar to load_new_order but loads only required orders and do it forcibly (see the comment below)
            var def = new $.Deferred();
            if (!ids) {
                return def.reject();
            }
            var self = this;
            var modelName = 'sale.order';
            var fields = _.find(this.models,function (model) {
                return model.model === modelName;
            }).fields;
            
            var linefields = _.find(this.models,function (model) {
                return model.model === 'sale.order.line';
            }).fields;
            
            ids = Array.isArray(ids)
            ? ids
            : [ids];
            rpc.query({
                model: modelName,
                method: 'read',
                args: [ids, fields],
            }, {
                shadow: true,
            }).then(function (orders) {
                // check if the partners we got were real updates
                // we add this trick with get_partner_write_date to be able to process several updates within the second
                // it is restricted by built-in behavior in add_partners function
            	var domain = [['order_id', 'in', ids]];
            	
            	rpc.query({
                    model: 'sale.order.line',
                    method: 'search_read',
                    args: [domain, linefields],
                })
                .then(function (orderlines) {
                	self.db.add_Orderline(orderlines);
                	
                	self.db.sorder_write_date = 0;
                    // returns default value "1970-01-01 00:00:00"
                    self.db.get_Sorder_Write_Date();
                    if (self.db.add_Sorders(orders)) {
                        def.resolve();
                    } else {
                        def.reject();
                    }
                });
                
            }, function (err,event) {
                if (err) {
                    console.log(err.stack);
                }
                event.preventDefault();
                def.reject();
            });
            return def;
        },
		/*remove the unlink sale order lines*/
        remove_unlinked_sorders: function (ids) {
            var self = this;
            var order = false;
            var sorder_sorted = this.db.sorder_sorted;
            _.each(ids, function (id) {
                order = self.db.get_Sorder_By_Id(id);
                sorder_sorted.splice(_.indexOf(sorder_sorted, id), 1);
                delete self.db.sorder_by_id[id];
            });
        },
    });

});
