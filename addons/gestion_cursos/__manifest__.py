{
    'name': "Gestión Cursos",
    'summary': "Módulo para la gestión de los cursos",
    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/curso_calendar_view.xml',
        'views/curso_list_view.xml',
        'views/curso_form_view.xml',
        'views/curso_actions.xml',
        'views/curso_menu.xml',
        'views/categoria_list_view.xml',
        'views/categoria_form_view.xml',
        'views/categoria_actions.xml',
        'views/categoria_menu.xml',
        'views/familia_profesional_list_view.xml',
        'views/familia_profesional_form_view.xml',
        'views/familia_profesional_actions.xml',
        'views/familia_profesional_menu.xml',
        'views/favicon.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gestion_cursos/static/scss/custom_colors.scss',
            'gestion_cursos/static/scss/iconos-actuales.scss',
            'gestion_cursos/static/scss/font-size.scss',
        ],
        'web.assets_frontend': [
            'gestion_cursos/static/scss/custom_colors.scss',
            'gestion_cursos/static/css/login.css',
        ],
    },
}

