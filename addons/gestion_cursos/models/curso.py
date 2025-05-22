from odoo import models, fields, api # type: ignore

class Curso(models.Model):
    _name = 'gestion_cursos.curso'
    _description = 'gestion_cursos.curso'
    _rec_name = 'nombre'

    nombre = fields.Char(string = 'Nombre')
    descripcion = fields.Text(string = 'Descripción')
    codigo = fields.Char(string = 'Código')
    duracion = fields.Integer(string = 'Duración')
    modalidad = fields.Selection([
        ('presencial', 'Presencial'),
        ('semipresencial', 'Semipresencial'),
        ('teleformación', 'Teleformación')], string = 'Modalidad')
    numero_alumnos = fields.Integer(string = 'Número de alumnos')
    numero_alumnos_consolidacion = fields.Integer(string = 'Número de alumnos consolidación')
    fecha_inicio = fields.Date(string='Fecha Inicio')
    fecha_fin = fields.Date(string='Fecha Fin')
    fecha_consolidacion = fields.Date(string='Fecha de consolidación')
    id_categoria = fields.Many2one('gestion_cursos.categoria', string='Categoría')
    id_familia_profesional = fields.Many2one('gestion_cursos.familia_profesional', string='Familia profesional')
    color_categoria = fields.Selection(
        related='id_categoria.color',
        string='Color de categoría',
        store=False
    )

    @api.model_create_multi
    def create(self, vals_list):
        cursos = super().create(vals_list)
        for curso in cursos:
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
                        <li><strong>Localización:</strong> {getattr(curso, 'localizacion', '')}</li>
                        <li><strong>Unidades didácticas:</strong> {getattr(curso, 'unidades_didacticas', '')}</li>
                        <li><strong>Duración:</strong> {curso.duracion}h</li>
                        <li><strong>Nivel:</strong> {getattr(curso, 'nivel', '')}</li>
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
            employees = self.env['hr.employee'].search([])
            mail_template = {
                'subject': f'Curso eliminado: {curso.nombre}',
                'body_html': f'''
                    <p>Se ha eliminado el siguiente curso del calendario:</p>
                    <ul>
                        <li><strong>Nombre:</strong> {curso.nombre}</li>
                        <li><strong>Descripción:</strong> {curso.descripcion}</li>
                        <li><strong>Categoría:</strong> {curso.id_categoria.nombre}</li>
                        <li><strong>Fecha inicio:</strong> {curso.fecha_inicio}</li>
                        <li><strong>Fecha fin:</strong> {curso.fecha_fin}</li>
                    </ul>
                ''',
                'email_from': self.env.user.email,
                'email_to': ','.join(employees.mapped('work_email')),
            }
            self.env['mail.mail'].create(mail_template).send()
        return super().unlink()