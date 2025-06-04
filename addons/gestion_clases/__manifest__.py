{
    'name': "Gestión Aulas",

    'summary': "Módulo para la gestión de las aulas",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'gestion_cursos'],
    'data': [
        'security/ir.model.access.csv',
        'views/aula_vista.xml',
        'views/horario_vista.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

