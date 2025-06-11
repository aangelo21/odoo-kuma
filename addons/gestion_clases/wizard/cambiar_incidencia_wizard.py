from odoo import models, fields, api # type: ignore

class CambiarIncidenciaWizard(models.TransientModel):
    _name = 'gestion_clases.cambiar_incidencia_wizard'
    _description = 'Wizard para Cambiar Incidencia de Horario'

    horario_id = fields.Many2one('gestion_clases.horario', string="Horario", required=True, readonly=True)
    # Assuming these are the selection values based on your Kanban view.
    # It's best to get these from the original 'incidencias' field definition in 'gestion_clases.horario' model.
    incidencias_field = fields.Selection([
        ('camara_en_negro', 'Cámara en Negro'),
        ('imagen_congelada', 'Imagen Congelada'),
        ('pte_grabacion_otra_clase', 'Pte. Grabación Otra Clase'),
        ('sin_sonido', 'Sin Sonido'),
        ('no_grabado', 'No Grabado'),
        ('no_subido_a_vimeo', 'No Subido a Vimeo'),
        ('pte_de_edicion', 'Pte. de Edición'),
        ('problemas_microfono', 'Problemas Micrófono'),
    ], string='Incidencia')

    @api.model
    def default_get(self, fields_list):
        res = super(CambiarIncidenciaWizard, self).default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id:
            horario = self.env['gestion_clases.horario'].browse(active_id)
            res['horario_id'] = horario.id
            res['incidencias_field'] = horario.incidencias # Pre-fill with current incidence
        return res

    def action_guardar_incidencia(self):
        self.ensure_one()
        if self.horario_id:
            self.horario_id.write({'incidencias': self.incidencias_field})
        return {'type': 'ir.actions.act_window_close'}
