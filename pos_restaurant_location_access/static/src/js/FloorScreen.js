odoo.define('pos_restaurant_location_access.FloorScreen', function(require) {
    'use strict';
    const FloorScreen = require('pos_restaurant.FloorScreen');
    const { useState, useRef } = owl.hooks;
    const { useListener } = require('web.custom_hooks');
    const { posbus } = require('point_of_sale.utils');
    const Registries = require('point_of_sale.Registries');

    const ThemeFloorScreen = (FloorScreen) =>
        class extends FloorScreen {
            constructor() {
                super(...arguments);
                this.env.pos.emfloors = this.env.pos.emfloors.length ? this.env.pos.emfloors : this.env.pos.floors;
                this.state = useState(_.extend(this.state, {'EPfloors': this.env.pos.emfloors}));
                if(this.props.floor != undefined){
                    var is_exist = this.env.pos.emfloors.filter((x)=> x.id == this.props.floor.id);
                    if(!is_exist.length){
                        this.SetUpdateFloors();
                    }
                }
            }
            mounted() {
                super.mounted
                posbus.on('updated_emp_floors', this, this.SetUpdateFloors);
            }
            SetUpdateFloors(){
                var tmpc = this.env.pos.get_cashier();
                var floor = null;
                var cashier = {}
                if(tmpc != undefined && tmpc.id != null){
                    cashier = this.env.pos.employee_by_id[tmpc.id];
                }
                if(cashier['floors_ids'] != undefined && cashier['floors_ids'].length){
                    var floor_ids = cashier['floors_ids'];
                    var floors = this.env.pos.floors.filter((x)=> floor_ids.includes(x.id));
                    floor = floors[0];
                    this.state.EPfloors = floors;
                    this.state.selectedFloorId = floor.id;
                    this.state.selectedTableId = null;
                    this.state.isEditMode = false;
                    this.state.floorBackground = floor.background_color;
                    this.env.pos.emfloors = floors;
                }else{
                    this.state.EPfloors = this.env.pos.floors;
                    floor = this.env.pos.floors[0];
                    this.state.selectedFloorId = floor.id;
                    this.state.selectedTableId = null;
                    this.state.isEditMode = false;
                    this.state.floorBackground = floor.background_color;
                    this.env.pos.emfloors = this.env.pos.floors;
                }
            }
        };
    Registries.Component.extend(FloorScreen, ThemeFloorScreen);
    return ThemeFloorScreen;
});
