# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMrpBomComponentCost(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.write({"currency_id": cls.env.ref("base.USD").id})
        cls.company_eur = cls.env["res.company"].create(
            {"name": "Test company", "currency_id": cls.env.ref("base.EUR").id}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "detailed_type": "product",
            }
        )
        cls.component1 = cls.env["product.product"].create(
            {"name": "Test Component", "detailed_type": "product", "standard_price": 1}
        )
        cls.component2 = cls.env["product.product"].create(
            {
                "name": "Test Component 2",
                "detailed_type": "product",
                "standard_price": 12,
                "uom_id": cls.env.ref("uom.product_uom_dozen").id,
            }
        )
        cls.component_eur = cls.env["product.product"].create(
            {
                "name": "Test Component Eur",
                "detailed_type": "product",
                "standard_price": 1,
                "company_id": cls.company_eur.id,
            }
        )
        cls.bom = cls.env["mrp.bom"].create(
            {
                "product_id": cls.product.id,
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "bom_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.component1.id,
                            "product_qty": 2,
                            "product_uom_id": cls.env.ref("uom.product_uom_dozen").id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.component2.id,
                            "product_qty": 1,
                            "product_uom_id": cls.env.ref("uom.product_uom_unit").id,
                        },
                    ),
                ],
            }
        )

    def test_mrp_bom_component_cost(self):
        self.assertEqual(self.bom.bom_line_ids[0].cost_unit, 12)
        self.assertEqual(self.bom.bom_line_ids[0].cost_subtotal, 24)
        self.assertEqual(self.bom.cost_subtotal, 25)

    def test_mrp_bom_component_cost_multicurrency(self):
        self.bom = self.env["mrp.bom"].create(
            {
                "product_id": self.product.id,
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "company_id": self.company_eur.id,
                "bom_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.component1.id,
                            "product_qty": 1,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.component_eur.id,
                            "product_qty": 1,
                        },
                    ),
                ],
            }
        )
        line_usd = self.bom.bom_line_ids[0]
        self.assertNotEqual(self.bom.currency_id, line_usd.product_id.currency_id)
        self.assertNotEqual(line_usd.cost_unit, 1)
        self.assertNotEqual(line_usd.cost_subtotal, 1)
        self.assertNotEqual(self.bom.cost_subtotal, 2)
