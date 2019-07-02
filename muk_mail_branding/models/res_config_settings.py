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

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    branding_system_user = fields.Many2one(
        comodel_name='res.users', 
        string='System User', 
        required=True,
        default=lambda self: self.sudo().env.user.id)
    
    branding_branding_system_image = fields.Binary(
        string='System User Image',
        related='branding_system_user.image',
        readonly=False)
    
    branding_branding_system_name = fields.Char(
        string='System User Name',
        related='branding_system_user.name',
        readonly=False)
    
    branding_branding_system_email = fields.Char(
        string='System User Email',
        related='branding_system_user.email',
        readonly=False)