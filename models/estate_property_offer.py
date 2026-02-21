from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    # This field links back to your main property model
    property_id = fields.Many2one("estate.properties", string="Property", required=True)