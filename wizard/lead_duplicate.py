# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _

class LeadDuplicate(models.TransientModel):
    _name = 'lead.duplicate'
    _description = 'lead duplicate'
    name = fields.Char(string="姓名")
    phone = fields.Char(string="电话")
    uname = fields.Many2one('res.users',string='已经分派')
    wname = fields.Char(string='将要分派')
    opt_time = fields.Datetime(string='操作时间')
