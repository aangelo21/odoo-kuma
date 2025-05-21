from odoo import models, fields, api # type: ignore

class Curso(models.Model):
    _name = 'gestion_cursos.curso'
    _description = 'gestion_cursos.curso'
    _rec_name = 'nombre'

    nombre = fields.Char(string = 'Nombre')
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
    id_familia_profesional = fields.Many2one('gestion_cursos.familia_profesional', string='Familia profesional')
    id_evento_calendario = fields.Many2one('calendar.event', string='Evento del calendario', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        cursos = super().create(vals_list)
        for curso in cursos:
            calendar_event = self.env['calendar.event'].create({
                'name': curso.nombre,
                'description': curso.descripcion,
                'start': curso.fecha_inicio,
                'stop': curso.fecha_fin or curso.fecha_inicio,
                'user_id': self.env.user.id,
                'allday': True,
            })
            curso.id_evento_calendario = calendar_event
        return cursos

    def write(self, vals):
        result = super().write(vals)
        for curso in self:
            if curso.id_evento_calendario:
                curso.id_evento_calendario.write({
                    'name': curso.id_categoria.nombre + ' - ' + curso.nombre,
                    'description': curso.descripcion,
                    'start': curso.fecha_inicio,
                    'stop': curso.fecha_fin or curso.fecha_inicio,
                    'allday': True,
                })
        return result

    def unlink(self):
        for curso in self:
            if curso.id_evento_calendario:
                curso.id_evento_calendario.unlink()
        return super().unlink()