{
    'name': 'Real Estate',
    'version':'1.0',
    'category':'Real Esate/brokerage',
    'summary':'manage property Advertisment',
    'description': 'A module to manage real estate listings as per the Odoo 19.0 tutorial.',
    'author':'Abel Meles',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv'
        'views/estate_property_views.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    
}
