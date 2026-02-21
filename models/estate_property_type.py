from odoo import models, fields

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Property type"

    name= fields.Char(string="Name", required= True)
    _sql_constraints = [
    ("check_name", "UNIQUE(name)", "The property type name must be unique.")
]

