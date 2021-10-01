from odoo import models, fields, api


# Adding field for invoice.move.line
class CustomAccountInvoice(models.Model):
    """ Inherit account.move.line to add fields and function"""
    _inherit = "account.move.line"

    product_packaging_qty = fields.Float(
        string='Package Quantity', descriptio="Field for packaging qty", store=True)
    product_packaging = fields.Many2one('product.packaging', string='Package', default=False, check_company=True,
                                        store=True, use_parent_address=False)

    @api.onchange('product_packaging_qty')
    def _product_packaging_qty_calc(self):
        """
        Multiple the product_packaging_qty and product_packaging.qty
        :return:
        """
        for v in self:
            if v.product_packaging:
                v.quantity = v.product_packaging_qty * v.product_packaging.qty
