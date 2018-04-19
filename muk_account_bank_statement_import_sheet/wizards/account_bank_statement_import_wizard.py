###################################################################################
#
#    Copyright (C) 2018 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

import os
import datetime
import logging
import psycopg2

from odoo import _
from odoo import api, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)

class AccountBankStatementImportWizard(models.TransientModel):
    
    _name = "account.bank.statement.import.wizard"
    _inherit = "base_import.import"

    @api.model
    def get_fields(self, model, depth=2):
        return [{  
            'id':'date',
            'name':'date',
            'string':'Date',
            'required':True,
            'fields':[],
            'type':'date'
        }, {  
            'id':'name',
            'name':'name',
            'string':'Label',
            'required':True,
            'fields':[],
            'type':'char'
        }, {  
            'id':'partner_name',
            'name':'partner_name',
            'string':'Partner Name',
            'required':False,
            'fields':[],
            'type':'char'
        }, {  
            'id':'partner_id',
            'name':'partner_id',
            'string':'Partner',
            'required':False,
            'fields':[{  
                'id':'partner_id',
                'name':'id',
                'string':'External ID',
                'required':False,
                'fields':[],
                'type':'id'
            }, {  
                'id':'partner_id',
                'name':'.id',
                'string':'Database ID',
                'required':False,
                'fields':[],
                'type':'id'
            }],
            'type':'many2one'
        }, {  
            'id':'ref',
            'name':'ref',
            'string':'Reference',
            'required':False,
            'fields':[],
            'type':'char'
        }, {  
            'id':'note',
            'name':'note',
            'string':'Notes',
            'required':False,
            'fields':[],
            'type':'text'
        }, {  
            'id':'amount',
            'name':'amount',
            'string':'Amount',
            'required':False,
            'fields':[],
            'type':'monetary'
        }, {  
            'id':'amount_currency',
            'name':'amount_currency',
            'string':'Amount Currency',
            'required':False,
            'fields':[],
            'type':'monetary'
        }, {  
            'id':'currency_id',
            'name':'currency_id',
            'string':'Currency',
            'required':False,
            'fields':[{  
                'id':'currency_id',
                'name':'id',
                'string':'External ID',
                'required':False,
                'fields':[],
                'type':'id'
            }, {  
                'id':'currency_id',
                'name':'.id',
                'string':'Database ID',
                'required':False,
                'fields':[],
                'type':'id'
            }],
            'type':'many2one'
        }, {
            'id':'balance',
            'name':'balance',
            'string':'Cumulative Balance',
            'required':False,
            'fields':[],
            'type':'monetary',
        }]

    def _parse_float(self, value):
        return float(value) if value else 0.0
    
    def _prepare_statement(self):
        date = datetime.date.today().strftime(DEFAULT_SERVER_DATE_FORMAT)
        filename = self.file_name and os.path.splitext(self.file_name)[0] or ""
        return self.env['account.bank.statement'].create({
            'journal_id': self._context.get('journal_id', False),
            'name': _("%s - Import %s") % (date, filename),
            'reference': self.file_name})
    
    def _update_statement(self, data, import_fields, options):
        vals = {}
        date_index = import_fields.index('date') if 'date' in import_fields else False
        balance_index = import_fields.index('balance') if 'balance' in import_fields else False
        statment_index = import_fields.index('statement_id/.id')
        if date_index:
            vals['date'] = data[len(data) - 1][date_index]
        if balance_index:
            self._parse_float_from_data(data, balance_index, 'balance', options)
            vals['balance_start'] = self._parse_float(data[0][balance_index])
            vals['balance_end_real'] = self._parse_float(data[len(data) - 1][balance_index])
        self.env['account.bank.statement'].browse(data[0][statment_index]).write(vals)
    
    @api.model
    def _convert_import_data(self, fields, options):
        data, import_fields = super(AccountBankStatementImportWizard, self)._convert_import_data(fields, options)
        bank_statement = self._prepare_statement()
        import_fields.append('sequence')
        import_fields.append('statement_id/.id')
        for index, row in enumerate(data):
            row.append(index)
            row.append(bank_statement.id)
        return data, import_fields
    
    @api.multi
    def _parse_import_data(self, data, import_fields, options):
        parsed_data = super(AccountBankStatementImportWizard, self)._parse_import_data(data, import_fields, options)
        self._update_statement(parsed_data, import_fields, options)
        balance_index = import_fields.index('balance') if 'balance' in import_fields else False
        amount_index = import_fields.index('amount') if 'amount' in import_fields else False
        bank_data = []
        for row in parsed_data:
            if row[amount_index]:
                if balance_index:
                    del row[balance_index]
                bank_data.append(row)
        if balance_index:
            import_fields.remove('balance')
        return bank_data

    @api.multi
    def do(self, fields, options, dryrun=False):
        self._cr.execute('SAVEPOINT import_bank_statement')
        res = super(AccountBankStatementImportWizard, self).do(fields, options, dryrun)
        try:
            if dryrun:
                self._cr.execute('ROLLBACK TO SAVEPOINT import_bank_statement')
            else:
                self._cr.execute('RELEASE SAVEPOINT import_bank_statement')
        except psycopg2.InternalError as e:
            _logger.debug(e)
        return res
