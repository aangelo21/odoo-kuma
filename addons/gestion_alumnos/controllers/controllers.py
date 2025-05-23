# -*- coding: utf-8 -*-
# from odoo import http


# class GestionAlumnos(http.Controller):
#     @http.route('/gestion_alumnos/gestion_alumnos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_alumnos/gestion_alumnos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_alumnos.listing', {
#             'root': '/gestion_alumnos/gestion_alumnos',
#             'objects': http.request.env['gestion_alumnos.gestion_alumnos'].search([]),
#         })

#     @http.route('/gestion_alumnos/gestion_alumnos/objects/<model("gestion_alumnos.gestion_alumnos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_alumnos.object', {
#             'object': obj
#         })

