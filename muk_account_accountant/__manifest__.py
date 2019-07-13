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

{
    'name': 'MuK Accounting and Finance',
    'summary': 'Financial and Analytic Accounting',
    'version': '12.0.2.0.0',   
    'category': 'Accounting',
    'license': 'LGPL-3',
    'author': 'MuK IT',
    'website': 'https://www.mukit.at',
    'live_test_url': 'https://mukit.at/r/SgN',
    'contributors': [
        'Mathias Markl <mathias.markl@mukit.at>',
    ],
    'depends': [
        'account',
        'muk_web_utils',
    ],
    'excludes': [
        'account_accountant',
    ],
    'data': [
        'security/accountant_security.xml',
        'views/accountant_menu.xml',
        'views/digest_views.xml',
        'views/res_config_settings_view.xml',
        'data/digest_data.xml',
    ],
    'demo': [
        'demo/accountant_demo.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
}
