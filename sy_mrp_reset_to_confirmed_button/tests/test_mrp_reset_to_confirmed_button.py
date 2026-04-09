# Copyright 2026 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMrpResetToConfirmedButton(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mrp_production = cls.env.ref("mrp.mrp_production_1")

    def test_reset_to_confirmed(self):
        self.mrp_production.action_start()
        self.assertEqual(self.mrp_production.state, "progress")
        self.assertTrue(self.mrp_production.action_unstart_available)
        self.mrp_production.action_unstart()
        self.assertEqual(self.mrp_production.state, "confirmed")

    def test_not_reset_to_confirmed(self):
        self.mrp_production.action_start()
        self.mrp_production.write({"qty_producing": 1})
        self.assertEqual(self.mrp_production.state, "progress")
        self.assertFalse(self.mrp_production.action_unstart_available)
        self.mrp_production.action_unstart()
        self.assertNotEqual(self.mrp_production.state, "confirmed")
