from odoo import fields, models, api
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
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Orientation"
    )
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
    