# -*- coding: utf-8 -*-
# from odoo import http


# class GestionCursos(http.Controller):
#     @http.route('/gestion_cursos/gestion_cursos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_cursos/gestion_cursos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_cursos.listing', {
#             'root': '/gestion_cursos/gestion_cursos',
#             'objects': http.request.env['gestion_cursos.gestion_cursos'].search([]),
#         })

#     @http.route('/gestion_cursos/gestion_cursos/objects/<model("gestion_cursos.gestion_cursos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_cursos.object', {
#             'object': obj
#         })

