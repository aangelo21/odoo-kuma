from odoo import models, fields, api # type: ignore

class Categoria(models.Model):
    _name = 'gestion_cursos.categoria'
    _description = 'gestion_cursos.categoria'
    _rec_name = 'nombre'

    nombre = fields.Char(string = 'Nombre')
    descripcion = fields.Text(string = 'Descripción')
    color = fields.Selection([
        ('0', 'Rojo'),
        ('1', 'Azul'),
        ('8', 'Gris')], string='Color para el evento del calendario')
    id_curso = fields.One2many('gestion_cursos.curso', 'id_categoria', string='Cursos')