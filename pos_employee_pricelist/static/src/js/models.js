odoo.define('pos_employee_pricelist.models', function (require) {
    "use strict";

var models = require('point_of_sale.models');
models.load_fields('hr.employee', ['pricelist_ids']);
const { posbus } = require('point_of_sale.utils');

var posmodel_super = models.PosModel.prototype;
models.PosModel = models.PosModel.extend({
    initialize: function(attributes) {
        posmodel_super.initialize.apply(this, arguments);
        this.empricelist_ids = [];
        this.on('change:selectedOrder', this.setEmployeePricelist, this);
    },
    set_cashier: function(employee){
        posmodel_super.set_cashier.apply(this, arguments);
        this.setEmployeePricelist();
    },
    setEmployeePricelist(){
        if( this.db.load('pos_session_id') == this.pos_session.id){
            var cashier = {}
            var tmpc = this.get_cashier();
            if(tmpc != undefined && tmpc.id != null && this.employee_by_id != undefined){
                cashier = this.employee_by_id[tmpc.id];
            }
            if(cashier['pricelist_ids'] != undefined && cashier['pricelist_ids'].length && this.pricelists != undefined && this.get_order()){
                var pricelist_ids = cashier['pricelist_ids'];
                var pricelists = this.pricelists.filter((x)=> pricelist_ids.includes(x.id));
                if(pricelists.length){
                    this.empricelist_ids = pricelists;
                    var pricelist = pricelists[0];
                    var cu = this.get_order().pricelist;
                    if(cu){
                        var cps= this.empricelist_ids.filter((x)=> x.id == cu.id);
                        if(!cps.length){
                           this.get_order().set_pricelist(pricelist); 
                        }
                    }
                }else{
                    this.empricelist_ids = [];
                }
            }else if(cashier['pricelist_ids'] != undefined && cashier['pricelist_ids'].length && this.pricelists){
                var pricelist_ids = cashier['pricelist_ids'];
                var pricelists = this.pricelists.filter((x)=> pricelist_ids.includes(x.id));
                if(pricelists.length){
                    this.empricelist_ids = pricelists;
                }else{
                    this.empricelist_ids = [];
                }
            }else{
                this.empricelist_ids = [];
            }
        }else{
            this.empricelist_ids = [];
        }
    },
});
var Order_super = models.Order.prototype;
models.Order = models.Order.extend({
    set_pricelist(pricelist){
        Order_super.set_pricelist.apply(this, arguments);
    },
    init_from_JSON: function(json) {
        Order_super.init_from_JSON.apply(this, arguments);
        this.pos.setEmployeePricelist();
        this.setEmpPricelist();
    },
    setEmpPricelist(){
        if(this.pos.empricelist_ids && this.pos.empricelist_ids.length){
            var cupri = this.pos.empricelist_ids.filter((x)=> x.id == this.pricelist.id);
            if(!cupri.length){
                this.set_pricelist(this.pos.empricelist_ids[0]);
            }
        }
    }
});

});