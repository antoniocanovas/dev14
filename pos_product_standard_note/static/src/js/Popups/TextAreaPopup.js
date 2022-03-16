odoo.define('pos_product_standard_note.ProductsWidget', function(require) {
    'use strict';

    const TextAreaPopup = require('point_of_sale.TextAreaPopup');
    const Registries = require('point_of_sale.Registries');

    const FixedTextAreaPopup = TextAreaPopup =>
        class extends TextAreaPopup {

            _selectedPosType(note_id) {
	            if (document.getElementById(note_id.id).checked == false){
	                document.getElementById(note_id.id).checked = true;
	            }
	            else {
	                document.getElementById(note_id.id).checked = false;
	            }
	        }

	        _onClearNoteClick() {
	            this.state.inputValue = ''
	            $('textarea').val('')
	        }
        }

    Registries.Component.extend(TextAreaPopup, FixedTextAreaPopup);

    return FixedTextAreaPopup;
});
