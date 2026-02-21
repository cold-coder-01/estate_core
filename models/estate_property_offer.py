from odoo import fields, models, api
from datetime import timedelta
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
    def action_accept(self):
        for record in self:
            # Check if an offer is already accepted for this property
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                raise UserError("Only one offer can be accepted for a given property!")
            
            record.status = "accepted"
            # Update the parent property using the Many2one relation
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    # This field links back to your main property model
    property_id = fields.Many2one("estate.properties", string="Property", required=True)
    validity= fields.Integer(string="Validity (days)", default=7)
    date_deadline= fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            # Fallback to today if create_date isn't set yet (for new records)
            start_date= record.create_date.date()if record.create_date else fields.Date.today()
            record.date_deadline = start_date + timedelta(days=record.validity)
    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            # Calculate the difference in days when the user manually picks a date
            if record.date_deadline:
                record.validity = (record.date_deadline - start_date).days
            else:
                record.validity = 7
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The offer price must be strictly positive."
        ),
    ]   #ensure that any offer made has a price grater than zero