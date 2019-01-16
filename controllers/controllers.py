# -*- coding: utf-8 -*-
from odoo import http

# class Construction(http.Controller):
#     @http.route('/construction/construction/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/construction/construction/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('construction.listing', {
#             'root': '/construction/construction',
#             'objects': http.request.env['construction.construction'].search([]),
#         })

#     @http.route('/construction/construction/objects/<model("construction.construction"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('construction.object', {
#             'object': obj
#         })