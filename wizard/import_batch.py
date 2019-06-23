# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _

class ImportBatch(models.Model):
    _name = 'import.batch'
    _description = '导入的批次管理，用于计算购买线索的成本'
    _rec_name = 'batch_no'
    batch_no = fields.Char(string='批次编号')
    batch_cost = fields.Float(string='总花费')
    batch_source_id = fields.One2many(comodel_name='batch.source',inverse_name='batch_id',string='资源批次')

    @api.onchange('batch_source_id')
    def _onchange_batch_source_id(self):
        if len(self.batch_source_id) > 0:
            self.batch_cost = sum(self.batch_source_id.mapped('source_cost'))
        else:
            self.batch_cost = 0
