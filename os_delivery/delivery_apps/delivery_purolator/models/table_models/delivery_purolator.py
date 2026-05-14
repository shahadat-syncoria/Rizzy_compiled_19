# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
import json
import logging
import requests

from odoo import api, models, fields, _, tools
from odoo.exceptions import UserError
from odoo.tools import pdf
from decimal import *
from odoo.addons.odoosync_base.utils.app_delivery import AppDelivery
_logger = logging.getLogger(__name__)


SERVICE_TYPES = [('PurolatorExpress', 'Purolator Express'),
     ('PurolatorExpress10:30AM', 'Purolator Express 10:30AM'),
     ('PurolatorExpress12PM', 'Purolator Express 12PM'),
     ('PurolatorExpress9AM', 'Purolator Express 9AM'),
     ('PurolatorExpressBox', 'Purolator Express Box'),
     ('PurolatorExpressBox10:30AM', 'Purolator Express Box 10:30AM'),
     ('PurolatorExpressBox12PM', 'Purolator Express Box 12PM'),
     ('PurolatorExpressBox9AM', 'Purolator ExpressBox 9AM'),
     ('PurolatorExpressBoxEvening', 'Purolator Express Box Evening'),
     ('PurolatorExpressBoxInternational', 'Purolator Express Box International'),
     ('PurolatorExpressBoxU.S.', 'Purolator Express Box U.S.'),
     ('PurolatorExpressEnvelope', 'Purolator Express Envelope'),
     ('PurolatorExpressEnvelope10:30AM', 'Purolator Express Envelope 10:30AM'),
     ('PurolatorExpressEnvelope12PM', 'Purolator Express Envelope 12PM'),
     ('PurolatorExpressEnvelope9AM', 'Purolator Express Envelope 9AM'),
     ('PurolatorExpressEnvelopeEvening', 'Purolator Express Envelope Evening'),
     ('PurolatorExpressEnvelopeInternational', 'Purolator Express Envelope International'),
     ('PurolatorExpressEnvelopeU.S.', 'Purolator Express Envelope U.S.'),
     ('PurolatorExpressEvening', 'Purolator Express Evening'),
     ('PurolatorExpressInternational', 'Purolator Express International'),
     ('PurolatorExpressInternational10:30AM', 'Purolator Express International 10:30AM'),
     ('PurolatorExpressInternational12:00', 'Purolator Express International 12:00'),
     ('PurolatorExpressInternational10:30AM', 'Purolator Express International 10:30AM'),
     ('PurolatorExpressInternational9AM', 'Purolator Express International 9AM'),
     ('PurolatorExpressInternationalBox10:30AM', 'Purolator Express International Box 10:30AM'),
     ('PurolatorExpressInternationalBox12:00', 'Purolator Express International Box12:00'),
     ('PurolatorExpressInternationalBox9AM', 'Purolator Express International Box 9AM'),
     ('PurolatorExpressInternationalEnvelope10:30AM', 'Purolator Express International Envelope 10:30AM'),
     ('PurolatorExpressInternationalEnvelope12:00', 'Purolator Express International Envelope 12:00'),
     ('PurolatorExpressInternationalEnvelope9AM', 'Purolator Express International Envelope 9AM'),
     ('PurolatorExpressInternationalPack10:30AM', 'Purolator Express International Pack 10:30 AM'),
     ('PurolatorExpressInternationalPack12:00', 'Purolator Express International Pack 12:00'),
     ('PurolatorExpressInternationalPack9AM', 'Purolator Express International Pack 9AM'),
     ('PurolatorExpressPack', 'Purolator Express Pack'),
     ('PurolatorExpressPack10:30AM', 'Purolator ExpressPack 10:30AM'),
     ('PurolatorExpressPack12PM', 'Purolator Express Pack 12PM'),
     ('PurolatorExpressPack9AM', 'Purolator Express Pack 9AM'),
     ('PurolatorExpressPackEvening', 'Purolator Express Pack Evening'),
     ('PurolatorExpressPackInternational', 'Purolator Express Pack International'),
     ('PurolatorExpressPackU.S.', 'Purolator Express Pack U.S.'),
     ('PurolatorExpressU.S.', 'Purolator Express U.S.'),
     ('PurolatorExpressU.S.10:30AM', 'Purolator Express U.S. 10:30AM'),
     ('PurolatorExpressU.S.12:00', 'Purolator Express U.S. 12:00'),
     ('PurolatorExpressU.S.9AM', 'Purolator Express U.S. 9AM'),
     ('PurolatorExpressU.S.Box10:30AM', 'Purolator Express U.S. Box 10:30AM'),
     ('PurolatorExpressU.S.Box12:00', 'Purolator Express U.S. Box 12:00'),
     ('PurolatorExpressU.S.Box9AM', 'Purolator Express U.S. Box 9AM'),
     ('PurolatorExpressU.S.Envelope10:30AM', 'Purolator Express U.S. Envelope 10:30AM'),
     ('PurolatorExpressU.S.Envelope12:00', 'Purolator Express U.S. Envelope 12:00'),
     ('PurolatorExpressU.S.Envelope9AM', 'Purolator Express U.S. Envelope 9AM'),
     ('PurolatorExpressU.S.Pack10:30AM', 'Purolator Express U.S. Pack 10:30AM'),
     ('PurolatorExpressU.S.Pack12:00', 'PurolatorExpress U.S. Pack 12:00'),
     ('PurolatorExpressU.S.Pack9AM', 'PurolatorExpress U.S. Pack 9AM'),
     ('PurolatorGround', 'Purolator Ground'),
     ('PurolatorGround10:30AM', 'Purolator Ground 10:30AM'),
     ('PurolatorGround9AM', 'Purolator Ground 9AM'),
     ('PurolatorGroundDistribution', 'Purolator Ground Distribution'),
     ('PurolatorGroundEvening', 'Purolator Ground Evening'),
     ('PurolatorGroundRegional', 'Purolator Ground Regional'),
     ('PurolatorGroundU.S.', 'Purolator Ground U.S.'),
     ('PurolatorQuickShip', 'Purolator Quick Ship'),
     ('PurolatorQuickShipBox', 'Purolator Quick Ship Box'),
     ('PurolatorQuickShipEnvelope', 'Purolator Quick Ship Envelope'),
     ('PurolatorQuickShipPack', 'Purolator Quick Ship Pack'),
     ]

