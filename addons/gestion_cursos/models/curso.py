from datetime import date, timedelta
from odoo import models, fields, api # type: ignore

class Curso(models.Model):
    _name = 'gestion_cursos.curso'
    _description = 'gestion_cursos.curso'
    _rec_name = 'nombre'    
    nombre = fields.Char(string = 'Nombre')
    expediente = fields.Char(string = 'Expediente')
    codigo = fields.Char(string = 'Código')    
    id_tutor = fields.Many2many('gestion_cursos.tutor', string='Tutores')
    tutor = fields.Char(string='Tutores (texto)', compute='_compute_tutor_display', store=False)
    duracion = fields.Integer(string = 'Duración')
    modalidad = fields.Selection([
        ('presencial', 'Presencial'),
        ('semipresencial', 'Semipresencial'),
        ('teleformación', 'Teleformación')], string = 'Modalidad')
    tipo_destinatario = fields.Selection([
        ('desempleados', 'Desempleados'),
        ('ocupados', 'Ocupados'),], string = 'Destinatario')
    numero_alumnos = fields.Integer(string = 'Número de alumnos')
    numero_alumnos_consolidacion = fields.Integer(string = 'Número de alumnos consolidación')
    numero_alumnos_finalizados = fields.Integer(string = 'Número de alumnos finalizados')
    fecha_inicio = fields.Date(string='Fecha Inicio')
    fecha_fin = fields.Date(string='Fecha Fin')
    fecha_consolidacion = fields.Date(string='Fecha de consolidación')
    id_categoria = fields.Many2one('gestion_cursos.categoria', string='Categoría')
    color_categoria = fields.Selection(
        related='id_categoria.color',
        string='Color de categoría',
        store=False
    )

    color_calendar = fields.Char(string='Color calendario', compute='_compute_color_calendar', store=True)
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
            if total > 0:
                record.consolidados_display = f"{consolidados}/{total}"
            else:
                record.consolidados_display = "0/0"
    
    @api.depends('numero_alumnos_finalizados', 'numero_alumnos_consolidacion')
    def _compute_finalizados_display(self):
        for record in self:
            finalizados = record.numero_alumnos_finalizados or 0
            consolidados = record.numero_alumnos_consolidacion or 0
            if consolidados > 0:
                record.finalizados_display = f"{finalizados}/{consolidados}"
            else:
                record.finalizados_display = "0/0"

    @api.depends('id_tutor')
    def _compute_tutor_display(self):
        for record in self:
            if record.id_tutor:
                record.tutor = ', '.join(record.id_tutor.mapped('nombre'))
            else:
                record.tutor = ''

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
                        <li><strong>Expediente:</strong> {curso.expediente}</li>
                        <li><strong>Código:</strong> {curso.codigo}</li>
                        <li><strong>Tutor:</strong> {curso.tutor}</li>
                        <li><strong>Categoría:</strong> {curso.id_categoria.nombre if curso.id_categoria else 'N/A'}</li>
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
                        <li><strong>Expediente:</strong> {curso.expediente}</li>
                        <li><strong>Tutor:</strong> {curso.tutor}</li>
                        <li><strong>Categoría:</strong> {curso.id_categoria.nombre if curso.id_categoria else 'N/A'}</li>
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
                    <strong>Expediente:</strong> {curso.expediente}<br/>
                    <strong>Tutor:</strong> {curso.tutor}<br/>
                    <strong>Categoría:</strong> {curso.id_categoria.nombre if curso.id_categoria else 'N/A'}<br/>
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
                    <strong>Expediente:</strong> {curso.expediente}<br/>
                    <strong>Tutor:</strong> {curso.tutor}<br/>
                    <strong>Categoría:</strong> {curso.id_categoria.nombre if curso.id_categoria else 'N/A'}<br/>
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
                    <strong>Expediente:</strong> {curso.expediente}<br/>
                    <strong>Tutor:</strong> {curso.tutor}<br/>
                    <strong>Categoría:</strong> {curso.id_categoria.nombre if curso.id_categoria else 'N/A'}<br/>
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
        for i in range(5):
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
                                <strong>Expediente:</strong> {curso.expediente}<br/>
                                <strong>Tutor:</strong> {curso.tutor}<br/>
                                <strong>Categoría:</strong> {curso.id_categoria.nombre if curso.id_categoria else 'N/A'}<br/>
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
                                <strong>Expediente:</strong> {curso.expediente}<br/>
                                <strong>Tutor:</strong> {curso.tutor}<br/>
                                <strong>Categoría:</strong> {curso.id_categoria.nombre if curso.id_categoria else 'N/A'}<br/>
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
                                <strong>Expediente:</strong> {curso.expediente}<br/>
                                <strong>Tutor:</strong> {curso.tutor}<br/>
                                <strong>Categoría:</strong> {curso.id_categoria.nombre if curso.id_categoria else 'N/A'}<br/>
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
    
    @api.depends('id_categoria.color')
    def _compute_color_calendar(self):
        for record in self:
            record.color_calendar = record.id_categoria.color if record.id_categoria else False
            
    @api.model
    def cron_aviso_dos_semanas_inicio(self):
        """Función para notificar cuando faltan 2 semanas para que inicie un curso"""
        hoy = date.today()
        fecha_dos_semanas = hoy + timedelta(days=14)
        employees = self.env['hr.employee'].search([])
        
        # Buscar cursos que inicien en la fecha de dos semanas (sin importar la hora)
        cursos_dos_semanas = self.search([
            ('fecha_inicio', '>=', fecha_dos_semanas),
            ('fecha_inicio', '<', fecha_dos_semanas + timedelta(days=1))
        ])
        
        if cursos_dos_semanas:
            bloques = ["<h3>RRSS + Cartel: Cursos que iniciarán en 2 semanas:</h3><ul>"]
            for curso in cursos_dos_semanas:
                bloques.append(f"""
                <li style="margin-bottom: 20px;">
                    <strong>Nombre:</strong> {curso.nombre}<br/>
                    <strong>Expediente:</strong> {curso.expediente}<br/>
                    <strong>Código:</strong> {curso.codigo}<br/>
                    <strong>Tutor:</strong> {curso.tutor}<br/>
                    <strong>Categoría:</strong> {curso.id_categoria.nombre if curso.id_categoria else 'N/A'}<br/>
                    <strong>Modalidad:</strong> {curso.modalidad}<br/>
                    <strong>Duración:</strong> {curso.duracion}h<br/>
                    <strong>Número de alumnos:</strong> {curso.numero_alumnos}<br/>
                    <strong>Fecha inicio:</strong> {curso.fecha_inicio}<br/>
                    <strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}<br/>
                    <strong>Fecha fin:</strong> {curso.fecha_fin}
                </li>
                <br>
            """)
            bloques.append("</ul>")
            
            cuerpo = f"""
                <html>
                    <body>
                        <p>Recordatorio: Los siguientes cursos iniciarán dentro de 2 semanas ({fecha_dos_semanas.strftime('%d/%m/%Y')}):</p>
                        {''.join(bloques)}
                    </body>
                </html>
            """
            
            mail_template = {
                'subject': f'Recordatorio: Cursos que inician en 2 semanas ({fecha_dos_semanas.strftime("%d/%m/%Y")})',
                'body_html': cuerpo.strip(),
                'email_from': self.env.user.email,
                'email_to': ','.join(employees.mapped('work_email')),
            }
            self.env['mail.mail'].create(mail_template).send()

    @api.model
    def cron_aviso_una_semana_inicio(self):
        """Función para notificar cuando falta 1 semana para que inicie un curso"""
        hoy = date.today()
        fecha_una_semana = hoy + timedelta(days=7)
        employees = self.env['hr.employee'].search([])
        
        # Buscar cursos que inicien en la fecha de una semana (sin importar la hora)
        cursos_una_semana = self.search([
            ('fecha_inicio', '>=', fecha_una_semana),
            ('fecha_inicio', '<', fecha_una_semana + timedelta(days=1))
        ])
        
        if cursos_una_semana:
            bloques = ["<h3>RRSS + Cartel: Cursos que iniciarán en 1 semana:</h3><ul>"]
            for curso in cursos_una_semana:
                bloques.append(f"""
                <li style="margin-bottom: 20px;">
                    <strong>Nombre:</strong> {curso.nombre}<br/>
                    <strong>Expediente:</strong> {curso.expediente}<br/>
                    <strong>Código:</strong> {curso.codigo}<br/>
                    <strong>Tutor:</strong> {curso.tutor}<br/>
                    <strong>Categoría:</strong> {curso.id_categoria.nombre if curso.id_categoria else 'N/A'}<br/>
                    <strong>Modalidad:</strong> {curso.modalidad}<br/>
                    <strong>Duración:</strong> {curso.duracion}h<br/>
                    <strong>Número de alumnos:</strong> {curso.numero_alumnos}<br/>
                    <strong>Fecha inicio:</strong> {curso.fecha_inicio}<br/>
                    <strong>Fecha consolidación:</strong> {curso.fecha_consolidacion}<br/>
                    <strong>Fecha fin:</strong> {curso.fecha_fin}
                </li>
                <br>
            """)
            bloques.append("</ul>")
            
            cuerpo = f"""
                <html>
                    <body>
                        <p>¡Atención! Los siguientes cursos iniciarán dentro de 1 semana ({fecha_una_semana.strftime('%d/%m/%Y')}):</p>
                        {''.join(bloques)}
                    </body>
                </html>
            """
            
            mail_template = {
                'subject': f'¡Próximo inicio! Cursos que inician en 1 semana ({fecha_una_semana.strftime("%d/%m/%Y")})',
                'body_html': cuerpo.strip(),
                'email_from': self.env.user.email,
                'email_to': ','.join(employees.mapped('work_email')),
            }
            self.env['mail.mail'].create(mail_template).send()