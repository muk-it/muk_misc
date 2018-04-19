/**********************************************************************************
* 
*    Copyright (C) 2018 MuK IT GmbH
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Affero General Public License as
*    published by the Free Software Foundation, either version 3 of the
*    License, or (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Affero General Public License for more details.
*
*    You should have received a copy of the GNU Affero General Public License
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
**********************************************************************************/

odoo.define('account_bank_statement.import', function (require) {
"use strict";

var core = require('web.core');

var BaseImport = require('base_import.import');

var _t = core._t;
var QWeb = core.qweb;

var AccountBankStatementImport = BaseImport.DataImport.extend({
    init: function (parent, action) {
        this._super.apply(this, arguments);
        this.filename = action.params.filename;
        action.display_name = _t('Import Bank Statement');
    },
    start: function () {
        var self = this;
        return this._super().then(function (res) {
        	self.loaded_file();
        });
    },
    create_model: function() {
    	return $.Deferred().resolve(this.parent_context.wizard_id);
    },
    onfile_loaded: function () {
    	this.$('.oe_import_file_show').val(this.filename);
        this.$('label[for=my-file-selector], input#my-file-selector').hide();
        this.$('label[for=my-file-selector]').parent().append(
        		$('<span/>' , {class: "btn btn-default disabled", text: "File loaded!"}));
        this.$('.oe_import_file_reload').hide();
        this.settings_changed();
    },
    onpreviewing: function () {
        var self = this;
        this.$el.addClass('oe_import_with_file');
        this.$el.removeClass('oe_import_preview_error oe_import_error');
        this.$el.toggleClass('oe_import_noheaders', !this.$('input.oe_import_has_header').prop('checked'));
        this._rpc({
                model: 'account.bank.statement.import.wizard',
                method: 'parse_preview',
                args: [this.id, this.import_options()],
            }).done(function (result) {
                var signal = result.error ? 'preview_failed' : 'preview_succeeded';
                self[signal](result);
            });
    },
	call_import: function (kwargs) {
		var tracking_disable = 'tracking_disable' in kwargs ?
				kwargs.tracking_disable : !this.$('#oe_import_tracking').prop('checked');
	    var defer_parent_store = 'defer_parent_store' in kwargs ?
	    		kwargs.defer_parent_store : !!this.$('#oe_import_deferparentstore').prop('checked');
	    delete kwargs.tracking_disable;
	    delete kwargs.defer_parent_store;
		var fields = this.$('.oe_import_fields input.oe_import_match_field').map(function (index, el) {
	        return $(el).select2('val') || false;
	    }).get();
	    kwargs.context = _.extend({}, this.parent_context, {
        	tracking_disable: tracking_disable,
        	defer_parent_store_computation: defer_parent_store
	    });
	    return this._rpc({
            model: 'account.bank.statement.import.wizard',
            method: 'do',
            args: [this.id, fields, this.import_options()],
            kwargs : kwargs,
        }).fail(function (error, event) {
            if (event) { 
            	event.preventDefault(); 
            }
            return $.when([{
                type: 'error',
                record: false,
                message: error.data.arguments && error.data.arguments[1] || error.message,
            }]);
        });
	},
});

core.action_registry.add('import_bank_statement', AccountBankStatementImport);

});

