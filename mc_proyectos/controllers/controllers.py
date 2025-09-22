# -*- coding: utf-8 -*-
# from odoo import http


# class McProyectos(http.Controller):
#     @http.route('/mc_proyectos/mc_proyectos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mc_proyectos/mc_proyectos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mc_proyectos.listing', {
#             'root': '/mc_proyectos/mc_proyectos',
#             'objects': http.request.env['mc_proyectos.mc_proyectos'].search([]),
#         })

#     @http.route('/mc_proyectos/mc_proyectos/objects/<model("mc_proyectos.mc_proyectos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mc_proyectos.object', {
#             'object': obj
#         })

