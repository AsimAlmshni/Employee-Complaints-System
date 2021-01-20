import simplejson as simplejson
from ebaysdk import exception

from odoo import models, fields, api, exceptions
from datetime import date
from lxml import etree
import json


class Complaint(models.Model):
    _name = 'complaints.complaint'
    _description = "Employee complaint"


    issue = fields.Text(string="Issue")
    action_taken_from_company = fields.Text(string="Action Taken From Company")
    date = fields.Date(string="ComplementDate", default=fields.Date.today)
    resolved_date = fields.Date(string="Resolved Date", readonly=True)
    has_effect_on_work = fields.Boolean(string="Does it have effect on Work")
    has_financial_effect = fields.Boolean(string="Does it has Financial Effect")
    color = fields.Integer()

    complaints_count = fields.Integer(
        string="complaints count", compute='_get_complaints_count')

    status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ], string="Status", default='pending', track_visibility='onchange', copy=False)


    complaint_id = fields.Many2one('complaints.type', string="Complaint Type")
    employee_id = fields.Many2one('hr.employee', string="Employee")

    department_id = fields.Many2one('hr.department', string="Department")

    @api.depends('complaints_count')
    def _get_complaints_count(self):
        for r in self:
            r.complaints_count = len(r.status)

    @api.constrains('date', 'resolved_date')
    def _check_complaint_date_greater_than_resolved_date(self):
        for r in self:
            if r.resolved_date != False:
                if r.date > r.resolved_date:
                    raise exceptions.ValidationError("the resolved date cannot be less than complaint date")



    def in_progress_action(self):
        if self.status == 'pending':
            self.status = "in_progress"
        else:
            raise exceptions.ValidationError("the status must be Pending to change to In Progress")

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
    #     context = self._context
    #     view_id = self.env.ref('complaints.complaint_form_view').id
    #     res = super(Complaint, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #
    #     print("view_id::::",view_id)
    #     print("testing before")
    #     print(context.get('turn_view_readonly'))
    #     if context.get('turn_view_readonly'):  # Check for context value
    #         doc = etree.XML(res['arch'])
    #
    #         if view_type == 'form':            # Applies only for form view
    #             for node in doc.xpath("//field"):   # All the view fields to readonly
    #                 node.set('readonly', 'True')
    #                 node_values = node.get('modifiers')
    #                 modifiers = json.loads(node_values)
    #                 modifiers['readonly'] = True
    #                 node.set('modifiers', simplejson.dumps(modifiers))
    #             res['arch'] = etree.tostring(doc)
    #         print(res)
    #     return res

    def resolve_action(self):
        if self.status == 'in_progress':
            self.status = "resolved"
            self.resolved_date = date.today()
            #self.fields_view_get(self)
        else:
            raise exceptions.ValidationError("the status must be In Progress to change to Resolved")

    @api.onchange('department_id')
    def _onchange_department(self):
        for rec in self:
            return {'domain': {'employee_id': [('department_id', '=', rec.department_id.id)]}}

    def set_resolved_status(self):
        for cmplnt in self:
            if cmplnt.status == "resolved":
                raise exceptions.ValidationError("the selected status must be In Progress or pending to change to Resolved")
        for cmplnt in self:
            cmplnt.status = "resolved"
            cmplnt.resolved_date = date.today()

    def complaint_create(self):
        print(self.id)
        return {
            'name': 'complaint.form',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'view_id': False,
            'res_model': 'complaints.complaint',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': []
        }






