from odoo import fields, models


class SalesPersonCode(models.Model):
    """ Created for salesman code"""
    _name = 'sale.person.code'
    _description = 'Salesman Code'
    _rec_name = 'salesperson_code'

    salesperson = fields.Many2one('res.users', string='Salesman')
    salesperson_code = fields.Char(string='Code')
    salesperson_team = fields.Many2one('crm.team', string='Salesman Team')
