from xml.dom import ValidationErr
from odoo import models, fields, api # type: ignore

class Horario(models.Model):
    _name = 'gestion_cursos.horario'
    _description = 'gestion_cursos.horario'
    _rec_name = 'dia'

    curso_id = fields.Many2one('gestion_cursos.curso', string='Curso', required=True)
    aula_id = fields.Many2one('gestion_cursos.aula', string='Aula')
    dia = fields.Selection([
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
    ], string='Día', required=True)
    hora_inicio = fields.Float(string='Hora inicio', required=True)
    hora_fin = fields.Float(string='Hora fin', required=True)

    @api.constrains('aula_id', 'dia', 'hora_inicio', 'hora_fin')
    def _check_aula_horario(self):
        for record in self:
            if record.aula_id:
                solapados = self.search([
                    ('id', '!=', record.id),
                    ('aula_id', '=', record.aula_id.id),
                    ('dia', '=', record.dia),
                    ('hora_inicio', '<', record.hora_fin),
                    ('hora_fin', '>', record.hora_inicio),
                ])
                if solapados:
                    raise ValidationErr('El aula ya está ocupada en ese horario.')