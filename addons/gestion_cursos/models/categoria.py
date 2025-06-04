from odoo import models, fields, api # type: ignore

class Categoria(models.Model):
    _name = 'gestion_cursos.categoria'
    _description = 'gestion_cursos.categoria'
    _rec_name = 'nombre'

    nombre = fields.Char(string = 'Nombre')
    color = fields.Selection([
        ("#FF0000", 'Rojo'),
        ("#0062FF", 'Azul'),
        ("#7C7C7C", 'Gris'),
        ("#4B0082", 'Índigo')
    ], string='Color para el evento del calendario')
    id_curso = fields.One2many('gestion_cursos.curso', 'id_categoria', string='Cursos')