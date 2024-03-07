from odoo.tests.common import TransactionCase

class TestMaterial(TransactionCase):

    def setUp(self):
        super(TestMaterial, self).setUp()
        self.env = self.env(user=self.env.ref('base.user_admin'))

    def test_method_create(self):
        partner_id = self.env['res.partner'].create({'name': 'Customer Test 1'})
        record = self.env['test.material'].create({
            'name': 'Test Record',
            'buy_price': 1000,
            'code': 'A001',
            'type': 'fabric',
            'related_supplier': partner_id.id
        })

        self.assertEqual(record.code, 'A001')
        self.assertEqual(record.buy_price, 1000)