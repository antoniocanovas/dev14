odoo.define('pos_order_priority.SetPriorityButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class SetPriorityButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        get currentOrder() {
            return this.env.pos.get_order();
        }
        get currentLine() {
            return this.env.pos.get_order().get_selected_orderline();
        }

        get currentPriority() {
            const pol = this.env.pos.get_order().get_selected_orderline();
            return pol && pol.priority
                ? pol.priority
                : this.env._t('Priority');
        }
        async onClick() {
            if (!this.currentLine) return;
            var self = this;
            var priority_list = []
            _.each(this.env.pos.config.priority_ids, function (priority) {
                _.each(self.env.pos.line_priority, function (priority_id) {
                    if (priority_id && priority_id.id == priority) {
		                priority_list.push({'id': priority_id.id,
			                               'label': priority_id.name,
			                               'value': priority_id.value,
			                               'color_code': priority_id.color_code,
			                               'item': priority_id.id});
			        }
		        });
            });
            console.log(priority_list);
            const selectionList = priority_list.map(prioritylist => ({
                id: prioritylist.id,
                label: prioritylist.label,
                value: prioritylist.value,
                item: prioritylist,
            }));
            const { confirmed, payload: selectedStatelist } = await self.showPopup(
                'SelectionPopup',
                {
                    title: self.env._t('Select Priority'),
                    list: selectionList,
                }
            );

            if (confirmed) {
                this.currentLine.set_priority(selectedStatelist.label);
                this.currentLine.set_priority_value(selectedStatelist.value);
                this.currentOrder.set_priority(selectedStatelist.label);
                this.currentOrder.set_priority_value(selectedStatelist.value);
            }
        }
    }
    SetPriorityButton.template = 'SetPriorityButton';

    ProductScreen.addControlButton({

        component: SetPriorityButton,
        condition: function() {
            return this.env.pos.config.priority_ids;
        },
    });

    Registries.Component.add(SetPriorityButton);

    return SetPriorityButton;
});
