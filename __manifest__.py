# -*- coding: utf-8 -*-
{
    'name': "base_group",

    'summary': """ 市场营销人员参与CRM使用的权限相关配置""",

    'description': """
        1.增加了市场专员和市场经理两个组
        2.市场营销人员只能创建线索无法跟进商机，无法将线索转换成商机
        3.市场营销人员无法看到所有的客户联系方式
    """,

    'author': "Jerry Ling",
    'website': "http://www.isoftino.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','hr','sale','board','sale_management'],

    # always loaded
    'data': [
        #'views/templates.xml',
        'security/groups.xml',
        'security/rules.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/views.xml',
        'wizard/excel_import_wizard.xml',
        'wizard/import_batch.xml',
        #'wizard/batch_source_line.xml',
        'wizard/import_log.xml',
        'wizard/lead_duplicate.xml',
        'report/report_view.xml',
        'report/lead_report_wizard.xml',
        'report/lead_report_template.xml',
        'report/opportunity_report_template.xml',
        'demo/company_info.xml',
        'demo/tag.xml',
        'demo/utm_source.xml',
        'demo/users.xml',
        'demo/crm_depart.xml',
        'demo/crm_team.xml',
        'demo/department.xml',
        'demo/job.xml',
        'demo/stage.xml',
        'demo/employee.xml',
        'demo/depart.xml',
        'demo/users_employee.xml'

    ],
    'qweb':[
        'static/src/xml/*.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
