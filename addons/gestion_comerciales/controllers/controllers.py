# -*- coding: utf-8 -*-
from odoo import http  # type: ignore
from odoo.http import request  # type: ignore
import json

class CaptacionController(http.Controller):
    
    @http.route('/gestion_comerciales/chart_data', type='json', auth='user')
    def get_chart_data(self):
        """Endpoint para obtener datos del gráfico via AJAX"""
        captacion_model = request.env['gestion_comerciales.captacion_alumnos']
        data = captacion_model.get_chart_data()
        return data
    
    @http.route('/gestion_comerciales/dashboard', type='http', auth='user')
    def dashboard(self):
        """Renderizar el dashboard principal"""
        return request.render('gestion_comerciales.dashboard_template', {
            'page_title': 'Dashboard Captación de Alumnos'
        })

