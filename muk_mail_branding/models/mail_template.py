###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Mail Branding 
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

from odoo import _, api, models

class MailTemplate(models.Model):
    
    _inherit = 'mail.template'
    
    @api.model
    def _render_template(self, template_txt, model, res_ids, post_process=False):
        res = super(MailTemplate, self)._render_template(
            template_txt, model, res_ids, post_process=post_process,
        )
        if isinstance(res, str):
            res = self.env['muk_branding.debranding'].debrand(res)
        else:
            for res_id, body in res.items():
                res[res_id] = self.env['muk_branding.debranding'].debrand(body)
        return res