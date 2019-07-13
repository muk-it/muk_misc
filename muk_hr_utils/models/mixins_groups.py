###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK HR Utils 
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

from odoo import models, fields, api

class Groups(models.AbstractModel):

    _inherit = 'muk_utils.mixins.groups'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    @api.model
    def _add_magic_fields(self):
        super(Groups, self)._add_magic_fields()
        def add(name, field):
            if name not in self._fields:
                self._add_field(name, field)
        add('departments', fields.Many2many(
            _module=self._module,
            comodel_name='hr.department',
            relation='%s_department_rel' % (self._table),
            column1='gid',
            column2='did',
            string='Departments',
            automatic=True))
        add('jobs', fields.Many2many(
            _module=self._module,
            comodel_name='hr.job',
            relation='%s_job_rel' % (self._table),
            column1='gid',
            column2='jid',
            string='Jobs',
            automatic=True))
    
    #----------------------------------------------------------
    # Read, View 
    #----------------------------------------------------------
    
    @api.depends('departments', 'departments.manager_id', 'departments.member_ids', 'jobs', 'jobs.employee_ids')
    def _compute_users(self):
        super(Groups, self)._compute_users()
        for record in self:
            employees = self.mapped('jobs.employee_ids')
            employees |= self.mapped('departments.manager_id')
            employees |= self.mapped('departments.member_ids')
            users = record.users | employees.mapped('user_id')
            record.update({'users': users, 'count_users': len(users)})