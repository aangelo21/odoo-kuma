from datetime import date, timedelta
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
    numero_alumnos_finalizados = fields.Integer(string = 'Número de alumnos finalizados')
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

    consolidados_display = fields.Char(
        string="Consolidados",
        compute="_compute_consolidados_display"
    )
    
    finalizados_display = fields.Char(
        string="Finalizados",
        compute="_compute_finalizados_display"
    )
    
    @api.depends('numero_alumnos_consolidacion', 'numero_alumnos')
    def _compute_consolidados_display(self):
        for record in self:
            consolidados = record.numero_alumnos_consolidacion or 0
            total = record.numero_alumnos or 0
            record.consolidados_display = f"{consolidados}/{total}"
    
    @api.depends('numero_alumnos_finalizados', 'numero_alumnos_consolidacion')
    def _compute_finalizados_display(self):
        for record in self:
            finalizados = record.numero_alumnos_finalizados or 0
            consolidados = record.numero_alumnos_consolidacion or 0
            record.finalizados_display = f"{finalizados}/{consolidados}"

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
                        <li><strong>Código:</strong> {curso.codigo}</li>
                        <li><strong>Categoría:</strong> {curso.id_categoria.nombre}</li>
                        <li><strong>Familia profesional:</strong> {curso.id_familia_profesional.nombre}</li>
                        <li><strong>Número de alumnos:</strong> {curso.numero_alumnos}</li>
                        <li><strong>Número de alumnos consolidados:</strong> {curso.numero_alumnos_consolidacion}</li>
                        <li><strong>Número de alumnos finalizados:</strong> {curso.numero_alumnos_finalizados}</li>
                        <li><strong>Modalidad:</strong> {curso.modalidad}</li>
                        <li><strong>Duración:</strong> {curso.duracion}h</li>
                        <li><strong>Fecha inicio:</strong> {curso.fecha_inicio}</li>
                        <li><strong>Fecha fin:</strong> {curso.fecha_fin}</li>
                        <li><strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}</li>
                    </ul>
                ''',
                'email_from': self.env.user.email,
                'email_to': ','.join(employees.mapped('work_email')),
            }
            self.env['mail.mail'].create(mail_template).send()
        return cursos

    def write(self, vals):
        result = super().write(vals)
        for curso in self:
            cambios = []

            if 'fecha_inicio' in vals:
                cambios.append(f"<li><strong>Nueva fecha inicio:</strong> {curso.fecha_inicio}</li>")
            else:
                cambios.append(f"<li><strong>Fecha inicio:</strong> {curso.fecha_inicio}</li>")
            if 'fecha_fin' in vals:
                cambios.append(f"<li><strong>Nueva fecha fin:</strong> {curso.fecha_fin}</li>")
            else:
                cambios.append(f"<li><strong>Fecha fin:</strong> {curso.fecha_fin}</li>")
            if 'fecha_consolidacion' in vals:
                cambios.append(f"<li><strong>Nueva fecha consolidación:</strong> {curso.fecha_consolidacion}</li>")
            else:
                cambios.append(f"<li><strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}</li>")
            if 'fecha_inicio' in vals or 'fecha_fin' in vals or 'fecha_consolidacion' in vals:
                employees = self.env['hr.employee'].search([])
                mail_template = {
                    'subject': f'Actualización de fechas en el curso: {curso.nombre}',
                    'body_html': f'''
                        <p>Se han actualizado las fechas del curso en el calendario:</p>
                        <ul>
                            <li><strong>Nombre:</strong> {curso.nombre}</li>
                            {''.join(cambios)}
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
                        <li><strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}</li>
                        <li><strong>Fecha fin:</strong> {curso.fecha_fin}</li>
                    </ul>
                ''',
                'email_from': self.env.user.email,
                'email_to': ','.join(employees.mapped('work_email')),
            }
            self.env['mail.mail'].create(mail_template).send()
        return super().unlink()
    
    @api.model
    def cron_aviso_fechas_dia(self):
        hoy = date.today()
        employees = self.env['hr.employee'].search([])
        cursos_inicio = self.search([('fecha_inicio', '=', hoy)])
        cursos_fin = self.search([('fecha_fin', '=', hoy)])
        cursos_consolidacion = self.search([('fecha_consolidacion', '=', hoy)])

        bloques = []

        if cursos_inicio:
            bloques.append("<h3>Cursos que inician hoy:</h3><ul>")
            for curso in cursos_inicio:
                bloques.append(f"""
                <li style="margin-bottom: 20px;">
                    <strong>Nombre:</strong> {curso.nombre}<br/>
                    <strong>Descripción:</strong> {curso.descripcion}<br/>
                    <strong>Categoría:</strong> {curso.id_categoria.nombre}<br/>
                    <strong>Fecha inicio:</strong> {curso.fecha_inicio}<br/>
                    <strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}<br/>
                    <strong>Fecha fin:</strong> {curso.fecha_fin}
                </li>
                <br>
            """)
            bloques.append("</ul>")
        if cursos_fin:
            bloques.append("<h3>Cursos que finalizan hoy:</h3><ul>")
            for curso in cursos_fin:
                bloques.append(f"""
                <li style="margin-bottom: 20px;">
                    <strong>Nombre:</strong> {curso.nombre}<br/>
                    <strong>Descripción:</strong> {curso.descripcion}<br/>
                    <strong>Categoría:</strong> {curso.id_categoria.nombre}<br/>
                    <strong>Fecha inicio:</strong> {curso.fecha_inicio}<br/>
                    <strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}<br/>
                    <strong>Fecha fin:</strong> {curso.fecha_fin}
                </li>
                <br>
            """)
            bloques.append("</ul>")
        if cursos_consolidacion:
            bloques.append("<h3>Cursos que consolidan hoy:</h3><ul>")
            for curso in cursos_consolidacion:
                bloques.append(f"""
                <li style="margin-bottom: 20px;">
                    <strong>Nombre:</strong> {curso.nombre}<br/>
                    <strong>Descripción:</strong> {curso.descripcion}<br/>
                    <strong>Categoría:</strong> {curso.id_categoria.nombre}<br/>
                    <strong>Fecha inicio:</strong> {curso.fecha_inicio}<br/>
                    <strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}<br/>
                    <strong>Fecha fin:</strong> {curso.fecha_fin}
                </li>
                <br>
            """)
            bloques.append("</ul>")

        if not bloques:
            cuerpo = f"""
                <html>
                    <body>
                        <p>No hay cursos con fechas coincidentes para hoy ({hoy}).</p>
                    </body>
                </html>
            """
        else:
            cuerpo = f"""
                <html>
                    <body>
                        <p>Resumen de cursos para hoy ({hoy}):</p>
                        {''.join(bloques)}
                    </body>
                </html>
            """
        mail_template = {
            'subject': f'Resumen diario de cursos ({hoy})',
            'body_html': cuerpo.strip(),
            'email_from': self.env.user.email,
            'email_to': ','.join(employees.mapped('work_email')),
        }
        self.env['mail.mail'].create(mail_template).send()

    @api.model
    def cron_aviso_fechas_semana(self):
        hoy = date.today()
        lunes = hoy - timedelta(days=hoy.weekday())
        viernes = lunes + timedelta(days=4)
        employees = self.env['hr.employee'].search([])

        dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

        bloques = []
        for i in range(5):  # Lunes a viernes
            dia = lunes + timedelta(days=i)
            cursos_inicio = self.search([('fecha_inicio', '=', dia)])
            cursos_fin = self.search([('fecha_fin', '=', dia)])
            cursos_consolidacion = self.search([('fecha_consolidacion', '=', dia)])

            if cursos_inicio or cursos_fin or cursos_consolidacion:
                nombre_dia = dias_es[i]
                bloques.append(f"<h3>{nombre_dia} {dia.strftime('%d/%m/%Y')}</h3>")
                if cursos_inicio:
                    bloques.append("<b>Cursos que inician este día:</b><ul>")
                    for curso in cursos_inicio:
                        bloques.append(f"""
                            <li style="margin-bottom: 10px;">
                                <strong>Nombre:</strong> {curso.nombre}<br/>
                                <strong>Descripción:</strong> {curso.descripcion}<br/>
                                <strong>Categoría:</strong> {curso.id_categoria.nombre}<br/>
                                <strong>Fecha inicio:</strong> {curso.fecha_inicio}<br/>
                                <strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}<br/>
                                <strong>Fecha fin:</strong> {curso.fecha_fin}
                            </li>
                        """)
                    bloques.append("</ul>")
                if cursos_fin:
                    bloques.append("<b>Cursos que finalizan este día:</b><ul>")
                    for curso in cursos_fin:
                        bloques.append(f"""
                            <li style="margin-bottom: 10px;">
                                <strong>Nombre:</strong> {curso.nombre}<br/>
                                <strong>Descripción:</strong> {curso.descripcion}<br/>
                                <strong>Categoría:</strong> {curso.id_categoria.nombre}<br/>
                                <strong>Fecha inicio:</strong> {curso.fecha_inicio}<br/>
                                <strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}<br/>
                                <strong>Fecha fin:</strong> {curso.fecha_fin}
                            </li>
                        """)
                    bloques.append("</ul>")
                if cursos_consolidacion:
                    bloques.append("<b>Cursos que consolidan este día:</b><ul>")
                    for curso in cursos_consolidacion:
                        bloques.append(f"""
                            <li style="margin-bottom: 10px;">
                                <strong>Nombre:</strong> {curso.nombre}<br/>
                                <strong>Descripción:</strong> {curso.descripcion}<br/>
                                <strong>Categoría:</strong> {curso.id_categoria.nombre}<br/>
                                <strong>Fecha inicio:</strong> {curso.fecha_inicio}<br/>
                                <strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}<br/>
                                <strong>Fecha fin:</strong> {curso.fecha_fin}
                            </li>
                        """)
                    bloques.append("</ul>")

        if not [b for b in bloques if '<li' in b]:
            cuerpo = f"""
                <html>
                    <body>
                        <p>No hay cursos con fechas coincidentes para esta semana ({lunes.strftime('%d/%m/%Y')} - {viernes.strftime('%d/%m/%Y')}).</p>
                    </body>
                </html>
            """
        else:
            cuerpo = f"""
                <html>
                    <body>
                        <p>Resumen semanal de cursos ({lunes.strftime('%d/%m/%Y')} - {viernes.strftime('%d/%m/%Y')}):</p>
                        {''.join(bloques)}
                    </body>
                </html>
            """
        mail_template = {
            'subject': f'Resumen semanal de cursos ({lunes.strftime("%d/%m/%Y")} - {viernes.strftime("%d/%m/%Y")})',
            'body_html': cuerpo.strip(),
            'email_from': self.env.user.email,
            'email_to': ','.join(employees.mapped('work_email')),
        }
        self.env['mail.mail'].create(mail_template).send()