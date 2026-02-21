from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
class EstateProperties(models.Model):
    _name="estate.properties"
    _description="Real Estate Property"
   



    # Basic Fields from Chapter 3
    property_type_id= fields.Many2one("estate.property.type",string="Property Type")
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )
    tag_ids= fields.Many2many("estate.property.tag", string="Tags")
    # ... inside my EstateProperty class ...
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    name = fields.Char(required=True)
    description = fields.Html()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today())
    expected_price = fields.Float(required=True)
    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            # 1. Skip the check if selling price is zero (it's zero until an offer is accepted) remeber abel
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            limit_price = record.expected_price * 0.9
            if float_compare(record.selling_price, limit_price, precision_digits=2) == -1:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price! "
                    "Check your offers and expected price."
                )
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    # The decorator tells Odoo to recalculate whenever living_area or garden_area changes
    # because of the api it updates the data at real time
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price= fields.Float(string="Best Offer", compute="_compute_best_price")
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            # We use mapped to get a list of all prices from the related offers
            prices = record.offer_ids.mapped("price")
            # If there are prices, find the max; otherwise, set to 0.0
            record.best_price = max(prices) if prices else 0.0
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Orientation"
    )
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer-received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'canceled'),
        ]
        
    )
    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("A canceled property cannot be set as sold.")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be canceled.")
            record.state = "canceled"
        return True
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive."
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive."
        ),
    ]
  