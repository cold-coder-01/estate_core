from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Property type"
    _order="sequence, name"

    name= fields.Char(string="Name", required= True)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    sequence = fields.Integer(string="Sequence", default=1, help="Used to order stages. Lower is better.")
    # Inline list of properties belonging to this type
    property_ids = fields.One2many("estate.properties", "property_type_id", string="Properties")
    _sql_constraints = [
    ("check_name", "UNIQUE(name)", "The property type name must be unique.")
]

