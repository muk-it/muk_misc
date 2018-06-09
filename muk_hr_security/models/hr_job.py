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

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class AccessJob(models.Model):

    _inherit = 'hr.job'

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    groups = fields.Many2many(
        comodel_name='muk_security.groups',
        relation='muk_groups_job_rel',
        column1='jid',
        column2='gid',
        string='Groups')
    
    #----------------------------------------------------------
    # Create, Update, Delete
    #----------------------------------------------------------
    
    @api.multi
    def write(self, vals):
        result = super(AccessJob, self).write(vals)
        if any(field in vals for field in ['employee_ids', 'department_id']):
            for record in self:
                for group in record.groups:
                    group.trigger_computation(['users'])
        return result
    
    @api.multi
    def unlink(self):
        groups = self.env['muk_security.groups']
        for record in self:
            groups |= record.groups
        result = super(AccessJob, self).unlink()
        for group in groups:
            group.trigger_computation(['users'])
        return result