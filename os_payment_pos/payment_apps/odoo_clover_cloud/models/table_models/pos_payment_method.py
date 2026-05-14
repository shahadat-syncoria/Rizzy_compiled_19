# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging
import json
import requests

_logger = logging.getLogger(__name__)

test_url = 'https://sandbox.dev.clover.com'
prod_url = 'https://www.clover.com'
regions = {
    'uscanada': 'https://www.clover.com',
    'europe': 'https://eu.clover.com',
}


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    clover_server_url = fields.Char(string='Clover Server URL',)

    clover_config_id = fields.Char(string='Clover Config Id',)

    clover_jwt_token = fields.Text(string='Clover JWT Token',)

    clover_merchant_id = fields.Char(string='Clover Merchant Id')

    clover_device_id = fields.Many2one(
        string='Device',
        comodel_name='clover.device',
        ondelete='restrict',
        # domain=lambda self: self._get_device(),
        help="To obtain the deviceId, you must first retrieve an accessToken and your merchantId. Press 'Get Device Id' button to get the Device Id."
    )

    clover_device_name = fields.Char(
        string='Device ID',
        compute='_compute_clover_device_name')

    @api.depends('clover_device_id')
    def _compute_clover_device_name(self):
        for record in self:
            record.clover_device_name = record.clover_device_id.serial

    clover_x_pos_id = fields.Char(
        string='X POS ID',
        compute='_compute_clover_x_pos_id')

    @api.depends('clover_device_id')
    def _compute_clover_x_pos_id(self):
        for record in self:
            record.clover_x_pos_id = ""
            if record.clover_device_id:
                record.clover_x_pos_id = record.clover_device_id.x_pos_id

    clover_log_ids = fields.One2many(
        string='Clover Logs',
        comodel_name='ir.logging',
        inverse_name='payment_method_id',
        domain=[('payment_method_id', '!=', False), ((
            'payment_method_id.use_payment_terminal', '=', 'clover_cloud'))]
    )

        
    # def send_welcome_message(self, values):
    #     if not self.clover_config_id or not self.clover_jwt_token or not self.clover_server_url:
    #         return {'success':False, 'description':'Config id or JWT Token or Server URL is missing'}

    #     URL = '%s/api/v1/show/welcome' % (self.clover_server_url)
    #     headers = self.get_headers(values)
    #     payload = {
    #         "configId": values.get('configId'),
    #         "deviceId": values.get('deviceId'),
    #         "posId": values.get('posId'),
    #     }

    #     response = requests.request("POST", URL, headers=headers, data=json.dumps(payload))

    #     _logger.info("URL ===>>>>{}".format(URL))
    #     _logger.info("headers ===>>>>{}".format(headers))
    #     _logger.info("payload ===>>>>{}".format(payload))
    #     _logger.info("response===>>>>" + str(response.text))

    #     if response.status_code == 200:
    #         return {
    #             'status_code' : response.status_code,
    #             'success': True,
    #             'description': 'Welcome Message sent Successfully',
    #             'action': 'welcome_message',
    #         }
    #     else:
    #         return {
    #             'status_code' : response.status_code,
    #             'success': False,
    #             'description': 'Welcome Message send failed!',
    #             'action': 'welcome_message',
    #         }

    # def send_thankyou_message(self, values):
    #     if not self.clover_config_id or not self.clover_jwt_token or not self.clover_server_url:
    #         return {'success':False, 'description':'Config id or JWT Token or Server URL is missing'}

    #     URL = '%s/api/v1/show/thank-you' % (self.clover_server_url)
    #     headers = self.get_headers(values)
    #     payload = {
    #         "configId": values.get('configId'),
    #         "deviceId": values.get('deviceId'),
    #         "posId": values.get('posId'),
    #     }

    #     response = requests.request("POST", URL, headers=headers, data=json.dumps(payload))

    #     _logger.info("URL ===>>>>{}".format(URL))
    #     _logger.info("headers ===>>>>{}".format(headers))
    #     _logger.info("payload ===>>>>{}".format(payload))
    #     _logger.info("response===>>>>" + str(response.text))

    #     if response.status_code == 200:
    #         return {
    #             'success': True,
    #             'description': 'Thankyou Message sent Successfully',
    #             'action': 'thankyou_message',
    #         }
    #     else:
    #         return {
    #             'success': False,
    #             'description': 'Thankyou Message send failed!',
    #             'action': 'thankyou_message',
    #         }

    # def send_payment_receipt(self, values):
    #     if not self.clover_config_id or not self.clover_jwt_token or not self.clover_server_url:
    #         return {'success':False, 'description':'Config id or JWT Token or Server URL is missing'}

    #     URL = '%s/api/v1/payments/%s/receipt/' % (self.clover_server_url, values.get('paymetId'))
    #     headers = self.get_headers(values)
    #     payload = {
    #         "configId": values.get('configId'),
    #         "deviceId": values.get('deviceId'),
    #         "posId": values.get('posId'),
    #     }

    #     response = requests.request("POST", URL, headers=headers, data=json.dumps(payload))

    #     _logger.info("URL ===>>>>{}".format(URL))
    #     _logger.info("headers ===>>>>{}".format(headers))
    #     _logger.info("payload ===>>>>{}".format(payload))
    #     _logger.info("response===>>>>" + str(response.text))

    #     if response.status_code == 200:
    #         return {
    #             'success': True,
    #             'description': 'Thankyou Message sent Successfully',
    #             'action': 'thankyou_message',
    #         }
    #     else:
    #         return {
    #             'success': False,
    #             'description': 'Thankyou Message send failed!',
    #             'action': 'thankyou_message',
    #         }

    # def send_payment_request(self, values):
    #     if not self.clover_config_id or not self.clover_jwt_token or not self.clover_server_url:
    #         return {'success':False, 'description':'Config id or JWT Token or Server URL is missing'}

    #     URL = '%s/api/v1/payments/%s/receipt/' % (self.clover_server_url, values.get('paymetId'))
    #     headers = self.get_headers(values)
    #     payload = {
    #         "configId": values.get('configId'),
    #         "deviceId": values.get('deviceId'),
    #         "posId": values.get('posId'),
    #     }

    #     response = requests.request("POST", URL, headers=headers, data=json.dumps(payload))

    #     _logger.info("URL ===>>>>{}".format(URL))
    #     _logger.info("headers ===>>>>{}".format(headers))
    #     _logger.info("payload ===>>>>{}".format(payload))
    #     _logger.info("response===>>>>" + str(response.text))

    #     if response.status_code == 200:
    #         return {
    #             'success': True,
    #             'description': 'Thankyou Message sent Successfully',
    #             'action': 'thankyou_message',
    #         }
    #     else:
    #         return {
    #             'success': False,
    #             'description': 'Thankyou Message send failed!',
    #             'action': 'thankyou_message',
    #         }
