from odoo import models, fields, api  # type: ignore
from odoo.exceptions import ValidationError  # type: ignore
from datetime import datetime, timedelta
import pytz  # type: ignore

class Horario(models.Model):
    _name = 'gestion_clases.horario'
    _description = 'Horario de Clases'
    _rec_name = 'display_name_calendar'

    curso_id = fields.Many2one('gestion_cursos.curso', string='Curso', required=True)
    aula_id = fields.Many2one('gestion_clases.aula', string='Aula')
    aula_display = fields.Many2one('gestion_clases.aula', string='Aula', readonly=True)
    fecha = fields.Datetime(string='Fecha del evento')
    fecha_fin = fields.Datetime(string='Fecha y hora de fin del evento')
    es_plantilla = fields.Boolean(string='Es plantilla', default=True)
    plantilla_id = fields.Many2one('gestion_clases.horario', string='Horario plantilla')
    temario = fields.Text(string='Temario', help='Contenido impartido en la clase')
    tutor_id = fields.Many2one('gestion_cursos.tutor', string='Tutor', help='Tutor que da esta clase específica', domain="[('id_curso', 'in', [curso_id])]")
    
    kanban_state = fields.Selection([
        ('normal', 'Sin incidencias'),
        ('blocked', 'Con incidencias'),
        ('done', 'Completado')
    ], string='Estado Kanban', compute='_compute_kanban_state', store=True, help='Estado de la clase para vista Kanban')

    color_event = fields.Char(string='Color del evento', compute='_compute_color_event', store=True)

    lunes = fields.Boolean(string='Lunes')
    lunes_hora_inicio = fields.Float(string='Hora inicio lunes')
    lunes_hora_fin = fields.Float(string='Hora fin lunes')

    martes = fields.Boolean(string='Martes')
    martes_hora_inicio = fields.Float(string='Hora inicio martes')
    martes_hora_fin = fields.Float(string='Hora fin martes')

    miercoles = fields.Boolean(string='Miércoles')
    miercoles_hora_inicio = fields.Float(string='Hora inicio miércoles')
    miercoles_hora_fin = fields.Float(string='Hora fin miércoles')

    jueves = fields.Boolean(string='Jueves')
    jueves_hora_inicio = fields.Float(string='Hora inicio jueves')
    jueves_hora_fin = fields.Float(string='Hora fin jueves')

    viernes = fields.Boolean(string='Viernes')
    viernes_hora_inicio = fields.Float(string='Hora inicio viernes')
    viernes_hora_fin = fields.Float(string='Hora fin viernes')

    hora_inicio_evento = fields.Float(string='Hora de inicio', compute='_compute_hora_evento', inverse='_inverse_hora_inicio')
    hora_fin_evento = fields.Float(string='Hora de fin', compute='_compute_hora_evento', inverse='_inverse_hora_fin')

    display_name_calendar = fields.Char(string='Nombre para calendario', compute='_compute_display_name_calendar')

    def name_get(self):
        result = []
        for record in self:
            if record.es_plantilla:
                name = f"{record.curso_id.name} - Plantilla"
            else:
                aula_text = f" - {record.aula_id.name}" if record.aula_id else ""
                name = f"{record.curso_id.name}{aula_text}"
            result.append((record.id, name))
        return result

    @api.depends('temario')
    def _compute_color_event(self):
        for record in self:
            record.color_event = '#55eb18' if record.temario else '#f91212'
    
    def recalcular_colores_eventos(self):
        """Método para recalcular los colores de todos los eventos existentes"""
        todos_los_eventos = self.env['gestion_clases.horario'].search([('es_plantilla', '=', False)])
        for evento in todos_los_eventos:
            evento.color_event = '#55eb18' if evento.temario else '#f91212'
      
    @api.depends('temario')
    def _compute_kanban_state(self):
        for record in self:
            if record.temario:
                record.kanban_state = 'done'
            else:
                record.kanban_state = 'normal'

    @api.constrains('lunes', 'lunes_hora_inicio', 'lunes_hora_fin',
                    'martes', 'martes_hora_inicio', 'martes_hora_fin',
                    'miercoles', 'miercoles_hora_inicio', 'miercoles_hora_fin',
                    'jueves', 'jueves_hora_inicio', 'jueves_hora_fin',
                    'viernes', 'viernes_hora_inicio', 'viernes_hora_fin')
    def _check_horas(self):
        for record in self:
            if record.lunes and record.lunes_hora_inicio >= record.lunes_hora_fin:
                raise ValidationError('La hora de inicio del lunes debe ser anterior a la hora de fin')
            if record.martes and record.martes_hora_inicio >= record.martes_hora_fin:
                raise ValidationError('La hora de inicio del martes debe ser anterior a la hora de fin')
            if record.miercoles and record.miercoles_hora_inicio >= record.miercoles_hora_fin:
                raise ValidationError('La hora de inicio del miércoles debe ser anterior a la hora de fin')
            if record.jueves and record.jueves_hora_inicio >= record.jueves_hora_fin:
                raise ValidationError('La hora de inicio del jueves debe ser anterior a la hora de fin')
            if record.viernes and record.viernes_hora_inicio >= record.viernes_hora_fin:
                raise ValidationError('La hora de inicio del viernes debe ser anterior a la hora de fin')

    def _generar_eventos(self):
        self.ensure_one()
        if not self.es_plantilla:
            return

        self.env['gestion_clases.horario'].search([
            ('plantilla_id', '=', self.id),
            ('es_plantilla', '=', False)
        ]).unlink()

        tz = pytz.timezone(self.env.user.tz or 'UTC')
        fecha_actual = self.curso_id.fecha_inicio

        while fecha_actual <= self.curso_id.fecha_fin:
            dia_semana = fecha_actual.weekday()
            hora_inicio = hora_fin = False

            if dia_semana == 0 and self.lunes:
                hora_inicio = self.lunes_hora_inicio
                hora_fin = self.lunes_hora_fin
            elif dia_semana == 1 and self.martes:
                hora_inicio = self.martes_hora_inicio
                hora_fin = self.martes_hora_fin
            elif dia_semana == 2 and self.miercoles:
                hora_inicio = self.miercoles_hora_inicio
                hora_fin = self.miercoles_hora_fin
            elif dia_semana == 3 and self.jueves:
                hora_inicio = self.jueves_hora_inicio
                hora_fin = self.jueves_hora_fin
            elif dia_semana == 4 and self.viernes:
                hora_inicio = self.viernes_hora_inicio
                hora_fin = self.viernes_hora_fin

            if hora_inicio and hora_fin:
                hora_i = int(hora_inicio)
                min_i = int((hora_inicio - hora_i) * 60)
                fecha_inicio = datetime.combine(fecha_actual, datetime.min.time())
                fecha_inicio = fecha_inicio.replace(hour=hora_i, minute=min_i)
                local_dt = tz.localize(fecha_inicio)
                fecha_inicio_utc = local_dt.astimezone(pytz.UTC).replace(tzinfo=None)

                hora_f = int(hora_fin)
                min_f = int((hora_fin - hora_f) * 60)
                fecha_fin = datetime.combine(fecha_actual, datetime.min.time())
                fecha_fin = fecha_fin.replace(hour=hora_f, minute=min_f)
                local_dt_fin = tz.localize(fecha_fin)
                fecha_fin_utc = local_dt_fin.astimezone(pytz.UTC).replace(tzinfo=None)

                self.env['gestion_clases.horario'].create({
                    'curso_id': self.curso_id.id,
                    'aula_id': self.aula_id.id,
                    'fecha': fecha_inicio_utc,
                    'fecha_fin': fecha_fin_utc,
                    'es_plantilla': False,
                    'plantilla_id': self.id,
                })

            fecha_actual += timedelta(days=1)
    @api.model
    def create(self, vals):
        if 'aula_id' in vals:
            vals['aula_display'] = vals['aula_id']
        record = super().create(vals)
        if record.es_plantilla:
            record._generar_eventos()
        return record
    
    def write(self, vals):
        # Detectar si se está añadiendo temario por primera vez
        enviar_correo = False
        for record in self:
            if 'temario' in vals and vals['temario'] and not record.temario:
                enviar_correo = True
                break
        
        # No actualizamos aula_display aunque cambie aula_id
        result = super().write(vals)
        
        # Enviar correo si se añadió temario por primera vez
        if enviar_correo:
            for record in self:
                if not record.es_plantilla and record.temario:
                    record._send_email_notificacion()
        
        # Regenerar eventos si es una plantilla y se han modificado campos relevantes
        campos_relevantes = [
            'curso_id', 'aula_id', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes',
            'lunes_hora_inicio', 'lunes_hora_fin', 'martes_hora_inicio', 'martes_hora_fin',
            'miercoles_hora_inicio', 'miercoles_hora_fin', 'jueves_hora_inicio', 'jueves_hora_fin',
            'viernes_hora_inicio', 'viernes_hora_fin'
        ]
        
        if any(campo in vals for campo in campos_relevantes):
            for record in self:
                if record.es_plantilla:
                    record._generar_eventos()
        
        return result

    @api.constrains('aula_id', 'fecha', 'fecha_fin')
    def _check_solapamiento_eventos(self):
        """Validation for non-template events (panel de aulas)"""
        for record in self:
            # Skip validation for templates or if skip flag is set
            if record.es_plantilla or self.env.context.get('skip_overlap_validation', False):
                continue

            if not record.aula_id or not record.fecha or not record.fecha_fin:
                continue

            domain = [
            ('id', '!=', record.id),
            ('aula_id', '=', record.aula_id.id),
            ('es_plantilla', '=', False),
            ('fecha', '<', record.fecha_fin),
            ('fecha_fin', '>', record.fecha)
            ]

            if self.search_count(domain) > 0:
                raise ValidationError('El aula ya está ocupada en la fecha y horario seleccionados')


    def _send_email_notificacion(self):
        employees = self.env['hr.employee'].search([])
        fecha_local = fields.Datetime.context_timestamp(self, self.fecha)
        fecha_fin_local = fields.Datetime.context_timestamp(self, self.fecha_fin)
        
        mail_template = {
            'subject': f'Clase lista para subir a plataforma - {self.curso_id.nombre}',
            'body_html': f'''
                <p>Se ha completado el temario de una clase y está lista para subirse a la plataforma:</p>
                <ul>
                    <li><strong>Curso:</strong> {self.curso_id.nombre}</li>
                    <li><strong>Aula:</strong> {self.aula_id.display_name}</li>
                    <li><strong>Tutor:</strong> {self.tutor_id.nombre if self.tutor_id else 'No asignado'}</li>
                    <li><strong>Hora inicio:</strong> {fecha_local.strftime('%H:%M')}</li>
                    <li><strong>Hora fin:</strong> {fecha_fin_local.strftime('%H:%M')}</li>
                    <li><strong>Contenido impartido:</strong> {self.temario}</li>
                </ul>
            ''',
            'email_from': self.env.user.email,
            'email_to': ','.join(employees.mapped('work_email')),
        }
        self.env['mail.mail'].create(mail_template).send()

    @api.constrains('aula_id', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes',
                    'lunes_hora_inicio', 'lunes_hora_fin',
                    'martes_hora_inicio', 'martes_hora_fin',
                    'miercoles_hora_inicio', 'miercoles_hora_fin',
                    'jueves_hora_inicio', 'jueves_hora_fin',
                    'viernes_hora_inicio', 'viernes_hora_fin')
    
    def _check_solapamiento(self):
        for record in self:
            if not record.aula_id:
                continue

            domain = [
                ('id', '!=', record.id),
                ('aula_id', '=', record.aula_id.id),
            ]

            if record.es_plantilla:
                domain.append(('es_plantilla', '=', True))
            
                dias = []
                horas = {}
            
                if record.lunes:
                    dias.append(('lunes', '=', True))
                    horas['lunes'] = (record.lunes_hora_inicio, record.lunes_hora_fin)
                if record.martes:
                    dias.append(('martes', '=', True))
                    horas['martes'] = (record.martes_hora_inicio, record.martes_hora_fin)
                if record.miercoles:
                    dias.append(('miercoles', '=', True))
                    horas['miercoles'] = (record.miercoles_hora_inicio, record.miercoles_hora_fin)
                if record.jueves:
                    dias.append(('jueves', '=', True))
                    horas['jueves'] = (record.jueves_hora_inicio, record.jueves_hora_fin)
                if record.viernes:
                    dias.append(('viernes', '=', True))
                    horas['viernes'] = (record.viernes_hora_inicio, record.viernes_hora_fin)

                if dias:
                    if len(dias) > 1:
                        domain.extend(['|'] * (len(dias) - 1))
                    domain.extend(dias)

                otros_horarios = self.search(domain)
            
                for otro in otros_horarios:
                    if (otro.curso_id.fecha_fin >= record.curso_id.fecha_inicio and 
                        otro.curso_id.fecha_inicio <= record.curso_id.fecha_fin):
                    
                        for dia, (hora_inicio, hora_fin) in horas.items():
                            otro_hora_inicio = getattr(otro, f'{dia}_hora_inicio')
                            otro_hora_fin = getattr(otro, f'{dia}_hora_fin')
                        
                            if getattr(otro, dia) and (
                                (hora_inicio < otro_hora_fin and hora_fin > otro_hora_inicio)
                            ):
                                raise ValidationError(
                                    f'Ya existe una plantilla de horario que usa esta aula el {dia} '
                                    f'en el horario seleccionado durante las fechas del curso'
                                )

    def unlink(self):
        for record in self:
            if record.es_plantilla:
                self.env['gestion_clases.horario'].search([
                    ('plantilla_id', '=', record.id),
                    ('es_plantilla', '=', False)
                ]).unlink()
        return super().unlink()

    @api.model
    def _read_group_aula_id(self, aulas, domain, order):
        # Obtener todas las aulas activas
        all_aulas = self.env['gestion_clases.aula'].search([])
        
        # Configurar columnas plegadas por defecto (aulas sin registros)
        aula_data = []
        for aula in all_aulas:
            aula_count = self.search_count([('aula_id', '=', aula.id)] + domain)
            aula_data.append((aula.id, aula.display_name, aula_count == 0))  # True = plegada si no hay registros
        
        return all_aulas

    _group_by_full = {
        'aula_id': lambda self, *args, **kwargs: self._read_group_aula_id(*args, **kwargs),
    }

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if 'aula_id' in groupby:
            Aula = self.env['gestion_clases.aula']
            aulas = Aula.search([])
  
            res = super(Horario, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
            
            aulas_con_eventos = {r['aula_id'][0]: r for r in res if r.get('aula_id')}
            
            result = []
            for aula in aulas:
                if aula.id in aulas_con_eventos:
                    group_data = aulas_con_eventos[aula.id]
                    # No plegar si tiene registros
                    group_data['__fold'] = False
                    result.append(group_data)
                else:
                    # Plegar columnas vacías por defecto
                    result.append({
                        'aula_id': (aula.id, aula.display_name),
                        'aula_id_count': 0,
                        '__domain': [(u'aula_id', '=', aula.id)] + domain,
                        '__fold': True  # Plegar columnas vacías
                    })
            return result
        return super(Horario, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

    @api.depends('fecha', 'fecha_fin')
    def _compute_hora_evento(self):
        for record in self:
            if record.fecha:
                fecha_local = fields.Datetime.context_timestamp(record, record.fecha)
                record.hora_inicio_evento = fecha_local.hour + fecha_local.minute / 60.0
            else:
                record.hora_inicio_evento = 0.0
                
            if record.fecha_fin:
                fecha_fin_local = fields.Datetime.context_timestamp(record, record.fecha_fin)
                record.hora_fin_evento = fecha_fin_local.hour + fecha_fin_local.minute / 60.0
            else:
                record.hora_fin_evento = 0.0
    
    def _inverse_hora_inicio(self):
        for record in self:
            if record.fecha and record.hora_inicio_evento:
                fecha_local = fields.Datetime.context_timestamp(record, record.fecha)
                hora = int(record.hora_inicio_evento)
                minuto = int((record.hora_inicio_evento - hora) * 60)
                nueva_fecha = fecha_local.replace(hour=hora, minute=minuto, second=0, microsecond=0)
                nueva_fecha_utc = nueva_fecha.astimezone(pytz.UTC).replace(tzinfo=None)
                record.fecha = nueva_fecha_utc

    def _inverse_hora_fin(self):
        for record in self:
            if record.fecha_fin and record.hora_fin_evento:
                fecha_fin_local = fields.Datetime.context_timestamp(record, record.fecha_fin)
                hora = int(record.hora_fin_evento)
                minuto = int((record.hora_fin_evento - hora) * 60)
                nueva_fecha_fin = fecha_fin_local.replace(hour=hora, minute=minuto, second=0, microsecond=0)
                nueva_fecha_fin_utc = nueva_fecha_fin.astimezone(pytz.UTC).replace(tzinfo=None)
                record.fecha_fin = nueva_fecha_fin_utc    @api.depends('curso_id', 'aula_display')
    def _compute_display_name_calendar(self):
        for record in self:
            curso_name = record.curso_id.nombre if record.curso_id else ""
            aula_name = record.aula_display.nombre if record.aula_display else ""
            
            # Crear el nombre para el calendario (aula arriba, curso abajo)
            if curso_name and aula_name:
                record.display_name_calendar = f"{aula_name}\n{curso_name}"
            elif curso_name:
                record.display_name_calendar = curso_name
            elif aula_name:
                record.display_name_calendar = aula_name
            else:
                record.display_name_calendar = ""
