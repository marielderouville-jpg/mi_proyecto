{
    'name': 'Facturación',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Sistema de facturación personalizado para proyectos escolares',
    'author': 'Tu Nombre',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/factura_views.xml',
    ],
    'installable': True,
    'application': True,
}