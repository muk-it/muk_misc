/**********************************************************************************
*
*    Copyright (c) 2017-2019 MuK IT GmbH.
*
*    This file is part of MuK Bank Statement Import 
*    (see https://mukit.at).
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Lesser General Public License as published by
*    the Free Software Foundation, either version 3 of the License, or
*    (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Lesser General Public License for more details.
*
*    You should have received a copy of the GNU Lesser General Public License
*    along with this program. If not, see <http://www.gnu.org/licenses/>.
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
        return this._super.apply(this, arguments).then(function (res) {
        	self.loaded_file();
        });
    },
    create_model: function() {
    	return $.Deferred().resolve(this.parent_context.wizard_id);
    },
    onfile_loaded: function () {
    	this.$('.oe_import_file').hide();
    	this._super.apply(this, arguments);
    },
    onpreviewing: function () {
        var self = this;
        this.$buttons.filter('.o_import_import, .o_import_validate, .o_import_file_reload').addClass('d-none');
        this.$el.addClass('oe_import_with_file');
        this.$el.removeClass('oe_import_preview_error oe_import_error');
        this.$el.toggleClass('oe_import_noheaders text-muted', !this.$('input.oe_import_has_header').prop('checked'));
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
        var fields = this.$('.oe_import_fields input.oe_import_match_field').map(function (index, el) {
            return $(el).select2('val') || false;
        }).get();
        var columns = this.$('.oe_import_grid-header .oe_import_grid-cell .o_import_header_name').map(function () {
            return $(this).text().trim().toLowerCase() || false;
        }).get();
        var tracking_disable = 'tracking_disable' in kwargs ? kwargs.tracking_disable : !this.$('#oe_import_tracking').prop('checked')
        var defer_parent_store = 'defer_parent_store' in kwargs ? kwargs.defer_parent_store : !!this.$('#oe_import_deferparentstore').prop('checked')
        delete kwargs.tracking_disable;
        delete kwargs.defer_parent_store;
        kwargs.context = _.extend({}, this.parent_context, {
    		tracking_disable: tracking_disable,
    		defer_parent_store_computation: defer_parent_store
        });
        var self = this;
        return this._rpc({
            model: 'account.bank.statement.import.wizard',
            method: 'do',
            args: [this.id, fields, columns, this.import_options()],
            kwargs : kwargs,
        }).done(function(result) {
        	self.bank_statement_id = result.bank_statement_id;
        }).fail(function (error, event) {
            if (event) {
            	event.preventDefault(); 
            }
            var msg = _t("An unknown issue occurred during import.");
            if (error.data.type === 'xhrerror') {
                var xhr = error.data.objects[0];
                switch (xhr.status) {
	                case 504:
	                    msg = _t("Import timed out. Please retry. If you still encounter this issue, the file may be too big for the system's configuration, try to split it (import less records per file).");
	                    break;
	                default:
	                    msg = _t("An unknown issue occurred during import (possibly lost connection, data limit exceeded or memory limits exceeded). Please retry in case the issue is transient. If the issue still occurs, try to split the file rather than import it at once.");
                }
            } else {
                msg = (error.data.arguments && error.data.arguments[1] || error.data.arguments[0]) || error.message;
            }
            return $.when({'messages': [{
                type: 'error',
                record: false,
                message: msg,
            }]});
        }) ;
    },
    exit: function () {
        this.do_action({
            name: _t("Reconciliation"),
            type: 'ir.actions.client',
            tag: 'bank_statement_reconciliation_view',
            context: {
                'statement_ids': [this.bank_statement_id],
            },
        });
    },
});

core.action_registry.add('import_bank_statement', AccountBankStatementImport);

});

