
# -*- coding: utf-8 -*-
# Part of sw-tech. See LICENSE file for full copyright and licensing details.

from odoo.tools.translate import _
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from odoo import tools, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import api, fields, models, _
import logging
from odoo.osv import  osv
from odoo import SUPERUSER_ID

class crm_lead(models.Model):
    """ CRM Lead Case """
    _inherit = "crm.lead"

    def task_count(self):
        task_obj = self.env['project.task']
        self.task_number = task_obj.search_count([('lead_id', 'in', [a.id for a in self])])

    task_number = fields.Integer(compute='task_count', string='Tasks')

class crm_task_wizard(models.TransientModel):
    _name = 'crm.task.wizard'
    _description = "CRM Task Wizard"
    
    def get_name(self):
        ctx = dict(self._context or {})
        active_id = ctx.get('active_id')
        crm_brw = self.env['crm.lead'].browse(active_id)
        name = crm_brw.name
        return name
    
    project_id = fields.Many2one('project.project', 'Project')
    dead_line = fields.Date('Deadline')
    name = fields.Char('Task Name', default=get_name)
    user_ids = fields.Many2many('res.users', 'Assignees', default=lambda self: self.env.uid, index=True)
    user_ids = fields.Many2many('res.users', relation='project_task_assignee_rel', column1='task_id', column2='user_id',
                                string='Assignees', default=lambda self: self.env.user)

    def create_task(self):
        ctx = dict(self._context or {})
        active_id = ctx.get('active_id')
        crm_brw = self.env['crm.lead'].browse(active_id)
        
        # Collect user ids
        user = [users.id for users in self.user_ids]

        # Get the sale_line_id from the related project
        sale_line_id = self.project_id.sale_line_id.id if self.project_id.sale_line_id else False

        # Prepare the values for task creation
        vals = {
            'name': self.name,
            'project_id': self.project_id.id or False,
            'user_ids': user or False,
            'date_deadline': self.dead_line or False,
            'partner_id': crm_brw.partner_id.id or False,
            'lead_id': crm_brw.id or False,
            'sale_line_id': sale_line_id  # Link the sale line from the project to the task
        }

        # Create the task
        self.env['project.task'].create(vals)

class project_Task(models.Model):
    _inherit = 'project.task'
    
    lead_id = fields.Many2one('crm.lead', 'Opportunity')
    sale_line_id = fields.Many2one('sale.order.line', string='Sale Order Item')  # New field for linking sale order line
