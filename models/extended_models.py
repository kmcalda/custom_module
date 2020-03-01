from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ContactsInherited(models.Model):
    _inherit = 'res.country.state'

    region_name = fields.Char(string='Region')


class ContactsRespartnerInherited(models.Model):
    _inherit = 'res.partner'

    region_contact = fields.Char(string='Region')

    @api.onchange('state_id')
    def onchange_value_state_id(self):
        for reg in self:
            reg.region_contact = reg.state_id.region_name

    @api.constrains('vat')
    def _check_value_len(self):
        for val in self:
            if val.vat.isdigit() != True:
                raise ValidationError("Error! Special characters are not allowed!")
            if len(val.vat) != 12:
                raise ValidationError("Error! TIN should be 12-digits!")

    # overriding create of res.partner
    @api.model
    def create(self, vals):
        res = super(ContactsRespartnerInherited, self).create(vals)
        # code inside
        return res

    _sql_constraints = [
        ('ref_unique', 'unique(ref)',
         'Error! Reference already exist'),

        ('vat_unique', 'unique(vat)',
         'Error! TIN already exist'),
    ]


class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [
        ('default_code_unique', 'unique(default_code)',
         'Error! Internal reference already exist'),
    ]
