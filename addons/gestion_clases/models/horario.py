from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import pytz

class Horario(models.Model):
    _name = 'gestion_clases.horario'
    _description = 'Horario de Clases'
    _rec_name = 'curso_id'

    curso_id = fields.Many2one('gestion_cursos.curso', string='Curso', required=True)
    aula_id = fields.Many2one('gestion_clases.aula', string='Aula')
    fecha = fields.Datetime(string='Fecha del evento')
    fecha_fin = fields.Datetime(string='Fecha y hora de fin del evento')
    es_plantilla = fields.Boolean(string='Es plantilla', default=True)
    plantilla_id = fields.Many2one('gestion_clases.horario', string='Horario plantilla')
    temario = fields.Text(string='Temario', help='Contenido impartido en la clase')
    color_event = fields.Char(string='Color del evento', compute='_compute_color_event', store=True)

    lunes = fields.Boolean(string='Lunes')
    lunes_hora_inicio = fields.Float(string='Hora inicio lunes')
    lunes_hora_fin = fields.Float(string='Hora fin lunes')

    martes = fields.Boolean(string='Martes')
    martes_hora_inicio = fields.Float(string='Hora inicio martes')
    martes_hora_fin = fields.Float(string='Hora fin martes')

    miercoles = fields.Boolean(string='Miércoles')
    miercoles_hora_inicio = fields.Float(string='Hora inicio miércoles')
    miercoles_hora_fin = fields.Float(string='Hora fin miércoles')

    jueves = fields.Boolean(string='Jueves')
    jueves_hora_inicio = fields.Float(string='Hora inicio jueves')
    jueves_hora_fin = fields.Float(string='Hora fin jueves')

    viernes = fields.Boolean(string='Viernes')
    viernes_hora_inicio = fields.Float(string='Hora inicio viernes')
    viernes_hora_fin = fields.Float(string='Hora fin viernes')

    @api.depends('temario')
    def _compute_color_event(self):
        for record in self:
            record.color_event = '#55eb18' if record.temario else '#f91212'

    @api.constrains('lunes', 'lunes_hora_inicio', 'lunes_hora_fin',
                    'martes', 'martes_hora_inicio', 'martes_hora_fin',
                    'miercoles', 'miercoles_hora_inicio', 'miercoles_hora_fin',
                    'jueves', 'jueves_hora_inicio', 'jueves_hora_fin',
                    'viernes', 'viernes_hora_inicio', 'viernes_hora_fin')
    def _check_horas(self):
        for record in self:
            if record.lunes and record.lunes_hora_inicio >= record.lunes_hora_fin:
                raise ValidationError('La hora de inicio del lunes debe ser anterior a la hora de fin')
            if record.martes and record.martes_hora_inicio >= record.martes_hora_fin:
                raise ValidationError('La hora de inicio del martes debe ser anterior a la hora de fin')
            if record.miercoles and record.miercoles_hora_inicio >= record.miercoles_hora_fin:
                raise ValidationError('La hora de inicio del miércoles debe ser anterior a la hora de fin')
            if record.jueves and record.jueves_hora_inicio >= record.jueves_hora_fin:
                raise ValidationError('La hora de inicio del jueves debe ser anterior a la hora de fin')
            if record.viernes and record.viernes_hora_inicio >= record.viernes_hora_fin:
                raise ValidationError('La hora de inicio del viernes debe ser anterior a la hora de fin')

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
            dia_semana = fecha_actual.weekday()
            hora_inicio = hora_fin = False
            
            if dia_semana == 0 and self.lunes:
                hora_inicio = self.lunes_hora_inicio
                hora_fin = self.lunes_hora_fin
            elif dia_semana == 1 and self.martes:
                hora_inicio = self.martes_hora_inicio
                hora_fin = self.martes_hora_fin
            elif dia_semana == 2 and self.miercoles:
                hora_inicio = self.miercoles_hora_inicio
                hora_fin = self.miercoles_hora_fin
            elif dia_semana == 3 and self.jueves:
                hora_inicio = self.jueves_hora_inicio
                hora_fin = self.jueves_hora_fin
            elif dia_semana == 4 and self.viernes:
                hora_inicio = self.viernes_hora_inicio
                hora_fin = self.viernes_hora_fin

            if hora_inicio and hora_fin:
                hora_i = int(hora_inicio)
                min_i = int((hora_inicio - hora_i) * 60)
                fecha_inicio = datetime.combine(fecha_actual, datetime.min.time())
                fecha_inicio = fecha_inicio.replace(hour=hora_i, minute=min_i)
                
                local_dt = tz.localize(fecha_inicio)
                fecha_inicio_utc = local_dt.astimezone(pytz.UTC).replace(tzinfo=None)
                
                hora_f = int(hora_fin)
                min_f = int((hora_fin - hora_f) * 60)
                fecha_fin = datetime.combine(fecha_actual, datetime.min.time())
                fecha_fin = fecha_fin.replace(hour=hora_f, minute=min_f)
                
                local_dt_fin = tz.localize(fecha_fin)
                fecha_fin_utc = local_dt_fin.astimezone(pytz.UTC).replace(tzinfo=None)

                self.env['gestion_clases.horario'].create({
                    'curso_id': self.curso_id.id,
                    'aula_id': self.aula_id.id,
                    'fecha': fecha_inicio_utc,
                    'fecha_fin': fecha_fin_utc,
                    'es_plantilla': False,
                    'plantilla_id': self.id,
                })
            fecha_actual += timedelta(days=1)

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.es_plantilla:
            record._generar_eventos()
        return record

    def write(self, vals):
        result = super().write(vals)
        if self.es_plantilla:
            self._generar_eventos()
        return result

    @api.constrains('aula_id', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes',
                    'lunes_hora_inicio', 'lunes_hora_fin',
                    'martes_hora_inicio', 'martes_hora_fin',
                    'miercoles_hora_inicio', 'miercoles_hora_fin',
                    'jueves_hora_inicio', 'jueves_hora_fin',
                    'viernes_hora_inicio', 'viernes_hora_fin')
    def _check_solapamiento(self):
        for record in self:
            if not record.aula_id:
                continue

            domain = [
                ('id', '!=', record.id),
                ('aula_id', '=', record.aula_id.id),
            ]

            if record.es_plantilla:
                domain.append(('es_plantilla', '=', True))
                
                dias = []
                horas = {}
                
                if record.lunes:
                    dias.append(('lunes', '=', True))
                    horas['lunes'] = (record.lunes_hora_inicio, record.lunes_hora_fin)
                if record.martes:
                    dias.append(('martes', '=', True))
                    horas['martes'] = (record.martes_hora_inicio, record.martes_hora_fin)
                if record.miercoles:
                    dias.append(('miercoles', '=', True))
                    horas['miercoles'] = (record.miercoles_hora_inicio, record.miercoles_hora_fin)
                if record.jueves:
                    dias.append(('jueves', '=', True))
                    horas['jueves'] = (record.jueves_hora_inicio, record.jueves_hora_fin)
                if record.viernes:
                    dias.append(('viernes', '=', True))
                    horas['viernes'] = (record.viernes_hora_inicio, record.viernes_hora_fin)

                if dias:
                    if len(dias) > 1:
                        domain.extend(['|'] * (len(dias) - 1))
                    domain.extend(dias)

                otros_horarios = self.search(domain)
                
                for otro in otros_horarios:
                    if (otro.curso_id.fecha_fin >= record.curso_id.fecha_inicio and 
                        otro.curso_id.fecha_inicio <= record.curso_id.fecha_fin):
                        
                        for dia, (hora_inicio, hora_fin) in horas.items():
                            otro_hora_inicio = getattr(otro, f'{dia}_hora_inicio')
                            otro_hora_fin = getattr(otro, f'{dia}_hora_fin')
                            
                            if getattr(otro, dia) and (
                                (hora_inicio < otro_hora_fin and hora_fin > otro_hora_inicio)
                            ):
                                raise ValidationError(
                                    f'Ya existe una plantilla de horario que usa esta aula el {dia} '
                                    f'en el horario seleccionado durante las fechas del curso'
                                )
            else:
                domain.append(('es_plantilla', '=', False))
                if record.fecha and record.fecha_fin:
                    domain.extend([
                        ('fecha', '<', record.fecha_fin),
                        ('fecha_fin', '>', record.fecha)
                    ])

                if self.search_count(domain) > 0:
                    raise ValidationError('El aula ya está ocupada en la fecha y horario seleccionados')

    def unlink(self):
        for record in self:
            if record.es_plantilla:
                self.env['gestion_clases.horario'].search([
                    ('plantilla_id', '=', record.id),
                    ('es_plantilla', '=', False)
                ]).unlink()
        return super().unlink()
