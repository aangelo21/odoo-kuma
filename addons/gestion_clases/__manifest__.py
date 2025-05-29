{
    'name': "Gestion de Aulas",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

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

