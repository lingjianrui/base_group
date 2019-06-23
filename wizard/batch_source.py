# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _

class BatchSource(models.Model):
    _name = 'batch.source'
    _description = '批次 资源类型'
    batch_id = fields.Many2one(comodel_name='import.batch',string='批次编号')
    source_id = fields.Many2one('utm.source',string="资源")
    source_cost = fields.Float(string='资源花费')
