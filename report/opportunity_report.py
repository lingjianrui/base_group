# -*- coding: utf-8 -*-
from odoo import api, models
import pdb
import datetime
import decimal

class opportunity_report(models.AbstractModel):
    
    _name = 'report.base_group.template_opportunity_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        result = []
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_year = datetime.datetime.now().strftime('%Y')
        current_month = datetime.datetime.now().strftime('%m')
        this_year = str(current_year)+'-01-01 00:00:00'
        this_month = str(current_year)+'-'+current_month+'-'+'01 00:00:00'
        time_start = str(current_year)+'-'+current_month+'-'+'01'
        time_end = datetime.datetime.now().strftime('%Y-%m-%d')

        #根据登陆用户判断是否是部门负责人
        d = self.env['crm.depart'].search([('user_id','=',self.env.user.id)])
        if d or (self.env.ref('base_group.sales_vp_group').id in self.env.user.groups_id.mapped('id')):
            all_depart = self.env['crm.depart'].sudo().search([])
            for depart in all_depart:
                #如果是负责人 根据user_id 查出 年签约目标
                if depart.user_id == d.user_id or (self.env.ref('base_group.sales_vp_group').id in self.env.user.groups_id.mapped('id')):
                    depart_name = depart.name if depart.name != None else ""
                    manager_name = depart.user_id.name if depart.user_id.name != None else ""
                    year_target = decimal.Decimal(depart.year_target) if depart.year_target != None else 0
                    year_back_target = decimal.Decimal(depart.year_back_target) if depart.year_back_target != None else 0
                    year_invite_target = decimal.Decimal(depart.year_invite_target) if depart.year_invite_target != None else 0
                    month_target = decimal.Decimal(depart.month_target) if depart.month_target != None else 0
                    month_back_target = decimal.Decimal(depart.month_back_target) if  depart.month_back_target != None else 0
                    month_invite_target = decimal.Decimal(depart.month_invite_target) if depart.month_invite_target != None else 0
                    #根据负责人的depart_id查出 所有的手下员工
                    team_members = self.env['res.users'].sudo().search([('sale_team_id','in',depart.team_ids.mapped('id'))])
                    #从sale_order里面根据手下员工的id 查出所有的订单的总额 求和
                    team_orders = self.env['sale.order'].sudo().search(['&','&',('user_id','in',team_members.mapped('id')),('create_date','>',this_year),('create_date','<=',current_datetime)])
                    month_team_orders = self.env['sale.order'].sudo().search(['&','&',('user_id','in',team_members.mapped('id')),('create_date','>',this_month),('create_date','<=',current_datetime)])
                    #月签约完成
                    month_signed_total = decimal.Decimal.from_float(sum(month_team_orders.mapped('amount_total')))
                    #月回款完成
                    month_back_total = month_team_orders.mapped(lambda r: sum(r.invoice_ids.mapped('amount_total')))
                    month_back_total = decimal.Decimal.from_float(sum(month_back_total) if len(month_back_total) > 0 else 0)
                    #月邀约完成
                    month_opp_total = self.env['crm.lead'].sudo().search(['&','&',('user_id','in',team_members.mapped('id')),('type','=','opportunity'),('create_date','>',this_month),('create_date','<=',current_datetime)])
                    month_opp_done = len(month_opp_total.filtered(lambda r: r.stage_id.name == '来访')) + len(month_opp_total.filtered(lambda r: r.stage_id.name == '赢得'))
                    #年签约完成
                    signed_total = decimal.Decimal.from_float(sum(team_orders.mapped('amount_total')))
                    #年回款完成

                    back_total_var = team_orders.mapped(lambda r: sum(r.invoice_ids.mapped('amount_total')))
                    back_total = decimal.Decimal.from_float(back_total_var[0] if len(back_total_var) > 0 else 0)
                    #年邀约完成 = 商机状态 来访 + 赢得的商机个数的和
                    opp_total = self.env['crm.lead'].sudo().search(['&',('user_id','in',team_members.mapped('id')),('type','=','opportunity')])
                    opp_done = len(opp_total.filtered(lambda r: r.stage_id.name == '来访')) + len(opp_total.filtered(lambda r: r.stage_id.name == '赢得'))
                    #计算完成百分比
                    year_signed_percent = signed_total / year_target * 100 if year_target != 0 else 0
                    month_signed_percent = month_signed_total / month_target * 100 if month_target != 0 else 0
                    year_back_percent =  back_total / year_back_target * 100 if year_back_target != 0 else 0
                    month_back_percent = month_back_total / month_back_target * 100 if month_back_target != 0 else 0
                    year_invite_percent = opp_done / year_invite_target * 100 if year_invite_target !=0 else 0
                    month_invte_percent = month_opp_done / month_invite_target * 100 if month_invite_target != 0 else 0
                    re = {
                      '部门名称': depart_name,
                      '部门负责人': manager_name,
                      '年签约目标':year_target/10000, 
                      '年回款目标':year_back_target/10000,
                      '年邀约目标':year_invite_target,
                      '年签约完成':signed_total/10000,
                      '年回款完成':back_total/10000,
                      '年邀约完成':opp_done,
                      '月签约目标':month_target/10000,
                      '月回款目标':month_back_target/10000,
                      '月邀约目标':month_invite_target,
                      '月签约完成':month_signed_total/10000,
                      '月回款完成':month_back_total/10000,
                      '月邀约完成':month_opp_done,
                      '年签约完成比例': decimal.Decimal(year_signed_percent).quantize(decimal.Decimal('0.00')),
                      '月签约完成比例': decimal.Decimal(month_signed_percent).quantize(decimal.Decimal('0.00')),
                      '年回款完成比例': decimal.Decimal(year_back_percent).quantize(decimal.Decimal('0.00')),
                      '月回款完成比例': decimal.Decimal(month_back_percent).quantize(decimal.Decimal('0.00')),
                      '年邀约完成比例': decimal.Decimal(year_invite_percent).quantize(decimal.Decimal('0.00')),
                      '月邀约完成比例': decimal.Decimal(month_invte_percent).quantize(decimal.Decimal('0.00'))
                      }
                    result.append(re)
        print(result)
        return {'result':result,'date_start':time_start,'date_end':time_end} 

