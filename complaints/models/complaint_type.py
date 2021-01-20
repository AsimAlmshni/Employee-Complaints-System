from odoo import models, fields, api, exceptions


class ComplaintType(models.Model):
    _name = 'complaints.type'
    _description = "complaint type"

    name = fields.Char(string="Complaint Title", required=True)
    code = fields.Integer(string="Complaint Code")