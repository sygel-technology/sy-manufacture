# Copyright 2023 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'MRP BOM Warn Message',
    'summary': '''
        Add a configurable warning when a bill of materials
        is selected on a MRP manufacturing order.
    ''',
    'version': '15.0.1.0.0',
    'category': 'MRP',
    'website': 'https://github.com/sygel-technology/sy-manufacture',
    'author': 'Alberto Martínez, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'mrp',
    ],
    'data': [
        'security/mrp_bom_warn_message_security.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
    ],
}
