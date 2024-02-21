# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class AccountInvoicePurchaseSupplierTestCase(ModuleTestCase):
    "Test Account Invoice Purchase Supplier module"
    module = 'account_invoice_purchase_supplier'


del ModuleTestCase
