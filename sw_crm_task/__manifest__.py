# -*- coding: utf-8 -*-
# Part of sw-tech. See LICENSE file for full copyright and licensing details.

{
    'name': 'Task from CRM Lead',
    'version': '17.0.1.0',
    'category': 'CRM',
    'license': 'LGPL-3',
    'summary': 'This module helps user to easily create a new task from crm lead.',
    'description': """
    Create Task button on Lead, Create Project Task from lead, CRM Lead to Project Task, Create Project Task from Lead, Create task from mail, create automatic task from lead, Generate a new task from lead.
""",
    'author': 'sw',
    'website': 'https://www.sw-tech.pro',
    'depends': ['base', 'crm', 'sale', 'project'],
    'data': [
            'security/ir.model.access.csv',
            'views/crm_lead_view.xml'
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'images':['static/description/Banner.gif'],
    'sequence': '-100',
    'price': '10.0',
    'currency': 'USD',
}

