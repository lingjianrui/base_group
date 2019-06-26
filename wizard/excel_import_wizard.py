# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _
import time
import traceback
from xmlrpc import client
import pdb
class ExcelImportWizard(models.TransientModel):
    _name = 'excel.import.wizard'

    _inherit = ['odo.base.import.excel.wizard']
    _description = '基本信息导入向导'
    def process_import_item(self, item, a):
        print(a)
        #pdb.set_trace()
        主键 = item["客户电话"]
        员工姓名 = item["招商员工"]
        客户姓名 = item["客户姓名"]
        客户电话 = item["客户电话"]
        信息来源 = item["信息来源"]
        信息反馈 = item["信息反馈"]
        分条日期 = item["分条日期"]
        error_msg = ''
        #if 主键 == '' or not isinstance(主键,str):
        #    error_msg = error_msg + '手机号格式不是字符串格式['+主键+']'
        u = self.env['res.users'].search([('name', '=', 员工姓名 )])
        if not u:
            error_msg = error_msg + '系统找不到用户['+员工姓名+']'
        s = self.env['utm.source'].search([('name', '=', 信息来源 )])
        if not s:
            error_msg = error_msg + '系统找不到信息来源['+信息来源+']'
        try:
            ss = time.strftime('%Y',time.localtime(time.time()))+'.'+str(分条日期)
            d = time.strptime(ss,"%Y.%m.%d")
            dd = time.strftime('%Y-%m-%d',d)
            sid = self.env['crm.team'].search([('member_ids','in',u.id)]).depart_id.id
            value = {'user_id': u.id,'contact_name':客户姓名,'name':客户姓名,'source_id':s.id,'dispatch_date':dd,'probability':10,'depart_id':sid,'batch_id':a}
            print(value)
            obj = self.env['crm.lead'].search([('phone', '=', 主键)])
            ob = self.env['res.partner'].search([('phone', '=', 主键)])
            if obj:
                if obj[0].user_id.name != 员工姓名:  
                    self.env['lead.duplicate'].create({'name':obj[0].name,'wname':员工姓名,'phone':obj[0].phone,'uname':obj[0].user_id.id,'opt_time':obj[0].create_date})
            elif ob:
                if ob[0].user_id.name != 员工姓名:
                    self.env['lead.duplicate'].create({'name':ob[0].name,'wname':员工姓名,'phone':ob[0].phone,'uname':ob[0].user_id.id,'opt_time':ob[0].create_date})
            else:
                obj2 = self.env['crm.lead'].search(['&',('phone', '=', 主键),('active','=',False)])
                if not obj2:
                    value['phone'] = 主键
                    obj.create(value)
        except Exception as e:
            msg = traceback.format_exc()
            print(msg)
            error_msg = error_msg + '请检查时间格式 应该为("3.10"), 错误格式['+str(分条日期)+']'

        return error_msg