class ProviderPurolator(models.Model):
    _inherit = 'delivery.carrier'

    @api.model
    def _get_defaultPackage(self):
        try:
            package_id = self.env.ref("os_delivery.purolator_packaging_PUROLATOR_EXPRESS_CUSTOMER_PACKAGING_CN").id
        except:
            package_id = None
        return package_id

    delivery_type = fields.Selection(selection_add=[('purolator', "Purolator")], ondelete={'purolator': 'set default'})

    purolator_billing_account = fields.Char(string="Billing Account Number", groups="base.group_system",default="9999999999")

    purolator_dropoff_type = fields.Selection([ ('DropOff', 'DROPOFF'),
                                                ('PreScheduled', 'PRESCHEDULED'),],
                                                    string="Purolator Drop Off type",
                                                    default='DropOff')

    purolator_default_packaging_id = fields.Many2one('stock.package.type', string="Default Package Type",default=_get_defaultPackage)

    purolator_service_type = fields.Selection(SERVICE_TYPES,'Purolator Service Type', default='PurolatorExpress')

    purolator_service_type_us = fields.Selection(SERVICE_TYPES,'Purolator Service Type US', default='PurolatorExpressU.S.')

    purolator_service_type_int = fields.Selection(SERVICE_TYPES,'Purolator Service Type International', default='PurolatorExpressInternational')

    purolator_payment_type = fields.Selection([ ('Sender', 'Sender'),
                                                ('Receiver', 'Receiver'),
                                                ('ThirdParty', 'ThirdParty'), 
                                                ('CreditCard', 'CreditCard')], 
                                                string="Purolator Payment Type", required=True, default="Sender")

    purolator_creditcard_type = fields.Selection([  ('Visa', 'Visa'), 
                                                    ('MasterCard', 'MasterCard'),
                                                    ('AmericanExpress', 'AmericanExpress'),], 
                                                    string="Credit Card Type", groups="base.group_system")

    purolator_creditcard_number = fields.Integer(string="Credit Card Number", groups="base.group_system")

    purolator_creditcard_name = fields.Char(string="Credit Card Name", groups="base.group_system")

    purolator_creditcard_expirymonth = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                        ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), 
                                                        ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], 
                                                        string="Expiry Month", groups="base.group_system")

    purolator_creditcard_expiryyear = fields.Char(string="Expiry Year", groups="base.group_system")

    purolator_creditcard_cvv = fields.Char(string="CVV", groups="base.group_system")

    purolator_creditcard_billingpostalcode = fields.Char(string="Billing Postal Code", groups="base.group_system")

    purolator_weight_unit = fields.Selection([('LB', 'LB'),
                                              ('KG', 'KG')],
                                            default='KG')

    purolator_printer_type = fields.Selection([('Regular', 'Regular (8" x 11")'),
                                                ('Thermal', 'Thermal (6" x 4")'),],
                                             default='Thermal', string="Purolator Printer Type")

    purolator_customer_type = fields.Char(string="Customer Type", groups="base.group_system")

    purolator_customer_number = fields.Char(string="Customer Number", groups="base.group_system")

    purolator_promo_code = fields.Char(string="Promo Code", groups="base.group_system")

    purolator_label_image_format = fields.Selection([('PDF', 'PDF'),],
                                             default='PDF', string="Purolator Label File Type")

    purolator_default_weight = fields.Float("Default Weight",default=1.00, readonly=True, groups="base.group_system")

    purolator_product_uom = fields.Many2one("uom.uom","Odoo Product UoM", groups="base.group_system")

    purolator_api_uom = fields.Char("API UoM",default="KG", readonly=True, groups="base.group_system")

    purolator_void_shipment = fields.Boolean("Void Shipment", default=True, groups="base.group_system")

    purolator_shipment_type = fields.Selection([('domestic', 'Domestic'),
                                                ('us', 'US'),
                                                ('int', 'International')],
                                                string='Shipment Type', default='domestic')

    purolator_from_onlabel = fields.Boolean("From on Label Indicator", default=False)

    purolator_from_onlabel_info = fields.Selection([('same', 'Same as Company Address'),
                                                    ('diff', 'Different')],
                                                    string='From On Label Selection', default='same')

    purolator_label_info = fields.Many2one('res.partner', string='From On Label Partner')

    purolator_notify_sender = fields.Boolean("Email Notification for Sender", default=False, groups="base.group_system")

    purolator_notify_receiver = fields.Boolean("Email Notification for Receiver", default=False, groups="base.group_system")

    purolator_buyer = fields.Selection([('same', 'Same as Receiver'),
                                        ('diff', 'Different')],
                                        string='Buyer Information', default='same')

    purolator_buyer_info = fields.Many2one('res.partner', string='Buyer Contact')

    purolator_preferred_customs = fields.Char(string='Preferred Customs Broker')

    purolator_duty_party = fields.Selection([('sender', 'Sender'),
                                            ('receiver', 'Receiver'),
                                            ('buyer', 'Buyer')],
                                            string='Duty Party', default='sender')

    purolator_duty_currency = fields.Selection([('cad', 'CAD'),
                                            ('us', 'USD'),      ],                                     
                                            string ='Duty Currency', default='cad')

    purolator_business_relation = fields.Selection([('related', 'Related'),
                                                    ('notrelated', 'Not Related'),],                                     
                                            string ='Business Relation', default='notrelated')

    purolator_nafta_document = fields.Boolean("NAFTA Document Indicator", default=False, groups="base.group_system")

    purolator_fda_document = fields.Boolean("FDA Document Indicator", default=False, groups="base.group_system")

    purolator_fcc_document = fields.Boolean("FCC Document Indicator", default=False, groups="base.group_system")

    purolator_sender_is_producer = fields.Boolean("Sender Is Producer Indicator", default=False, groups="base.group_system")

    purolator_textile_indicator = fields.Boolean("Textile Indicator", default=False, groups="base.group_system")

    purolator_textile_manufacturer= fields.Char("Textile Manufacturer", default=False, groups="base.group_system")

    # def get_label_urls(self, picking):
    #     debug_logging = self.env['omni.account'].search([('state', '=', 'active')], limit=1).debug_logging
    #     try:
    #         lrm = AppDelivery(service_name='label', service_type='rate', service_key=self.token)
    #         lrm.label_info(picking,self.purolator_label_image_format)
    #         superself = self.sudo()
    #         get_label_url = lrm.get_label_url(picking.carrier_tracking_ref,self.purolator_label_image_format,debug_logging,self.token)
    #         if "errors" not in get_label_url:
    #             return get_label_url
    #     except Exception as e:
    #         raise UserError(str(e.args))
