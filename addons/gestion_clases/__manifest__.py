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

    'depends': ['base', 'gestion_cursos'],    'data': [
        'security/ir.model.access.csv',
        'views/root_menu.xml',
        'views/aula_list_view.xml',
        'views/aula_form_view.xml',
        'views/aula_actions.xml',
        'views/aula_menu.xml',
        'views/horario_form_view.xml',
        'views/horario_list_view.xml',
        'views/horario_search_view.xml',
        'views/horario_kanban_view.xml',
        'views/horario_kanban_diario_view.xml',
        'views/horario_actions.xml',
        'views/horario_menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

