# -*- coding: utf-8 -*-
# from odoo import http


# class GestionComerciales(http.Controller):
#     @http.route('/gestion_comerciales/gestion_comerciales', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_comerciales/gestion_comerciales/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_comerciales.listing', {
#             'root': '/gestion_comerciales/gestion_comerciales',
#             'objects': http.request.env['gestion_comerciales.gestion_comerciales'].search([]),
#         })

#     @http.route('/gestion_comerciales/gestion_comerciales/objects/<model("gestion_comerciales.gestion_comerciales"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_comerciales.object', {
#             'object': obj
#         })

