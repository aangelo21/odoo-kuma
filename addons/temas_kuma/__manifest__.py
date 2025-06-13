# -*- coding: utf-8 -*-
{
    'name': "Tema Kuma",
    'summary': "Módulo para los estilos de la aplicación",
    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",    'category': 'Themes/Backend',
    'version': '0.1',
    'installable': True,
    'auto_install': False,
    'application': False,
    'depends': ['base', 'web'],    'data': [
        'templates/favicon_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'temas_kuma/static/scss/custom_colors.scss',
            'temas_kuma/static/scss/iconos-actuales.scss',
            'temas_kuma/static/scss/font-size.scss',
        ],
        'web.assets_frontend': [
            'temas_kuma/static/scss/custom_colors.scss',
            'temas_kuma/static/css/login.css',
        ],
    },
}

