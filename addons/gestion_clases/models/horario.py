from odoo import models, fields, api # type: ignore
from odoo.exceptions import ValidationError # type: ignore
from datetime import datetime

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
    hora_inicio_datetime = fields.Datetime(compute='_compute_hora_datetime', store=True)
    hora_fin_datetime = fields.Datetime(compute='_compute_hora_datetime', store=True)

    @api.depends('hora_inicio', 'hora_fin')
    def _compute_hora_datetime(self):
        fecha_base = datetime(2000, 1, 1)
        for record in self:
            horas_i = int(record.hora_inicio)
            minutos_i = int(round((record.hora_inicio - horas_i) * 60))
            record.hora_inicio_datetime = fecha_base.replace(hour=horas_i, minute=minutos_i, second=0)
            horas_f = int(record.hora_fin)
            minutos_f = int(round((record.hora_fin - horas_f) * 60))
            record.hora_fin_datetime = fecha_base.replace(hour=horas_f, minute=minutos_f, second=0)

    @api.constrains('hora_inicio', 'hora_fin')
    def _check_horas(self):
        for record in self:
            if record.hora_inicio >= record.hora_fin:
                raise ValidationError('La hora de inicio debe ser anterior a la de fin')
