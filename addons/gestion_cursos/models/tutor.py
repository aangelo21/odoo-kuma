from odoo import models, fields, api # type: ignore

class FamiliaProfesional(models.Model):
    _name = 'gestion_cursos.tutor'
    _description = 'gestion_cursos.tutor'
    _rec_name = 'nombre'

    nombre = fields.Char(string = 'Nombre')
    id_curso = fields.One2many('gestion_cursos.curso', 'id_tutor', string='Cursos')