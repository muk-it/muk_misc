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

{
    "name": "MuK Mail Branding",
    "summary": """Branding and Debranding""",
    "version": "12.0.2.0.0",
    "category": "Discuss",
    "license": "LGPL-3",
    "website": "http://www.mukit.at",
    'live_test_url': 'https://mukit.at/r/SgN',
    "author": "MuK IT",
    "contributors": [
        "Mathias Markl <mathias.markl@mukit.at>",
    ],
    "depends": [
        "digest",
        "mail_bot",
        "muk_web_branding",
    ],
    "data": [
        "data/users.xml",
        "data/digest.xml",
        "template/layout.xml",
        "views/res_config_settings_view.xml",
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    "images": [
        'static/description/banner.png'
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    'auto_install': True,
    "application": False,
    "installable": True,
    "post_init_hook": "_install_debrand_system",
    "uninstall_hook": "_uninstall_rebrand_system",
}