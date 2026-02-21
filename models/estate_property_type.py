from odoo import models, fields

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Property type"
    _order="sequence, name"

    name= fields.Char(string="Name", required= True)
    sequence = fields.Integer(string="Sequence", default=1, help="Used to order stages. Lower is better.")
    # Inline list of properties belonging to this type
    property_ids = fields.One2many("estate.properties", "property_type_id", string="Properties")
    _sql_constraints = [
    ("check_name", "UNIQUE(name)", "The property type name must be unique.")
]

