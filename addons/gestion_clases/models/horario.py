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
    
    @api.constrains('hora_inicio', 'hora_fin')
    def _check_horas(self):
        for record in self:
            if record.hora_inicio < 0 or record.hora_inicio >= 24:
                raise ValidationError('La hora de inicio debe estar entre 0 y 24')
            if record.hora_fin < 0 or record.hora_fin >= 24:
                raise ValidationError('La hora de fin debe estar entre 0 y 24')
            if record.hora_inicio >= record.hora_fin:
                raise ValidationError('La hora de inicio debe ser anterior a la hora de fin')

    @api.constrains('aula_id', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'hora_inicio', 'hora_fin')
    def _check_aula_horario(self):
        for record in self:
            if record.es_plantilla:
                dias_seleccionados = []
                if record.lunes:
                    dias_seleccionados.append(('lunes', '=', True))
                if record.martes:
                    dias_seleccionados.append(('martes', '=', True))
                if record.miercoles:
                    dias_seleccionados.append(('miercoles', '=', True))
                if record.jueves:
                    dias_seleccionados.append(('jueves', '=', True))
                if record.viernes:
                    dias_seleccionados.append(('viernes', '=', True))

                if not dias_seleccionados:
                    raise ValidationError('Debe seleccionar al menos un día de la semana')

            if record.aula_id:
                domain = [
                    ('id', '!=', record.id),
                    ('aula_id', '=', record.aula_id.id),
                ]

                if record.es_plantilla:
                    domain.append(('es_plantilla', '=', True))
                    domain.append(('hora_inicio', '<', record.hora_fin))
                    domain.append(('hora_fin', '>', record.hora_inicio))
                    
                    if len(dias_seleccionados) > 1:
                        domain.extend(['|'] * (len(dias_seleccionados) - 1))
                    domain.extend(dias_seleccionados)
                else:
                    domain.append(('es_plantilla', '=', False))
                    if record.fecha and record.fecha_fin:
                        domain.extend([
                            ('fecha', '<', record.fecha_fin),
                            ('fecha_fin', '>', record.fecha)
                        ])

                solapados = self.search(domain)
                if solapados:
                    if record.es_plantilla:
                        raise ValidationError('Ya existe una plantilla de horario que usa esta aula en alguno de los días y horarios seleccionados')
                    else:
                        raise ValidationError('El aula ya está ocupada en la fecha y horario seleccionados')
