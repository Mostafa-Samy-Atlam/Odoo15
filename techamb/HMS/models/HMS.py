from odoo import models, fields, api
from odoo.fields import Many2one
from odoo.exceptions import UserError, ValidationError
import re
import datetime
from datetime import date
import time
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class HmsPatient(models.Model):
    _name = "hms.patient"
    _description = "menus to view/create patients"
    _rec_name = "first_name"
    # _log_access = False

    # To make my table appear I need a menu Item and Action
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    email = fields.Char()
    birth_date = fields.Date()
    pcr = fields.Boolean()
    cr_ratio = fields.Float()
    age = fields.Integer(compute="calc_age", store=True)
    compute_age = fields.Char()
    image = fields.Binary()  # Upload Image
    address = fields.Text()
    history = fields.Html()
    blood_type = fields.Selection([
        ("A+", "Positive A"),
        ("A-", "Negative A"),
        ("B+", "Positive B"),
        ("B-", "Negative B"),
        ("AB+", "Positive AB"),
        ("AB-", "Negative AB"),
        ("O+", "Positive O"),
        ("O-", "Negative O"),
    ])
    state = fields.Selection([
        ("Undetermined", "Undetermined"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Serious", "Serious"),
    ], default='Undetermined')
    department_id = fields.Many2one('hms.department')
    dept_open = fields.Boolean(related="department_id.is_opened")
    doctor_id = fields.Many2many("hms.doctor")
    log_history = fields.One2many("hms.log.history", "patient_id")
    department_capacity = fields.Integer(related="department_id.capacity")

    def change_state(self):
        if self.state == 'Undetermined':
            self.state = 'Good'
        elif self.state == 'Good':
            self.state = 'Fair'
        elif self.state == 'Fair':
            self.state = 'Serious'
        self.env['hms.log.history'].create({
            "description": f"state changed to {self.state}",
        })

    def reset_state(self):
        self.state = 'Undetermined'

    @api.onchange("dept_open")
    def onchange_open(self):
        if not self.dept_open:
            return {
                'domain': {
                    'department_id': ''
                },
                'warning': {
                    "title": "Warning Message",
                    "message": "Closed Department"
                }
            }

    @api.onchange("age")
    def onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    "title": "Warning Message",
                    "message": "PCR has been checked"
                }
            }

    @api.constrains("email")
    def _validate_email(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, self.email):
            raise ValidationError("Wrong Format for Email")

    _sql_constraints = [('duplicate_name', 'UNIQUE(email)', 'Email already exists')]

    @api.depends("birth_date")
    def calc_age(self):
        for rec in self:
            if rec.birth_date:
                diff = fields.Date.today() - rec.birth_date
                rec.age = diff.days // 365
            else:
                print("error")


class LogHistory(models.Model):
    _name = "hms.log.history"
    description = fields.Text()
    patient_id = fields.Many2one("hms.patient")