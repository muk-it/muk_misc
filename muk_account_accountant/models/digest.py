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

from odoo import fields, models, _
from odoo.exceptions import AccessError

class Digest(models.Model):

    _inherit = 'digest.digest'

    #----------------------------------------------------------
    # KPI
    #----------------------------------------------------------

    kpi_account_total_expense = fields.Boolean(
        string="Expense")

    kpi_account_total_expense_value = fields.Monetary(
        compute='_compute_kpi_account_total_expense_value',
        string="Expense Value")

    kpi_account_total_bank = fields.Boolean(
        string="Bank")

    kpi_account_total_bank_value = fields.Monetary(
        compute='_compute_kpi_account_total_bank_value',
        string="Bank Value")

    kpi_account_total_cash = fields.Boolean(
        string="Cash")

    kpi_account_total_cash_value = fields.Monetary(
        compute='_compute_kpi_account_total_cash_value',
        string="Cash Value")

    #----------------------------------------------------------
    # Computation
    #----------------------------------------------------------

    def _compute_kpi_account_total_expense_value(self):
        if not self.env.user.has_group('account.group_account_invoice'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            account_moves = self.env['account.move'].read_group([
                ('journal_id.type', '=', 'purchase'),
                ('company_id', '=', company.id),
                ('date', '>=', start),
                ('date', '<', end)], ['journal_id', 'amount'], ['journal_id'])
            record.kpi_account_total_expense_value = sum([account_move['amount'] for account_move in account_moves])

    def _compute_kpi_account_total_bank_value(self):
        if not self.env.user.has_group('account.group_account_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            account_moves = self.env['account.move'].read_group([
                ('journal_id.type', '=', 'bank'),
                ('company_id', '=', company.id),
                ('date', '>=', start),
                ('date', '<', end)], ['journal_id', 'amount'], ['journal_id'])
            record.kpi_account_total_bank_value = sum([account_move['amount'] for account_move in account_moves])

    def _compute_kpi_account_total_cash_value(self):
        if not self.env.user.has_group('account.group_account_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            account_moves = self.env['account.move'].read_group([
                ('journal_id.type', '=', 'cash'),
                ('company_id', '=', company.id),
                ('date', '>=', start),
                ('date', '<', end)], ['journal_id', 'amount'], ['journal_id'])
            record.kpi_account_total_bank_value = sum([account_move['amount'] for account_move in account_moves])

    def compute_kpis_actions(self, company, user):
        res = super(Digest, self).compute_kpis_actions(company, user)
        res.update({
            'kpi_account_total_expense': 'account.action_invoice_tree2&menu_id=%s' % (self.env.ref('account.menu_finance').id),
            'kpi_account_total_bank': 'account.open_account_journal_dashboard_kanban&menu_id=%s' % (self.env.ref('account.menu_finance').id),
            'kpi_account_total_cash': 'account.open_account_journal_dashboard_kanban&menu_id=%s' % (self.env.ref('account.menu_finance').id)})
        return res
