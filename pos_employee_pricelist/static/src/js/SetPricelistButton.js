odoo.define('pos_employee_pricelist.SetPricelistButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const SetPricelistButton = require('point_of_sale.SetPricelistButton');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

     const EmpSetPricelistButton = (SetPricelistButton) =>
        class extends SetPricelistButton {
            async onClick() {
                // Create the list to be passed to the SelectionPopup.
                // Pricelist object is passed as item in the list because it
                // is the object that will be returned when the popup is confirmed.
                var selectionList = this.env.pos.pricelists.map(pricelist => ({
                    id: pricelist.id,
                    label: pricelist.name,
                    isSelected: pricelist.id === this.currentOrder.pricelist.id,
                    item: pricelist,
                }));
                if(this.env.pos.empricelist_ids && this.env.pos.empricelist_ids.length){
                    selectionList = this.env.pos.empricelist_ids.map(pricelist => ({
                        id: pricelist.id,
                        label: pricelist.name,
                        isSelected: pricelist.id === this.currentOrder.pricelist.id,
                        item: pricelist,
                    }));
                }

                const { confirmed, payload: selectedPricelist } = await this.showPopup(
                    'SelectionPopup',
                    {
                        title: this.env._t('Select the pricelist'),
                        list: selectionList,
                    }
                );

                if (confirmed) {
                    this.currentOrder.set_pricelist(selectedPricelist);
                }
            }
        };
    Registries.Component.extend(SetPricelistButton, EmpSetPricelistButton);
    return EmpSetPricelistButton;
    
});
