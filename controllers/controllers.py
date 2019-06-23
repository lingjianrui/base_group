# -*- coding: utf-8 -*-
from odoo import http

# class BaseGroup(http.Controller):
#     @http.route('/base_group/base_group/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/base_group/base_group/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('base_group.listing', {
#             'root': '/base_group/base_group',
#             'objects': http.request.env['base_group.base_group'].search([]),
#         })

#     @http.route('/base_group/base_group/objects/<model("base_group.base_group"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('base_group.object', {
#             'object': obj
#         })