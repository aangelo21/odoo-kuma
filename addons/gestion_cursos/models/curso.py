from odoo import models, fields, api # type: ignore

class Curso(models.Model):
    _name = 'gestion_cursos.curso'
    _description = 'gestion_cursos.curso'
    _rec_name = 'nombre'

    nombre = fields.Text(string = 'Nombre')
    descripcion = fields.Text(string = 'Descripción')
    nivel = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')], string = 'Nivel')
    duracion = fields.Integer(string = 'Duración')
    modalidad = fields.Selection([
        ('presencial', 'Presencial'),
        ('semipresencial', 'Semipresencial'),
        ('teleformación', 'Teleformación')], string = 'Modalidad')
    localizacion = fields.Selection([
    ('nacional', 'Nacional'),
    ('teleformacion', 'Teleformación'),
    ('gran_canaria', 'Gran Canaria'),
    ('tenerife', 'Tenerife'),
    ('lanzarote', 'Lanzarote'),
    ('fuerteventura', 'Fuerteventura'),
    ('la_palma', 'La Palma'),
    ('la_gomera', 'La Gomera'),
    ('el_hierro', 'El Hierro')], string='Localización')
    unidades_didacticas = fields.Integer(string = 'Unidades didácticas')
    fecha_inicio = fields.Date(string='Fecha Inicio')
    fecha_fin = fields.Date(string='Fecha Fin')
    id_categoria = fields.Many2one('gestion_cursos.categoria', string='Categoría')
    id_familia_profesional = fields.Many2one('gestion_cursos.familia_profesional', string='Familia Profesional')