# -*- coding: utf-8 -*-
{
    'name': "Gestión Cursos",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/calendario_vista.xml',
        'views/curso_vista.xml',
        'views/categoria_vista.xml',
        'views/familia_profesional_vista.xml',
        # 'views/views.xml',
        'views/templates.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'gestion_cursos/static/scss/custom_colors.scss',
        'gestion_cursos/static/scss/iconos-actuales.scss',
        'gestion_cursos/static/scss/font-size.scss',
    ],
    'web.assets_frontend': [
        'gestion_cursos/static/css/login.css',
    ],
},
    # only loaded in demonstration mode
    # 'demo': [
    #    'demo/demo.xml',
    #],
}

