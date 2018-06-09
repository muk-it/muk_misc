###################################################################################
# 
#    Copyright (C) 2017 MuK IT GmbH
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

from odoo import models, fields, api

class AccessGroups(models.Model):

    _inherit = 'muk_security.groups'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
  
    departments = fields.Many2many(
        comodel_name='hr.department',
        relation='muk_groups_department_rel',
        column1='gid',
        column2='did',
        string='Departments')
    
    jobs = fields.Many2many(
        comodel_name='hr.job',
        relation='muk_groups_job_rel',
        column1='gid',
        column2='jid',
        string='Jobs')
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    @api.model
    def check_user_values(self, values):
        check = any(field in values for field in ['departments', 'jobs'])
        if super(AccessGroups, self).check_user_values(values) or check:
            return True
        return False

    @api.multi
    def get_users(self):
        users = super(AccessGroups, self).get_users()
        employees = record.env['hr.employee']
        employees |= record.departments.mapped('manager_id')
        employees |= record.departments.mapped('member_ids')
        employees |= record.jobs.mapped('employee_ids')
        for employee in employees:
            users += employee.user_id
        return users
        