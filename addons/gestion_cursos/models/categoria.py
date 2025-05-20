from odoo import models, fields, api # type: ignore

class Categoria(models.Model):
    _name = 'gestion_cursos.categoria'
    _description = 'gestion_cursos.categoria'

    nombre = fields.Text(string = 'Nombre')
    descripcion = fields.Text(string = 'Descripción')