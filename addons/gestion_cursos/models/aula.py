from odoo import models, fields, api # type: ignore

class Aula(models.Model):
    _name = 'gestion_cursos.aula'
    _description = 'gestion_cursos.aula'
    _rec_name = 'nombre'

    nombre = fields.Char(string = 'Nombre')
    centro = fields.Char(string = 'Centro')