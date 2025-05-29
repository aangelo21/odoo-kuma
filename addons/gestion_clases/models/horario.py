from odoo import models, fields, api # type: ignore
from odoo.exceptions import ValidationError # type: ignore
from datetime import datetime, timedelta

class Horario(models.Model):
    _name = 'gestion_clases.horario'
    _description = 'Horario de Clases'
    _rec_name = 'curso_id'

    curso_id = fields.Many2one('gestion_cursos.curso', string='Curso', required=True)
    aula_id = fields.Many2one('gestion_clases.aula', string='Aula')
    lunes = fields.Boolean(string='Lunes')
    martes = fields.Boolean(string='Martes')
    miercoles = fields.Boolean(string='Miércoles')
    jueves = fields.Boolean(string='Jueves')
    viernes = fields.Boolean(string='Viernes')
    hora_inicio = fields.Float(string='Hora inicio', required=True)
    hora_fin = fields.Float(string='Hora fin', required=True)
    fecha_inicio = fields.Datetime(compute='_compute_fechas', store=True)
    fecha_fin = fields.Datetime(compute='_compute_fechas', store=True)

    @api.depends('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'hora_inicio', 'hora_fin')
    def _compute_fechas(self):
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        for record in self:
            base_date = start_of_week
            dates = []
            if record.lunes:
                dates.append(base_date + timedelta(days=0))
            if record.martes:
                dates.append(base_date + timedelta(days=1))
            if record.miercoles:
                dates.append(base_date + timedelta(days=2))
            if record.jueves:
                dates.append(base_date + timedelta(days=3))
            if record.viernes:
                dates.append(base_date + timedelta(days=4))
            
            if dates:
                date = dates[0]
                hora_i = int(record.hora_inicio)
                minutos_i = int((record.hora_inicio - hora_i) * 60)
                record.fecha_inicio = datetime(date.year, date.month, date.day, hora_i, minutos_i)
                
                hora_f = int(record.hora_fin)
                minutos_f = int((record.hora_fin - hora_f) * 60)
                record.fecha_fin = datetime(date.year, date.month, date.day, hora_f, minutos_f)
            else:
                record.fecha_inicio = False
                record.fecha_fin = False

    @api.constrains('hora_inicio', 'hora_fin')
    def _check_horas(self):
        for record in self:
            if record.hora_inicio >= record.hora_fin:
                raise ValidationError('La hora de inicio debe ser anterior a la de fin')
