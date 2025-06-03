from odoo import models, fields, api # type: ignore

class Aula(models.Model):
    _name = 'gestion_clases.aula'
    _description = 'gestion_clases.aula'
    _rec_name = 'display_name'

    nombre = fields.Char(string='Nombre')
    centro = fields.Char(string='Centro')
    
    display_name = fields.Char(string='Nombre a mostrar', compute='_compute_display_name', store=True)
    
    @api.depends('nombre', 'centro')
    def _compute_display_name(self):
        for aula in self:
            count = self.env['gestion_clases.horario'].search_count([
                ('aula_id', '=', aula.id),
                ('es_plantilla', '=', False)
            ])
            aula.display_name = f"{aula.nombre} - {aula.centro}" if aula.centro else f"{aula.nombre}"