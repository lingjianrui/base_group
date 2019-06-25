# -*- coding: utf-8 -*-
from odoo import api, models
import pdb



class lead_report(models.AbstractModel):
    
    _name = 'report.base_group.template_lead_report'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        print(data['batch_id'])
        批次 = data['batch_id']
        所有线索 = self.env['crm.lead'].with_context(active_test=False).read_group(domain=[], fields=['depart_id'],groupby='depart_id')
        商机线索 = self.env['crm.lead'].read_group(domain=[('type', '=', 'opportunity')], fields=['name'],groupby='depart_id')
        单批次所有线索 = self.env['crm.lead'].with_context(active_test=False).search([('batch_id','=',批次)])
        单批次线索分组 = self.env['crm.lead'].with_context(active_test=False).read_group(domain=[('batch_id','=',批次)],fields=[],groupby='source_id')
        批次对象 = self.env['import.batch'].search([('id','=',批次)])
        print(单批次线索分组)
        print("-----------------------") 
        print(批次对象.batch_source_id.mapped('source_id'))
        for k in 批次对象.batch_source_id.mapped('source_id'):
            分组 = filter(lambda r: r['source_id'][0] == k.id,单批次线索分组)
            print(list(分组)[0]['source_id_count'])
        单批次 = self.env['import.batch'].search([('id','=',批次)])
        单批次预算 = 单批次['batch_cost']
        单批次平均每条成本 = float(单批次预算)/float(len(单批次所有线索))
        print(所有线索)
        print(商机线索)
        总条数 = 0
        有效总条数 = 0
        print(len(所有线索))
        for i in range(0,len(所有线索)):
           print(所有线索[i]['depart_id'][1])
           总条数 = 总条数 + 所有线索[i]['depart_id_count']
           商机线索总数 = 0
           if len(商机线索) > 0:
                商机线索总数 = self._get_opportunity_count(商机线索, 所有线索[i]['depart_id'][0])
           有效总条数 = 有效总条数 + 商机线索总数
           所有线索[i]['valid_count'] = 商机线索总数
           percent = 商机线索总数 / 所有线索[i]['depart_id_count'] * 100
           print(percent)
           所有线索[i]['valid_count_percentage'] = str('{:.1f}'.format(percent)) + '%'
        #所有线索.sort(key=self._sort_department)
        汇总百分比 = str('{:.1f}'.format(有效总条数 / 总条数 * 100)) + '%'
        return {
                '有效总条数':有效总条数,
                'alead':所有线索,
                '总条数':总条数,
                '汇总百分比': 汇总百分比,
                '单批次所有线索':单批次所有线索,
                '单批次':单批次,
                '单批次线索分组':单批次线索分组,
                '单批次平均每条成本': 单批次平均每条成本
               }
    
    def _get_opportunity_count(self, dicts, depart_id):
        count = 0
        if len(dicts) > 0:
            for d in dicts:
                if d['depart_id'][0] == depart_id:
                    count = d['depart_id_count']
        return count

    def _sort_department(self,elem):
        return elem['depart_id'][0]

