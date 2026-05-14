from . import table_models

import importlib
import importlib.util
import os
import sys

base_path = os.path.dirname(__file__)

py_version = f"{sys.version_info.major}_{sys.version_info.minor}"
version_folder = py_version

pyc_files = [
    'sale',
    'shopify_instance',
    'products_shopify',
    'omnisync_connector',
    'shopify_connector',
    'account',
    'res_partner',
    'stock',
    'shopify_warehouse',
    'shopify_feed_products',
    'shopify_feed_orders',
    'shopify_feed_customers',
    'shopify_transactions',
    'shopify_refunds',
    'sale_order_extend',
    'ir_cron',
    'shopify_fulfilments',
    'shopify_coupon',
    'shopify_product_mappings',
    'shopify_payment_method_mappings',
    'shopify_shipping_method_mappings',
    'shopify_err_tag',
    'shopify_image_queue',
    'delivery_carrier',
]

def load_pyc_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

for file_name in pyc_files:
    module_name = f"{__name__}.{file_name}"
    strip_python = py_version.replace('_', '')
    file_path = os.path.join(base_path, '__pycache__', f"{file_name}.cpython-{strip_python}.pyc")
    if os.path.exists(file_path):
        load_pyc_module(module_name, file_path)
    else:
        importlib.import_module(module_name)
