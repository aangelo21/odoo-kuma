# -*- coding: utf-8 -*-
{
    'name': "Gestión Comerciales",

    'summary': "Módulo para la gestión comercial con gráficos de captación de alumnos",

    'description': """
Sistema completo de gestión comercial que permite:
- Registrar captación de alumnos por trabajador
- Visualizar gráficos de barras interactivos
- Dashboard con estadísticas en tiempo real
- Integración con módulo de empleados y categorías
    """,

    'author': "Tu Empresa",
    'website': "https://www.tuempresa.com",

    'category': 'Sales',
    'version': '1.0',

    # Dependencias necesarias
    'depends': ['base', 'hr', 'gestion_cursos', 'web'],

    # Archivos de datos
    'data': [
        'security/ir.model.access.csv',
        'views/captacion_alumnos_views.xml',
        'views/captacion_actions.xml',
        'views/captacion_menus.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}

