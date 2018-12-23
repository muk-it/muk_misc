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

import logging

from odoo import models, api
from odoo.release import version_info

_logger = logging.getLogger(__name__)

class PublisherWarrantyContract(models.AbstractModel):
    
    _inherit = 'publisher_warranty.contract'

    @api.multi
    def update_notification(self, cron_mode=True):
        if version_info[5] == 'e':
            return super(PublisherWarrantyContract, self).update_notification(cron_mode)
        else:
            return True