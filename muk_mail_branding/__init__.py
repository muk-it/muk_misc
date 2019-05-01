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

import ast
import datetime

from odoo import api, osv, SUPERUSER_ID
from odoo.release import version_info
from odoo.tools import config, convert_file
from odoo.modules.module import get_module_resource

from . import models

#----------------------------------------------------------
# Hooks
#----------------------------------------------------------

def _install_debrand_system(cr, registry):
    if version_info[5] != 'e':
        env = api.Environment(cr, SUPERUSER_ID, {})
        domain = env.ref('base.ir_cron_act').domain
        record = env.ref('mail.ir_cron_module_update_notification', False)
        if record and record.exists():
            env.ref('base.ir_cron_act').write({
                'domain': "[]"
            })
            record.unlink()
        
def _uninstall_rebrand_system(cr, registry):
    if version_info[5] != 'e':
        filename = get_module_resource('mail', 'data', 'ir_cron_data.xml')
        convert_file(cr, 'mail', filename, {}, 'init', False, 'data', registry._assertion_report)