# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, SUPERUSER_ID, _
import pdb
_logger = logging.getLogger(__name__)



class base_group(models.Model):
    
    _inherit = 'crm.lead'
    phone = fields.Char('Phone', track_visibility=False, track_sequence=5)
    dispatch_date = fields.Date(string='分条日期')
    department_id = fields.Many2one('hr.department', string="所属部门")
    batch_id = fields.Many2one('import.batch', string="导入批次")
    is_same_user = fields.Boolean(compute='_compute_first',string="same")
    depart_id = fields.Many2one('crm.depart', string="部门")
   
    def _compute_first (self):
        if self._uid == self.user_id.id:
            self.is_same_user = False
        else:
            self.is_same_user = True
        if self.env.user.has_group('base_group.sales_vp_group'):
            self.is_same_user = False
    
    @api.onchange('user_id')
    def _onchange_user_id(self):
        """ When changing the user, also set a team_id or restrict team id to the ones user_id is member of. """
        if self.user_id.sale_team_id:
            values = self._onchange_user_values(self.user_id.id)
            self.update(values)
        #data = {'department_id':self.env['hr.employee'].search([('user_id','=',self.user_id.id)]).department_id.id} 
        data = {'depart_id':self.team_id.depart_id.id} 
        self.update(data)

class custom_depart(models.Model):
    _name = 'crm.depart'
    name = fields.Char(string="部门名称")
    year_target = fields.Char(string="年签约目标")
    year_back_target = fields.Char(string="年回款目标")
    year_invite_target = fields.Char(string="年邀约目标")
    month_target = fields.Char(string="月签约目标")
    month_back_target = fields.Char(string="月回款目标")
    month_invite_target = fields.Char(string="月邀约目标")
    user_id = fields.Many2one('res.users', string="部门负责人")
    team_ids = fields.One2many('crm.team','depart_id',string="销售团队")
    #member_ids = fields.One2many('res.users',''

class custom_team(models.Model):
    _inherit = "crm.team"
    depart_id = fields.Many2one('crm.depart', string="所属部门")

class custom_user(models.Model):
    _inherit = 'res.users'
    employee_id = fields.Many2one('hr.employee',string='相关员工', ondelete='restrict', help='与这个用户相关的员工', auto_join=True)
   
    #创建用户自动创建员工
    #@api.model
    #def create(self, vals):
    #    res = super(custom_user, self).create(vals)
    #    res['employee_id'] = self.env['hr.employee'].create({'name': res['name'],'user_id': res['id']})
    #    return res

class custom_crm(models.Model):

    _inherit  = 'res.partner'
    
    @api.model
    def create(self, values):
        print(values)
        record = super(custom_crm, self).create(values)
        record['user_id'] = self._uid
        record['company_type'] = 'company'
        return record

