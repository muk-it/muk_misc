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
import base64
import logging

from odoo import api, models
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)

MIMETYPE_CSV = 'text/csv'
MIMETYPE_XLS = 'application/vnd.ms-excel'
MIMETYPE_ODS = 'application/vnd.oasis.opendocument.spreadsheet'
MIMETYPE_XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

class AccountBankStatementImport(models.TransientModel):
    
    _inherit = "account.bank.statement.import"

    def _check_csv(self, data_file, filename):
        return filename and os.path.splitext(filename)[1] == '.csv' or \
            guess_mimetype(data_file) == MIMETYPE_CSV

    def _check_xls(self, data_file, filename):
        return filename and os.path.splitext(filename)[1] == '.xls' or \
            guess_mimetype(data_file) == MIMETYPE_XLS
            
    def _check_xlsx(self, data_file, filename):
        return filename and os.path.splitext(filename)[1] == '.xlsx' or \
            guess_mimetype(data_file) == MIMETYPE_XLSX
            
    def _check_ods(self, data_file, filename):
        return filename and os.path.splitext(filename)[1] == '.ods' or \
            guess_mimetype(data_file) == MIMETYPE_ODS

    @api.multi
    def import_file(self):
        if self._check_csv(self.data_file, self.filename):
            return self._import_wizard(self.filename, self.data_file, MIMETYPE_CSV)
        elif self._check_xls(self.data_file, self.filename):
            return self._import_wizard(self.filename, self.data_file, MIMETYPE_XLS)
        elif self._check_xlsx(self.data_file, self.filename):
            return self._import_wizard(self.filename, self.data_file, MIMETYPE_XLSX)
        elif self._check_ods(self.data_file, self.filename):
            return self._import_wizard(self.filename, self.data_file, MIMETYPE_ODS)
        return super(AccountBankStatementImport, self).import_file()
        
    @api.model
    def _import_wizard(self, file_name, file, file_type):
        wizard = self.env['account.bank.statement.import.wizard'].create({
            'res_model': "account.bank.statement.line",
            'file_type': 'text/csv',
            'file_name': self.filename,
            'file': base64.b64decode(self.data_file),
        })
        context = dict(self.env.context)
        context.update({'wizard_id': wizard.id})
        return {
            'type': 'ir.actions.client',
            'tag': 'import_bank_statement',
            'params': {
                'model': "account.bank.statement.line",
                'filename': self.filename,
                'context': context,
            }
        }
            