from odoo import models, fields


class Doctor(models.Model):
    _name = "hms.doctor"
    _description = "HMS Doctors"
    # _log_access = False to avoid self created columns
    _rec_name = "first_name"

    # To make my table appear I need a menu Item and Action
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Binary()
