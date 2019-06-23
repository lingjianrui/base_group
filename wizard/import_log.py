# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _

class ImportLog(models.TransientModel):
    _name = 'import.log'
    _description = 'import log'
    name = fields.Char(string='操作人员')
    status = fields.Char(string='状态')
    opt_time = fields.Datetime(string='操作时间')
