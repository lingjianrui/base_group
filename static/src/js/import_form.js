odoo.define('base_group.ReportWidget', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var Widget = require('web.Widget');

    var QWeb = core.qweb;

    var _t = core._t;

    var ReportWidget = AbstractAction.extend({
        start: function() {
            console.log("hello");
            var products = new ProductsWidget(
                this, ["cpu", "mouse", "keyboard", "graphic card", "screen"], "#00FF00");
                products.appendTo(this.$el); 
        }
    });
    
    var ProductsWidget = Widget.extend({
        template: "ProductsWidget",
        
        init: function(parent, products, color) {
            this._super(parent);
            this.products = products;
            this.color = color;
        }
    });

    core.action_registry.add("abc", ReportWidget);
    return ReportWidget;

});
