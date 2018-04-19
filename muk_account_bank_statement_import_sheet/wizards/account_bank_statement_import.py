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
import base64
import logging

from odoo import api, models
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)

class AccountBankStatementImport(models.TransientModel):
    
    _inherit = "account.bank.statement.import"

    def _check_csv(self, data_file, filename):
        return guess_mimetype(data_file) == 'text/csv' or \
             filename and os.path.splitext(filename)[1] == '.csv'
                 
    def _check_xls(self, data_file, filename):
        return guess_mimetype(data_file) == 'application/vnd.ms-excel' or \
             filename and os.path.splitext(filename)[1] == '.xls'
            
    def _check_xlsx(self, data_file, filename):
        return guess_mimetype(data_file) == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or \
             filename and os.path.splitext(filename)[1] == '.xlsx'
             
    def _check_ods(self, data_file, filename):
        return guess_mimetype(data_file) == 'application/vnd.oasis.opendocument.spreadsheet' or \
             filename and os.path.splitext(filename)[1] == '.ods'

    @api.multi
    def import_file(self):
        if self._check_csv(self.data_file, self.filename) or \
            self._check_xls(self.data_file, self.filename) or \
            self._check_xlsx(self.data_file, self.filename) or \
            self._check_ods(self.data_file, self.filename):
            import_wizard = self.env['account.bank.statement.import.wizard'].create({
                'res_model': "account.bank.statement.line",
                'file_name': self.filename,
                'file': base64.b64decode(self.data_file),
            })
            ctx = dict(self.env.context)
            ctx['wizard_id'] = import_wizard.id
            return {
                'type': 'ir.actions.client',
                'tag': 'import_bank_statement',
                'params': {
                    'model': "account.bank.statement.line",
                    'filename': self.filename,
                    'context': ctx,
                }
            }
        else:
            return super(AccountBankStatementImport, self).import_file()