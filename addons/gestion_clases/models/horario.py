from odoo import models, fields, api # type: ignore
from odoo.exceptions import ValidationError # type: ignore
from datetime import datetime, timedelta
import pytz # type: ignore

class Horario(models.Model):
    _name = 'gestion_clases.horario'
    _description = 'Horario de Clases'
    _rec_name = 'curso_id'

    curso_id = fields.Many2one('gestion_cursos.curso', string='Curso', required=True)
    aula_id = fields.Many2one('gestion_clases.aula', string='Aula')
    hora_inicio = fields.Float(string='Hora inicio', required=True)
    hora_fin = fields.Float(string='Hora fin', required=True)
    fecha = fields.Datetime(string='Fecha del evento')
    es_plantilla = fields.Boolean(string='Es plantilla', default=True)
    plantilla_id = fields.Many2one('gestion_clases.horario', string='Horario plantilla')
    
    fecha_inicio = fields.Datetime(string='Fecha y hora de inicio')
    fecha_fin = fields.Datetime(string='Fecha y hora de fin del evento')  
    
    lunes = fields.Boolean(string='Lunes')
    martes = fields.Boolean(string='Martes')
    miercoles = fields.Boolean(string='Miércoles')
    jueves = fields.Boolean(string='Jueves')
    viernes = fields.Boolean(string='Viernes')

    @api.model
    def create(self, vals):
        if vals.get('es_plantilla'):
            horario = super().create(vals)
            horario._generar_eventos()
            return horario
        return super().create(vals)

    def _generar_eventos(self):
        self.ensure_one()
        if not self.es_plantilla:
            return

        self.env['gestion_clases.horario'].search([
            ('plantilla_id', '=', self.id),
            ('es_plantilla', '=', False)
        ]).unlink()

        tz = pytz.timezone(self.env.user.tz or 'UTC')
        
        fecha_actual = self.curso_id.fecha_inicio
        while fecha_actual <= self.curso_id.fecha_fin:
            if ((fecha_actual.weekday() == 0 and self.lunes) or
                (fecha_actual.weekday() == 1 and self.martes) or
                (fecha_actual.weekday() == 2 and self.miercoles) or
                (fecha_actual.weekday() == 3 and self.jueves) or
                (fecha_actual.weekday() == 4 and self.viernes)):
                
                hora_i = int(self.hora_inicio)
                min_i = int((self.hora_inicio - hora_i) * 60)
                fecha_inicio = datetime.combine(fecha_actual, datetime.min.time())
                fecha_inicio = fecha_inicio.replace(hour=hora_i, minute=min_i)
                
                local_dt = tz.localize(fecha_inicio)
                fecha_inicio_utc = local_dt.astimezone(pytz.UTC).replace(tzinfo=None)
                
                hora_f = int(self.hora_fin)
                min_f = int((self.hora_fin - hora_f) * 60)
                fecha_fin = datetime.combine(fecha_actual, datetime.min.time())
                fecha_fin = fecha_fin.replace(hour=hora_f, minute=min_f)
                
                local_dt_fin = tz.localize(fecha_fin)
                fecha_fin_utc = local_dt_fin.astimezone(pytz.UTC).replace(tzinfo=None)

                self.env['gestion_clases.horario'].create({
                    'curso_id': self.curso_id.id,
                    'aula_id': self.aula_id.id,
                    'hora_inicio': self.hora_inicio,
                    'hora_fin': self.hora_fin,
                    'fecha': fecha_inicio_utc,
                    'fecha_fin': fecha_fin_utc,
                    'es_plantilla': False,
                    'plantilla_id': self.id,
                })
            fecha_actual += timedelta(days=1)

    @api.constrains('hora_inicio', 'hora_fin')
    def _check_horas(self):
        for record in self:
            if record.hora_inicio >= record.hora_fin:
                raise ValidationError('La hora de inicio debe ser anterior a la de fin')

    def write(self, vals):
        res = super().write(vals)
        if self.es_plantilla:
            if any(field in vals for field in ['hora_inicio', 'hora_fin', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes']):
                self._generar_eventos()
        return res

    def unlink(self):
        for record in self:
            if record.es_plantilla:
                self.env['gestion_clases.horario'].search([
                    ('plantilla_id', '=', record.id),
                    ('es_plantilla', '=', False)
                ]).unlink()
        return super().unlink()

    @api.constrains('aula_id', 'fecha', 'fecha_fin', 'es_plantilla')
    def _check_solapamiento(self):
        for record in self:
            if record.es_plantilla:
                return

            if not record.aula_id or not record.fecha or not record.fecha_fin:
                return

            # Buscar horarios que se solapen
            horarios_solapados = self.env['gestion_clases.horario'].search([
                ('id', '!=', record.id),
                ('aula_id', '=', record.aula_id.id),
                ('es_plantilla', '=', False),
                '|',
                '&',
                ('fecha', '<=', record.fecha),
                ('fecha_fin', '>', record.fecha),
                '&',
                ('fecha', '<', record.fecha_fin),
                ('fecha_fin', '>=', record.fecha_fin)
            ])

            if horarios_solapados:
                raise ValidationError(
                    f'Hay un solapamiento de horarios en el aula {record.aula_id.nombre}:\n' +
                    '\n'.join([
                        f'- Curso: {h.curso_id.nombre}, ' +
                        f'Fecha: {h.fecha.strftime("%d/%m/%Y")}, ' +
                        f'Hora: {int(h.hora_inicio)}:{int((h.hora_inicio % 1) * 60):02d} - ' +
                        f'{int(h.hora_fin)}:{int((h.hora_fin % 1) * 60):02d}'
                        for h in horarios_solapados
                    ])
                )
