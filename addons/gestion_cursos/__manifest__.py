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
        # 'views/calendario_vista.xml',
        'views/curso_vista.xml',
        'views/categoria_vista.xml',
        'views/familia_profesional_vista.xml',
        'views/templates.xml',
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

