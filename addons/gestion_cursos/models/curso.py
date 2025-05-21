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
    
        employees = self.env['hr.employee'].search([])
        
        mail_template = {
            'subject': f'Nuevo curso añadido al calendario: {curso.nombre}',
            'body_html': f'''
                <p>Se ha añadido un nuevo curso al calendario:</p>
                <ul>
                    <li><strong>Nombre:</strong> {curso.nombre}</li>
                    <li><strong>Descripción:</strong> {curso.descripcion}</li>
                    <li><strong>Categoría:</strong> {curso.id_categoria.nombre}</li>
                    <li><strong>Familia profesional:</strong> {curso.id_familia_profesional.nombre}</li>
                    <li><strong>Modalidad:</strong> {curso.modalidad}</li>
                    <li><strong>Localización:</strong> {curso.localizacion}</li>
                    <li><strong>Modalidad:</strong> {curso.modalidad}</li>
                    <li><strong>Unidades didácticas:</strong> {curso.unidades_didacticas}</li>
                    <li><strong>Duración:</strong> {curso.duracion}h</li>
                    <li><strong>Nivel:</strong> {curso.nivel}</li>
                    <li><strong>Fecha inicio:</strong> {curso.fecha_inicio}</li>
                    <li><strong>Fecha fin:</strong> {curso.fecha_fin}</li>
                </ul>
            ''',
            'email_from': self.env.user.email,
            'email_to': ','.join(employees.mapped('work_email')),
        }
        self.env['mail.mail'].create(mail_template).send()
        return cursos

    def write(self, vals):
        fecha_modificada = 'fecha_inicio' in vals or 'fecha_fin' in vals
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

            if fecha_modificada:
                employees = self.env['hr.employee'].search([])
                
                mail_template = {
                    'subject': f'Actualización de fechas en el curso: {curso.nombre}',
                    'body_html': f'''
                        <p>Se han actualizado las fechas del curso en el calendario:</p>
                        <ul>
                            <li><strong>Nombre:</strong> {curso.nombre}</li>
                            <li><strong>Nueva fecha inicio:</strong> {curso.fecha_inicio}</li>
                            <li><strong>Nueva fecha fin:</strong> {curso.fecha_fin}</li>
                        </ul>
                    ''',
                    'email_from': self.env.user.email,
                    'email_to': ','.join(employees.mapped('work_email')),
                }
                self.env['mail.mail'].create(mail_template).send()
        return result

    def unlink(self):
        for curso in self:
            if curso.id_evento_calendario:
                curso.id_evento_calendario.unlink()
        return super().unlink()