odoo.define('sh_pos_product_multi_category', function (require) {
    'use strict';

    var models = require('point_of_sale.models')
    var PosDb = require("point_of_sale.DB")
    var utils = require('web.utils');

    models.load_fields('product.product', ['sh_pos_categ_ids'])


    PosDb.include({
        add_products: function (products) {
            var stored_categories = this.product_by_category_id;
            var self = this;
            if (!products instanceof Array) {
                products = [products];
            }
            for (var i = 0, len = products.length; i < len; i++) {
                var product = products[i];
                if (product.id in self.product_by_id) continue;
                if (product.available_in_pos) {
                    var search_string = utils.unaccent(self._product_search_string(product));
                    product.product_tmpl_id = product.product_tmpl_id[0];
                    var sh_pos_categ_ids = product.sh_pos_categ_ids
                    for (var k = 0; k < sh_pos_categ_ids.length; k++) {
                        var pos_categ_id = sh_pos_categ_ids[k]
                        if (!stored_categories[pos_categ_id]) {
                            stored_categories[pos_categ_id] = [];
                        }
                        stored_categories[pos_categ_id].push(product.id);
                        if (self.category_search_string[pos_categ_id] === undefined) {
                            self.category_search_string[pos_categ_id] = '';
                        }
                        self.category_search_string[pos_categ_id] += search_string;
                    }

                    var base_categ_id = product.pos_categ_id ? product.pos_categ_id[0] : self.root_category_id;
                    if (!stored_categories[base_categ_id]) {
                        stored_categories[base_categ_id] = [];
                    }
                    stored_categories[base_categ_id].push(product.id);

                    if (this.category_search_string[base_categ_id] === undefined) {
                        this.category_search_string[base_categ_id] = '';
                    }
                    this.category_search_string[base_categ_id] += search_string;

                    var ancestors = this.get_category_ancestors_ids(base_categ_id) || [];

                    for (var j = 0, jlen = ancestors.length; j < jlen; j++) {
                        var ancestor = ancestors[j];
                        if (!stored_categories[ancestor]) {
                            stored_categories[ancestor] = [];
                        }
                        stored_categories[ancestor].push(product.id);

                        if (this.category_search_string[ancestor] === undefined) {
                            this.category_search_string[ancestor] = '';
                        }
                        this.category_search_string[ancestor] += search_string;
                    }
                }
                self.product_by_id[product.id] = product;
                if (product.barcode) {
                    self.product_by_barcode[product.barcode] = product;
                }
            }
            this._super(products)
        }
    })
});
