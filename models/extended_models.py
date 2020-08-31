from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.misc import formatLang, get_lang
import base64


class ContactsInherited(models.Model):
    _inherit = 'res.country.state'

    region_name = fields.Char(string='Region')


class ContactsRespartnerInherited(models.Model):
    _inherit = 'res.partner'

    region_contact = fields.Char(string='Region')
    payable_options = fields.Selection([('vat', 'VAT'), ('non', 'NON VAT')], string='Payable Option', default=False)

    @api.onchange('state_id')
    def onchange_value_state_id(self):
        """
        Execute on-change of state-id
        This will update region_contact

        :return: string
        """
        for reg in self:
            reg.region_contact = reg.state_id.region_name

    @api.constrains('region_contact')
    def check_region_contact_validity(self):
        """
        This will make sure that the region should be the appropriate region to be for the city

        :return: string
        """
        for reg_cont in self:
            if reg_cont.region_contact != reg_cont.state_id.region_name:
                raise ValidationError("Error! You're not allowed to change the Region!")

    @api.constrains('vat')
    def _check_value_len(self):
        """
        This will alert the user if the field did not meet the requirements

        :return: integer
        """
        for val in self:
            if val.vat:
                if not val.vat.isdigit():
                    raise ValidationError("Error! Special characters are not allowed!")
                if len(val.vat) != 12:
                    raise ValidationError("Error! TIN should be 12-digit!")

    # check if the ref and vat is unique, else throw an error
    _sql_constraints = [
        ('ref_unique', 'unique(ref)',
         'Error! Reference already exist'),

        ('vat_unique', 'unique(vat)',
         'Error! TIN already exist'),
    ]


class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    # check if the default_code is unique, else throw error!
    _sql_constraints = [
        ('default_code_unique', 'unique(default_code)',
         'Error! Internal reference already exist'),
    ]


class SalesOrderCustom(models.Model):
    _inherit = 'sale.order'

    def _default_code(self):
        return self.env['sale.person.code'].search([('salesperson', '=', self.env.user.id)], limit=1).id

    state = fields.Selection(selection_add=[('sent', 'Review Sent')])
    salesperson_code = fields.Many2one('sale.person.code', string='Salesman Code', default=_default_code)

    # @api.onchange('user_id')
    # def _user_code(self):
    #     for rec in self:
    #         return {'domain':{'salesperson_code':[('salesperson','=', rec.user_id.id)]}}

    def _add_to_nav(self):
        """

        :return: test function
        """
        self.ensure_one()
        data = ""
        data += "Order,H,%s,%s,%s,%s,%s,FG_LMS_MAI,%s,,,%s,, ,%s,%d\n" % (
            self.partner_id.ref if self.partner_id.ref else "customer code", self.payment_term_id.name, self.name,
            self.commitment_date if self.commitment_date else self.expected_date.strftime("%m/%d/%Y"), "salesman code",
            self.partner_id.street, self.partner_id.street2 if self.partner_id.street2 else "address 2",
            self.date_order.strftime("%m/%d/%Y"), 0)
        for num, rec in enumerate(self.order_line):
            data += ",L,,,%s,,,,,,,,,,,,,Item,%s,%d,%s,%d,%d,%d\n" % (
                self.name, rec.product_id.default_code,
                rec.product_uom_qty, rec.product_uom.name,
                rec.price_unit, rec.discount, num + 1)

        data_record = base64.encodebytes(data.encode())
        ir_values = {
            'name': "SALESORDER_%s.csv" % self.name,
            'res_model': self._name,
            'res_id': self.id,
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'text/csv',
        }
        data_id = self.env['ir.attachment'].create(ir_values)
        template_id = self.env.ref('custom_module.email_template_test_send').id
        template = self.env['mail.template'].browse(template_id)
        template.attachment_ids = [(6, 0, [data_id.id])]
        template.send_mail(self.id, force_send=True)
        template.attachment_ids = [(3, data_id.id)]

    def email_review(self):
        """

        :return: test function for "send for review" button
        """
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('custom_module', 'email_template_review_sale')[1]
        except ValueError:
            template_id = False

        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True
        }

        print(ctx)
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'name': 'Send Email',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    # override confirm button (sales order)
    def action_confirm(self):
        """

        :return:
        """
        record = super(SalesOrderCustom, self).action_confirm()
        self._add_to_nav()
        return record


class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_packaging_qty = fields.Float('Package Quantity')

    # overide product_packaging method
    def _check_package(self):
        default_uom = self.product_id.uom_id
        pack = self.product_packaging
        qty = self.product_uom_qty
        q = default_uom._compute_quantity(pack.qty, self.product_uom)
        if qty and q and (qty % q):
            newqty = qty - (qty % q) + q
            self.product_uom_qty = newqty * self.product_packaging_qty
        return {}

    # update the unit quantity onchange of package quantity
    @api.onchange('product_packaging_qty')
    def _product_packaging_qty_calc(self):
        if self.product_packaging:
            self.product_uom_qty = self.product_packaging_qty * self.product_packaging.qty
            return {}

    # override onchange for payable option
    @api.onchange('product_id')
    def product_id_change(self):
        customer_id = self._context.get('partner_id')
        customer_option = self.env['res.partner'].search([('id', '=', customer_id)]).payable_options
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        if customer_option == 'vat':
            self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False

        return result

