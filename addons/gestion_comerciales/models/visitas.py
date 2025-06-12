from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Visitas(models.Model):
    _name = 'gestion_comerciales.visitas'
    _description = 'Gestión de Visitas y Llamadas Comerciales'
    _rec_name = 'display_name'

    empleado_id = fields.Many2one(
        'hr.employee',
        string='Trabajador',
        required=True,
        help='Empleado que realizó la visita o llamada'
    )
    
    fecha = fields.Date(
        string='Fecha',
        default=fields.Date.today,
        required=True,
        help='Fecha de la visita o llamada'
    )
    
    nombre = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre del contacto'
    )
    
    dni_empresa = fields.Text(
        string='DNI/Empresa',
        required=True,
        help='DNI del particular o nombre de la empresa'
    )
    
    telefono = fields.Char(
        string='Teléfono',
        required=True,
        help='Número de teléfono de contacto'
    )
    
    mail = fields.Char(
        string='Email',
        required=True,
        help='Correo electrónico de contacto'
    )
    
    tipo_contacto = fields.Selection(
        [
            ('visita', 'Visita'),
            ('llamada', 'Llamada')
        ],
        string='Visita/Llamada',
        required=True,
        default='visita',
        help='Tipo de contacto realizado'
    )
    
    plan_id = fields.Many2one(
        'gestion_cursos.categoria',
        string='Plan',
        required=True,
        help='Categoría/Plan del curso'
    )
    
    confirmado = fields.Boolean(
        string='Confirmado',
        default=False,
        help='Indica si el contacto está confirmado'
    )
    
    observaciones = fields.Text(
        string='Observaciones',
        help='Observaciones adicionales sobre la visita o llamada'
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
        help='Mes de la fecha de contacto'
    )

    año = fields.Integer(
        string='Año',
        compute='_compute_fecha_parts',
        store=True,
        help='Año de la fecha de contacto'
    )
    
    mes_año = fields.Char(
        string='Mes/Año',
        compute='_compute_fecha_parts',
        store=True,
        help='Mes y año de la fecha de contacto'
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
    
    @api.depends('empleado_id', 'nombre', 'tipo_contacto', 'fecha', 'confirmado')
    def _compute_display_name(self):
        for record in self:
            if record.empleado_id and record.nombre:
                fecha_str = record.fecha.strftime('%d/%m/%Y') if record.fecha else ''
                tipo_str = dict(record._fields['tipo_contacto'].selection).get(record.tipo_contacto, '')
                confirmado_str = ' ✓' if record.confirmado else ''
                record.display_name = f"{record.empleado_id.name} - {record.nombre} ({tipo_str}) - {fecha_str}{confirmado_str}"
            else:
                record.display_name = "Visita/Llamada"
