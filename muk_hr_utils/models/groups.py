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

class Groups(models.AbstractModel):

    _inherit = 'muk_utils.groups'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    @api.model
    def _add_magic_fields(self):
        super(Groups, self)._add_magic_fields()
        def add(name, field):
            if name not in self._fields:
                self._add_field(name, field)
        base, model = self._name.split(".")
        add('departments', fields.Many2many(
            _module=base,
            comodel_name='hr.department',
            relation='%s_department_rel' % (self._table),
            column1='gid',
            column2='did',
            string='Departments',
            automatic=True))
        add('jobs', fields.Many2many(
            _module=base,
            comodel_name='hr.job',
            relation='%s_job_rel' % (self._table),
            column1='gid',
            column2='jid',
            string='Jobs',
            automatic=True))
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    @api.model
    def check_user_values(self, values):
        check = any(field in values for field in ['departments', 'jobs'])
        if super(Groups, self).check_user_values(values) or check:
            return True
        return False

    @api.multi
    def get_users(self):
        users = super(Groups, self).get_users()
        employees = self.env['hr.employee']
        employees |= self.departments.mapped('manager_id')
        employees |= self.departments.mapped('member_ids')
        employees |= self.jobs.mapped('employee_ids')
        for employee in employees:
            users += employee.user_id
        return users
        