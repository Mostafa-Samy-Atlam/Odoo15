from odoo import models, fields


class HmsDepartment(models.Model):
    _name = "hms.department"
    _description = "HMS Departments"
    # _log_access = False to avoid self created columns
    # _rec_name = "Field thar will act as name"

    # To make my table appear I need a menu Item and Action
    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patients_id = fields.One2many("hms.patient", "department_id")
