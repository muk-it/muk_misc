###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Bank Statement Import 
#    (see https://mukit.at).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

import os
import datetime
import logging

from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)

class BaseTestCase(common.TransactionCase):
    
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.currency_id = self.env.ref('base.EUR').id
        self.bank_journal = self.env['account.journal'].create({
            'name': 'Test Bank',
            'code': 'TB1', 
            'type': 'bank',            
            'bank_acc_number': '0000',
            'currency_id': self.currency_id})
        self.options = {
            'headers': True,
            'encoding': 'utf-8',
            'separator': ';',
            'quoting': '"',
            'date_format': '%d.%m.%y',
            'float_thousand_separator': '.',
            'float_decimal_separator': ','}
        
    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        
    def run_import_with_amount(self, file_name, file_type):
        fields = ['date', 'name', 'amount', 'balance']
        with open(os.path.join(_path, 'tests/data', file_name), 'rb') as file:
            import_wizard = self.env['account.bank.statement.import.wizard'].create({
                'res_model': 'account.bank.statement.line',
                'file': file.read(),
                'file_name': file_name,
                'file_type': file_type})
            import_wizard.with_context(journal_id=self.bank_journal.id).do(fields, [], self.options)
            statement = self.env['account.bank.statement'].search([('reference', '=', file_name)], limit=1)
            self.assertEqual(statement.balance_start, 5000.00)
            self.assertEqual(statement.balance_end_real, 20795.00)
            line = statement.line_ids.filtered(lambda rec: rec.name == 'STATEMENT 10')
            self.assertEqual(line.date, datetime.date(2018, 1, 8))
            self.assertEqual(line.amount, -2516.00)
    
    def run_import_with_partner(self, file_name, file_type):
        fields = ['date', 'name', 'partner_id', 'balance', 'amount']
        with open(os.path.join(_path, 'tests/data', file_name), 'rb') as file:
            import_wizard = self.env['account.bank.statement.import.wizard'].create({
                'res_model': 'account.bank.statement.line',
                'file': file.read(),
                'file_name': file_name,
                'file_type': file_type})
            import_wizard.with_context(journal_id=self.bank_journal.id).do(fields, [], self.options)
            statement = self.env['account.bank.statement'].search([('reference', '=', file_name)], limit=1)
            line = statement.line_ids.filtered(lambda rec: rec.name == 'STATEMENT 15')
            self.assertEqual(line.partner_id.name, "Azure Interior")
            
    def test_import_csv_with_amount(self):
        self.run_import_with_amount(
            'test_amount.csv',
            'text/csv')
    
    def test_import_csv_with_partner(self):
        self.run_import_with_partner(
            'test_partner.csv',
            'text/csv')
        
    def test_import_ods_with_amount(self):
        self.run_import_with_amount(
            'test_amount.ods',
            'application/vnd.oasis.opendocument.spreadsheet')

    def test_import_ods_with_partner(self):
        self.run_import_with_partner(
            'test_partner.ods',
            'application/vnd.oasis.opendocument.spreadsheet')
        
    def test_import_xls_with_amount(self):
        self.run_import_with_amount(
            'test_amount.xls',
            'application/vnd.ms-excel')
    
    def test_import_xls_with_partner(self):
        self.run_import_with_partner(
            'test_partner.xls',
            'application/vnd.ms-excel')

    def test_import_xlsx_with_amount(self):
        self.run_import_with_amount(
            'test_amount.xlsx',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    def test_import_xlsx_with_partner(self):
        self.run_import_with_partner(
            'test_partner.xlsx', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')