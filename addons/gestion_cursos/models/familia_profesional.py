from odoo import models, fields, api # type: ignore

class FamiliaProfesional(models.Model):
    _name = 'gestion_cursos.familia_profesional'
    _description = 'gestion_cursos.familia_profesional'

    nombre = fields.Text(string = 'Nombre')
    descripcion = fields.Text(string = 'Descripción')
    id_curso = fields.One2many('gestion_cursos.curso', 'id_familia_profesional', string='Cursos')