from odoo import models, fields, api  # type: ignore
import logging
from datetime import datetime, timedelta

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
    
    fecha = fields.Date(
        string='Fecha',
        default=fields.Date.today,
        required=True,
        help='Fecha de captación de alumnos'
    )

    # Campos calculados para filtros de fecha
    mes = fields.Selection(
        [
            ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'),
            ('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'),
            ('07', 'Julio'), ('08', 'Agosto'), ('09', 'Septiembre'),
            ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
        ],
        string='Mes',
        compute='_compute_fecha_parts',
        store=True,
        help='Mes de la fecha de captación'
    )

    año = fields.Integer(
        string='Año',
        compute='_compute_fecha_parts',
        store=True,
        help='Año de la fecha de captación'
    )
    mes_año = fields.Char(
        string='Mes/Año',
        compute='_compute_fecha_parts',
        store=True,
        help='Mes y año de la fecha de captación'
    )

    display_name = fields.Char(
        string='Nombre para mostrar',
        compute='_compute_display_name',
        store=True
    )

    @api.depends('fecha')
    def _compute_fecha_parts(self):
        """Calcula las partes de la fecha para filtros"""
        for record in self:
            if record.fecha:
                record.mes = record.fecha.strftime('%m')
                record.año = record.fecha.year
                record.mes_año = record.fecha.strftime('%m/%Y')
            else:
                record.mes = False
                record.año = False
                record.mes_año = False

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        user = self.env.user
        if not user.has_group('base.group_system'):
            empleado = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
            if empleado:
                res['empleado_id'] = empleado.id
        return res
    
    @api.depends('empleado_id', 'categoria_id', 'numero_alumnos', 'fecha')
    def _compute_display_name(self):
        for record in self:
            if record.empleado_id and record.categoria_id:
                fecha_str = record.fecha.strftime('%d/%m/%Y') if record.fecha else ''
                record.display_name = f"{record.empleado_id.name} - {record.categoria_id.nombre} ({record.numero_alumnos} alumnos) - {fecha_str}"
            else:
                record.display_name = "Captación de Alumnos"

    @api.model
    def get_chart_data(self):
        """Obtiene los datos para el gráfico de barras"""
        try:
            # Buscar todos los registros de captación
            captaciones = self.sudo().search([])

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
    
    @api.model
    def _get_group_employees(self):
        group_jefa = self.env.ref('gestion_cursos.group_jefa_comercial')
        group_coord = self.env.ref('gestion_cursos.group_coordinacion')
        users = group_jefa.users | group_coord.users
        return self.env['hr.employee'].search([
            ('user_id', 'in', users.ids),
            ('work_email', '!=', False)
        ])

    @api.model
    def enviar_informe_diario_captacion(self):
        """Envía un informe diario de captación de alumnos por comercial"""
        try:
            hoy = fields.Date.today()
            captaciones_hoy = self.sudo().search([('fecha', '=', hoy)])
            if not captaciones_hoy:
                _logger.info(f"No hay captaciones para el día {hoy}")
                return

            employees = self._get_group_employees()
            if not employees:
                _logger.warning("No hay empleados de grupo jefa comercial o coordinación con email")
                return

            empleado_data = {}
            total_alumnos_dia = 0

            for captacion in captaciones_hoy:
                empleado_name = captacion.empleado_id.name
                categoria_name = captacion.categoria_id.nombre
                alumnos = captacion.numero_alumnos
                total_alumnos_dia += alumnos

                empleado_data.setdefault(empleado_name, {'total': 0, 'categorias': {}})
                empleado_data[empleado_name]['total'] += alumnos
                empleado_data[empleado_name]['categorias'].setdefault(categoria_name, 0)
                empleado_data[empleado_name]['categorias'][categoria_name] += alumnos

            sorted_empleados = sorted(empleado_data.items(), key=lambda x: x[1]['total'], reverse=True)

            bloques = ["<h3>📊 Resumen de Captación por Comercial:</h3><ul>"]
            for empleado_name, data in sorted_empleados:
                bloques.append(f"<li><strong>{empleado_name}</strong>: {data['total']} alumnos<ul>")
                for categoria, cantidad in data['categorias'].items():
                    bloques.append(f"<li>{categoria}: {cantidad} alumnos</li>")
                bloques.append("</ul></li>")
            bloques.append("</ul>")
            bloques.append(f"<p><strong>Total del día:</strong> {total_alumnos_dia} alumnos captados</p>")

            cuerpo = f"""
                <html>
                    <body>
                        <p>📅 <strong>Informe Diario de Captación de Alumnos - {hoy.strftime('%d/%m/%Y')}</strong></p>
                        {''.join(bloques)}
                        <hr>
                        <p><em>Este es un informe automático del sistema de gestión comercial.</em></p>
                    </body>
                </html>
            """

            self.env['mail.mail'].create({
                'subject': f'📊 Informe Diario de Captación - {hoy.strftime("%d/%m/%Y")}',
                'body_html': cuerpo.strip(),
                'email_from': self.env.user.email,
                'email_to': ','.join(employees.mapped('work_email')),
            }).send()

            _logger.info(f"Informe diario de captación enviado para el día {hoy}")

        except Exception as e:
            _logger.error(f"Error al enviar informe diario de captación: {str(e)}")

    @api.model
    def enviar_informe_semanal_captacion(self):
        """Envía un informe semanal de captación de alumnos por comercial"""
        try:
            hoy = fields.Date.today()
            lunes = hoy - timedelta(days=hoy.weekday())
            viernes = lunes + timedelta(days=4)

            captaciones_semana = self.sudo().search([
                ('fecha', '>=', lunes),
                ('fecha', '<=', viernes)
            ])
            if not captaciones_semana:
                _logger.info(f"No hay captaciones para la semana {lunes} - {viernes}")
                return

            employees = self._get_group_employees()
            if not employees:
                _logger.warning("No hay empleados de grupo jefa comercial o coordinación con email")
                return

            empleado_data = {}
            total_alumnos_semana = 0

            for captacion in captaciones_semana:
                empleado_name = captacion.empleado_id.name
                categoria_name = captacion.categoria_id.nombre
                alumnos = captacion.numero_alumnos
                total_alumnos_semana += alumnos

                empleado_data.setdefault(empleado_name, {'total': 0, 'categorias': {}})
                empleado_data[empleado_name]['total'] += alumnos
                empleado_data[empleado_name]['categorias'].setdefault(categoria_name, 0)
                empleado_data[empleado_name]['categorias'][categoria_name] += alumnos

            sorted_empleados = sorted(empleado_data.items(), key=lambda x: x[1]['total'], reverse=True)

            bloques = ["<h3>📊 Resumen Semanal de Captación por Comercial:</h3><ul>"]
            for empleado_name, data in sorted_empleados:
                bloques.append(f"<li><strong>{empleado_name}</strong>: {data['total']} alumnos<ul>")
                for categoria, cantidad in data['categorias'].items():
                    bloques.append(f"<li>{categoria}: {cantidad} alumnos</li>")
                bloques.append("</ul></li>")
            bloques.append("</ul>")
            bloques.append(f"<p><strong>Total de la semana:</strong> {total_alumnos_semana} alumnos captados</p>")

            cuerpo = f"""
                <html>
                    <body>
                        <p>📅 <strong>Informe Semanal de Captación de Alumnos - Semana del {lunes.strftime('%d/%m/%Y')} al {viernes.strftime('%d/%m/%Y')}</strong></p>
                        {''.join(bloques)}
                        <hr>
                        <p><em>Este es un informe automático del sistema de gestión comercial.</em></p>
                    </body>
                </html>
            """

            self.env['mail.mail'].create({
                'subject': f'📊 Informe Semanal de Captación - Semana del {lunes.strftime("%d/%m/%Y")} al {viernes.strftime("%d/%m/%Y")}',
                'body_html': cuerpo.strip(),
                'email_from': self.env.user.email,
                'email_to': ','.join(employees.mapped('work_email')),
            }).send()

            _logger.info(f"Informe semanal de captación enviado para la semana {lunes} - {viernes}")

        except Exception as e:
            _logger.error(f"Error al enviar informe semanal de captación: {str(e)}")

    @api.model
    def enviar_informe_mensual_captacion(self):
        """Envía un informe mensual de captación de alumnos por comercial"""
        try:
            hoy = fields.Date.today()
            primer_dia_mes_anterior = (hoy.replace(day=1) - timedelta(days=1)).replace(day=1)
            ultimo_dia_mes_anterior = hoy.replace(day=1) - timedelta(days=1)

            captaciones_mes = self.sudo().search([
                ('fecha', '>=', primer_dia_mes_anterior),
                ('fecha', '<=', ultimo_dia_mes_anterior)
            ])
            if not captaciones_mes:
                _logger.info(f"No hay captaciones para el mes {primer_dia_mes_anterior.strftime('%m/%Y')}")
                return

            employees = self._get_group_employees()
            if not employees:
                _logger.warning("No hay empleados de grupo jefa comercial o coordinación con email")
                return

            empleado_data = {}
            total_alumnos_mes = 0
            categoria_totals = {}

            for captacion in captaciones_mes:
                empleado_name = captacion.empleado_id.name
                categoria_name = captacion.categoria_id.nombre
                alumnos = captacion.numero_alumnos
                total_alumnos_mes += alumnos

                categoria_totals[categoria_name] = categoria_totals.get(categoria_name, 0) + alumnos
                empleado_data.setdefault(empleado_name, {'total': 0, 'categorias': {}})
                empleado_data[empleado_name]['total'] += alumnos
                empleado_data[empleado_name]['categorias'].setdefault(categoria_name, 0)
                empleado_data[empleado_name]['categorias'][categoria_name] += alumnos

            sorted_empleados = sorted(empleado_data.items(), key=lambda x: x[1]['total'], reverse=True)
            sorted_categorias = sorted(categoria_totals.items(), key=lambda x: x[1], reverse=True)

            bloques = ["<h3>📊 Resumen Mensual de Captación por Comercial:</h3><ul>"]
            for empleado_name, data in sorted_empleados:
                bloques.append(f"<li><strong>{empleado_name}</strong>: {data['total']} alumnos<ul>")
                for categoria, cantidad in data['categorias'].items():
                    bloques.append(f"<li>{categoria}: {cantidad} alumnos</li>")
                bloques.append("</ul></li>")
            bloques.append("</ul>")

            bloques.append("<h3>📈 Resumen por Categorías:</h3><ul>")
            for categoria, total in sorted_categorias:
                porcentaje = (total / total_alumnos_mes * 100) if total_alumnos_mes else 0
                bloques.append(f"<li><strong>{categoria}</strong>: {total} alumnos ({porcentaje:.1f}%)</li>")
            bloques.append("</ul>")
            bloques.append(f"<p><strong>Total del mes:</strong> {total_alumnos_mes} alumnos captados</p>")

            cuerpo = f"""
                <html>
                    <body>
                        <p>📅 <strong>Informe Mensual de Captación de Alumnos - {primer_dia_mes_anterior.strftime('%B %Y')}</strong></p>
                        {''.join(bloques)}
                        <hr>
                        <p><em>Este es un informe automático del sistema de gestión comercial.</em></p>
                    </body>
                </html>
            """

            self.env['mail.mail'].create({
                'subject': f'📊 Informe Mensual de Captación - {primer_dia_mes_anterior.strftime("%B %Y")}',
                'body_html': cuerpo.strip(),
                'email_from': self.env.user.email,
                'email_to': ','.join(employees.mapped('work_email')),
            }).send()

            _logger.info(f"Informe mensual de captación enviado para {primer_dia_mes_anterior.strftime('%B %Y')}")

        except Exception as e:
            _logger.error(f"Error al enviar informe mensual de captación: {str(e)}")