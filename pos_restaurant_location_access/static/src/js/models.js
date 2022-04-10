odoo.define('pos_restaurant_location_access.models', function (require) {
    "use strict";

var models = require('point_of_sale.models');
models.load_fields('hr.employee', ['floors_ids']);
const { posbus } = require('point_of_sale.utils');

var posmodel_super = models.PosModel.prototype;
models.PosModel = models.PosModel.extend({
    initialize: function(attributes) {
        posmodel_super.initialize.apply(this, arguments);
        this.emfloors = [];
    },
    set_cashier: function(employee){
        posmodel_super.set_cashier.apply(this, arguments);
        posbus.trigger('updated_emp_floors');
    }
});
});