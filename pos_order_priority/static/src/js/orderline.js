odoo.define('pos_order_priority.orderline', function(require) {
	"use strict";

var models = require('point_of_sale.models');


var _super_orderline = models.Orderline.prototype;
models.Orderline = models.Orderline.extend({
    initialize: function(attr, options) {
        _super_orderline.initialize.call(this,attr,options);
        this.order = options.order;
        if (this.order.priority) {
             this.priority = this.order.priority;
             this.priority_value = this.order.priority_value;
        }else {
            this.priority = this.priority || "";
            this.priority_value = this.priority_value || "";
        }
    },
    set_priority: function(priority){
        this.priority = priority;
        this.trigger('change',this);
    },
    get_priority: function(priority){
        return this.priority;
    },
    set_priority_value: function(priority_value){
        this.priority_value = priority_value;
        this.trigger('change',this);
    },
    get_priority_value: function(priority_value){
        return this.priority_value;
    },
    can_be_merged_with: function(orderline) {
        if (orderline.get_priority() !== this.get_priority()) {
            return false;
        } else {
            return _super_orderline.can_be_merged_with.apply(this,arguments);
        }
    },
    clone: function(){
        var orderline = _super_orderline.clone.call(this);
        orderline.priority = this.priority;
        orderline.priority_value = this.priority_value;
        return orderline;
    },
    export_as_JSON: function(){
        var json = _super_orderline.export_as_JSON.call(this);
        json.priority = this.priority;
        json.priority_value = this.priority_value;
        return json;
    },
    init_from_JSON: function(json){
        _super_orderline.init_from_JSON.apply(this,arguments);
        this.priority = json.priority;
        this.priority_value = json.priority_value;
    },
});

var _super_order = models.Order.prototype;
models.Order = models.Order.extend({
    initialize: function(attr, options) {
        _super_order.initialize.call(this,attr,options);
        this.priority = this.priority || "";
        this.priority_value = this.priority_value || "";
    },
    set_priority: function(priority){
        this.priority = priority;
        this.trigger('change',this);
    },
    get_priority: function(priority){
        return this.priority;
    },
    set_priority_value: function(priority_value){
        this.priority_value = priority_value;
        this.trigger('change',this);
    },
    get_priority_value: function(priority_value){
        return this.priority_value;
    },
    export_as_JSON: function(){
        var json = _super_order.export_as_JSON.call(this);
        json.priority = this.priority;
        json.priority_value = this.priority_value;
        return json;
    },
    init_from_JSON: function(json){
        _super_order.init_from_JSON.apply(this,arguments);
        this.priority = json.priority;
        this.priority_value = json.priority_value;
    },
});

});
