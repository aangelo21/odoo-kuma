from odoo import models, fields, api # type: ignore

class Aula(models.Model):
    _name = 'gestion_clases.aula'
    _description = 'gestion_clases.aula'
    _rec_name = 'nombre'

    nombre = fields.Char(string = 'Nombre')
    centro = fields.Char(string = 'Centro')