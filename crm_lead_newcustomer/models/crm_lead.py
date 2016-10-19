# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, api


class Lead(models.Model):
    _inherit = 'crm.lead'

    @api.one
    def create_partner_assignation(self):
        data = {
            'name': self.contact_name,
            'user_id': self.user_id.id,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email_from or False,
            'fax': self.fax,
            'title': self.title and self.title.id or False,
            'street': self.street,
            'street2': self.street2,
            'zip': self.zip,
            'city': self.city,
            'country_id': self.country_id and self.country_id.id or False,
            'state_id': self.state_id and self.state_id.id or False,
            'type': 'contact'
        }

        if self.partner_name:
            data['name'] = self.partner_name
            data['is_company'] = True
            company = self.env['res.partner'].create(data)
            data['parent_id'] = company.id
            data['name'] = self.contact_name
            data['use_parent_address'] = True
            data['is_company'] = False

        client = self.env['res.partner'].create(data)
        self.partner_id = client
