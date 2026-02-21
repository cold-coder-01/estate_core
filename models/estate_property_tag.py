from odoo import fields, models

class PropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Property Tag"

    name= fields.Char(string="Name", required=True)
    _sql_constraints = [
    ("check_name", "UNIQUE(name)", "The property tag name must be unique.")
]   #for not to create duplicated name
    