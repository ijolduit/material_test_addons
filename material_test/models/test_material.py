from odoo import _,fields,api,models
from datetime import datetime
from odoo.exceptions import ValidationError

class TestMaterial(models.Model):
    _name = 'test.material'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    type = fields.Selection([('fabric','Fabric'),('jeans','Jeans'),('cotton','Cotton')], required=True)
    buy_price = fields.Float('Buy Price', required=True)
    related_supplier = fields.Many2one('res.partner', string="Related Supplier", required=True)

    @api.constrains('buy_price')
    def _check_minimum_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError('Buy Price must greater than 100')

