# -*- coding: utf-8 -*-
{
    'name': "Temas Kuma",
    'summary': "Módulo para los estilos de la aplicación",
    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',    'depends': ['base'],
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

