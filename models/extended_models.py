from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ContactsInherited(models.Model):
    _inherit = 'res.country.state'

    region_name = fields.Char(string='Region')


class ContactsRespartnerInherited(models.Model):
    _inherit = 'res.partner'

    region_contact = fields.Char(string='Region')

    # assign region_name to region_contact base on state_id
    @api.onchange('state_id')
    def onchange_value_state_id(self):
        for reg in self:
            reg.region_contact = reg.state_id.region_name

    # alert user to NOT change the region
    @api.constrains('region_contact')
    def check_region_contact_validity(self):
        for reg_cont in self:
            if reg_cont.region_contact != reg_cont.state_id.region_name:
                raise ValidationError("Error! You're not allowed to change the Region!")

    # alert user to put 12-digits only without special characters
    @api.constrains('vat')
    def _check_value_len(self):
        for val in self:
            if not val.vat.isdigit():
                raise ValidationError("Error! Special characters are not allowed!")
            if len(val.vat) != 12:
                raise ValidationError("Error! TIN should be 12-digits!")

    # field ref and vat unique
    _sql_constraints = [
        ('ref_unique', 'unique(ref)',
         'Error! Reference already exist'),

        ('vat_unique', 'unique(vat)',
         'Error! TIN already exist'),
    ]


class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    # field default_code unique
    _sql_constraints = [
        ('default_code_unique', 'unique(default_code)',
         'Error! Internal reference already exist'),
    ]
