odoo.define('pos_product_standard_note.OrderlineNoteButton', function(require) {
    'use strict';

    const OrderlineNoteButton = require('pos_restaurant.OrderlineNoteButton');
    const Registries = require('point_of_sale.Registries');

    const FixedOrderlineNoteButton = OrderlineNoteButton =>
        class extends OrderlineNoteButton {

            async onClick() {
	            if (!this.selectedOrderline) return;
				var pos_note_type_id = this.selectedOrderline.product.template.pos_note_type_id ? this.selectedOrderline.product.template.pos_note_type_id[0] : false
	            var self = this;
	            var vals = {}
	            var note_id_list = []
	            var selected_note_ids = [];
				var selected_note_string = ''

				vals = {
		            startingValue: self.selectedOrderline.get_note(),
	                title: self.env._t('Add Note'),
		        }

		        _.each(this.env.pos.note_ids, function (note_id) {
		            if (note_id.id == pos_note_type_id) {
		                _.each(note_id.note_ids, function (note) {
		                    _.each(self.env.pos.note_id, function (note_list) {
								if (note == note_list.id) {
									note_id_list.push({'name': note_list.name, 'id': note_list.id})
								}
		                    });
		                });
		            }
		        });
		        if (note_id_list) {
		            vals['note_ids'] = note_id_list
		        }
				const { confirmed, payload: inputNote } = await this.showPopup('TextAreaPopup', vals);

				for (var i=0; i< $('input[type="checkbox"]').length; i++) {
				    if ($('input[type="checkbox"]')[i].checked) {
				        selected_note_ids.push({'name': $('input[type="checkbox"]')[i].name, 'id': $('input[type="checkbox"]')[i].value});
				        selected_note_string  += [$('input[type="checkbox"]')[i].name, " , "].join('');
				    }
				}
				var new_string_note = ''
				if (inputNote) {
					new_string_note = [inputNote, selected_note_string].join(',');
				}
				else {
					new_string_note = [selected_note_string];
				}

				if (confirmed) {
	                this.selectedOrderline.set_note(new_string_note);
	                this.selectedOrderline.set_order_note(new_string_note);
	            }

	        }
        }

    Registries.Component.extend(OrderlineNoteButton, FixedOrderlineNoteButton);

    return FixedOrderlineNoteButton;
});