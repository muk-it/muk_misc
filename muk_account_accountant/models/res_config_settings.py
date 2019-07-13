###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Accounting and Finance 
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

import datetime
import calendar

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    
    _inherit = 'res.config.settings'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    fiscalyear_last_day = fields.Integer(
        related='company_id.fiscalyear_last_day',
        readonly=False)

    fiscalyear_last_month = fields.Selection(
        related='company_id.fiscalyear_last_month',
        readonly=False)
    
    period_lock_date = fields.Date(
        related='company_id.period_lock_date',
        readonly=False)

    fiscalyear_lock_date = fields.Date(
        related='company_id.fiscalyear_lock_date',
        readonly=False)
    
    module_muk_account_bank_statement_import_sheet = fields.Boolean(
        string="Sheet Import",
        help="Import your bank statements in CSV/XLS/XLSX/ODS.")
    
    #----------------------------------------------------------
    # View
    #----------------------------------------------------------
    
    @api.onchange('fiscalyear_last_month')
    def _onchange_fiscalyear_last_month(self):
        year = datetime.datetime.now().year
        month = self.fiscalyear_last_month
        self.fiscalyear_last_day = calendar.monthrange(year, month)[1]