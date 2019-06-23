# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _
import time
import traceback
import pdb
class LeadReportWizard(models.TransientModel):
    _name = 'lead_report.wizard'
    _description = '基本信息导入向导'
    batch_id = fields.Many2one('import.batch',string="批次")
    @api.multi 
    def gen_report(self):
        docs = {"batch_id":self.batch_id.id}
        return self.env.ref("base_group.lead_report").report_action(self, data=docs)




