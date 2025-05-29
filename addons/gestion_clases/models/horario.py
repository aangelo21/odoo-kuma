from odoo import models, fields, api # type: ignore
from odoo.exceptions import ValidationError # type: ignore

class Horario(models.Model):
    _name = 'gestion_clases.horario'
    _description = 'gestion_clases.horario'
    _rec_name = 'curso_id'

    curso_id = fields.Many2one('gestion_cursos.curso', string='Curso', required=True)
    aula_id = fields.Many2one('gestion_clases.aula', string='Aula')
    lunes = fields.Boolean(string='Lunes')
    martes = fields.Boolean(string='Martes')
    miercoles = fields.Boolean(string='Miércoles')
    jueves = fields.Boolean(string='Jueves')
    viernes = fields.Boolean(string='Viernes')
    hora_inicio = fields.Float(string='Hora inicio', required=True, help='Format: 24h (e.g., 13.5 = 13:30)')
    hora_fin = fields.Float(string='Hora fin', required=True, help='Format: 24h (e.g., 15.0 = 15:00)')

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
            if record.aula_id:
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

                domain = [
                    ('id', '!=', record.id),
                    ('aula_id', '=', record.aula_id.id),
                    ('hora_inicio', '<', record.hora_fin),
                    ('hora_fin', '>', record.hora_inicio),
                ]

                if len(dias_seleccionados) > 1:
                    domain.extend(['|'] * (len(dias_seleccionados) - 1))
                domain.extend(dias_seleccionados)

                solapados = self.search(domain)
                if solapados:
                    raise ValidationError('El aula ya está ocupada en alguno de los días y horarios seleccionados')