
# -*- coding: utf-8 -*-
{
    'name': 'Tienda de Ropa SGE',
    'summary': 'Gestion de una tienda de ropa',
    'description': 'Aplicacion para gestionar productos, empleados y ventas de una tienda de ropa.',
    'author': 'Alberto',
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base'],
    'data': [
    'security/ir.model.access.csv',
    'views/producto_views.xml',
    'views/empleado_views.xml',
    'views/venta_views.xml',
    ],
    'installable': True,
    'application': True,
}
