# -*- coding: utf-8 -*-
# from odoo import http


# class GestionClases(http.Controller):
#     @http.route('/gestion_clases/gestion_clases', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_clases/gestion_clases/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_clases.listing', {
#             'root': '/gestion_clases/gestion_clases',
#             'objects': http.request.env['gestion_clases.gestion_clases'].search([]),
#         })

#     @http.route('/gestion_clases/gestion_clases/objects/<model("gestion_clases.gestion_clases"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_clases.object', {
#             'object': obj
#         })

