from odoo import models, fields, api  # type: ignore
import logging

_logger = logging.getLogger(__name__)

class CaptacionAlumnos(models.Model):
    _name = 'gestion_comerciales.captacion_alumnos'
    _description = 'Captación de Alumnos por Trabajador'
    _rec_name = 'display_name'

    empleado_id = fields.Many2one(
        'hr.employee',
        string='Trabajador',
        required=True,
        help='Empleado que captó los alumnos'
    )
    categoria_id = fields.Many2one(
        'gestion_cursos.categoria',
        string='Categoría',
        required=True,
        help='Categoría del curso de los alumnos captados'
    )
    numero_alumnos = fields.Integer(
        string='Número de Alumnos',
        required=True,
        help='Cantidad de alumnos captados'
    )

    display_name = fields.Char(
        string='Nombre para mostrar',
        compute='_compute_display_name',
        store=True
    )

    @api.depends('empleado_id', 'categoria_id', 'numero_alumnos')
    def _compute_display_name(self):
        for record in self:
            if record.empleado_id and record.categoria_id:
                record.display_name = f"{record.empleado_id.name} - {record.categoria_id.nombre} ({record.numero_alumnos} alumnos)"
            else:
                record.display_name = "Captación de Alumnos"

    @api.model
    def get_chart_data(self):
        """Obtiene los datos para el gráfico de barras"""
        try:
            # Buscar todos los registros de captación
            captaciones = self.search([])

            if not captaciones:
                return {
                    'labels': [],
                    'totals': [],
                    'details': []
                }

            # Agrupar por empleado
            empleado_data = {}

            for captacion in captaciones:
                empleado_name = captacion.empleado_id.name
                categoria_name = captacion.categoria_id.nombre
                categoria_color = captacion.categoria_id.color or '#808080'
                alumnos = captacion.numero_alumnos

                if empleado_name not in empleado_data:
                    empleado_data[empleado_name] = {
                        'total': 0,
                        'categorias': {}
                    }

                empleado_data[empleado_name]['total'] += alumnos

                if categoria_name not in empleado_data[empleado_name]['categorias']:
                    empleado_data[empleado_name]['categorias'][categoria_name] = {
                        'alumnos': 0,
                        'color': categoria_color
                    }

                empleado_data[empleado_name]['categorias'][categoria_name]['alumnos'] += alumnos

            # Ordenar por total de alumnos (descendente)
            sorted_empleados = sorted(empleado_data.items(), key=lambda x: x[1]['total'], reverse=True)

            # Preparar datos para el gráfico
            labels = [emp[0] for emp in sorted_empleados]
            totals = [emp[1]['total'] for emp in sorted_empleados]
            details = [
                [
                    {
                        'categoria': cat,
                        'alumnos': info['alumnos'],
                        'color': info['color']
                    } for cat, info in emp[1]['categorias'].items()
                ]
                for emp in sorted_empleados
            ]

            return {
                'labels': labels,
                'totals': totals,
                'details': details
            }

        except Exception as e:
            _logger.error(f"Error en get_chart_data: {str(e)}")
            return {
                'labels': [],
                'totals': [],
                'details': []
            }
