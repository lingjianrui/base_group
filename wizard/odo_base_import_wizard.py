# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _
import datetime
import pandas as pd
import base64
import re
import logging
from odoo import exceptions
class OdoBaseImportExcelWizard(models.TransientModel):
    _name = 'odo.base.import.excel.wizard'
    _description = '基本信息导入向导'

    excel = fields.Binary(string='文件', attachment=True, required=True)
    batch_id = fields.Many2one('import.batch',string="批次")
    def convert_list_date_item(self, item_list, key_list):
        # 定义转化日期戳的函数,dates为日期戳
        for key in key_list:
            item_time = item_list.get(key)
            if item_time:
                if type(item_time) == int:
                    delta = datetime.timedelta(days=item_time)
                    item_list[key] = datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + delta

                elif type(item_time) == datetime.time:
                    item_list[key] = False

                elif type(item_time) == str:
                    item_list[key] = False

        return True

    def process_import_item(self, item, a):
        """

        :param item:
        :return:
        """
        print('hello')
        print(item[u'客户电话'])
        #self.env['item'].search([('state', '!=', 'manual')])
        return False



    @api.one
    def do_import(self):

        domain = [('res_model', '=', self._name), ('res_field', '=', "excel"),('res_id', '=', self.id)]
        attach = self.env['ir.attachment'].sudo().search(domain)
        returnlist = []
        if attach.store_fname:
            attach_full_path = attach._full_path(attach.store_fname)

            df_res = pd.read_excel(attach_full_path).fillna(value=False)
        
            for index, row in df_res.iterrows():
                item = row.to_dict()

                i = self.process_import_item(item,self.batch_id.id)
                if i != '':
                    returnlist.append(i)
        if len(returnlist) != 0:
            #raise osv.except_osv(_('错误'), returnlist)) 
            
            raise exceptions.Warning(returnlist)
        else:
            self.env['import.log'].create({'name':self.env.user.name,'status':'导入成功'})
        #print(self.env['warning'].info(self.env.uid, title='Export imformation', message="%s products Created, %s products Updated "%('abc','++++')))
        #return self.env['warning'].info(self.env.uid, title='Export imformation', message="%s products Created, %s products Updated "%('abc','++++'))




