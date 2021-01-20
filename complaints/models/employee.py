from odoo import models, fields, api, exceptions


class Employee(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee"

    complaints_id = fields.One2many('complaints.complaint', 'employee_id', string="Complaints")

    complaints_count = fields.Integer(
        string="complaints count", compute='_get_complaints_count')

    def _get_complaints_count(self):
        count = len(self.complaints_id)
        self.complaints_count = count

    def complaint_tree(self):
        return {
            'name': 'complaint.form',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'complaints.complaint',
            'type': 'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id)]
        }

