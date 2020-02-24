from odoo import models, fields, api


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

    _sql_constraints = [
        ('ref_unique', 'unique(ref)',
         'Error! Reference already exist'),

        ('vat_unique', 'unique(vat)',
         'Error! TIN already exist')
    ]


class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [
        ('default_code_unique', 'unique(default_code)',
         'Error! Internal reference already exist'),
        ]