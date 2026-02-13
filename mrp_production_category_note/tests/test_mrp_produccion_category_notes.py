# Copyright 2025 Angel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMrpProduccionCategoryNotes(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product_category_with_mrp_notes = cls.env["product.category"].create(
            {
                "name": "Test Category with Mrp Notes",
                "mrp_notes": "<table><tr><td>Test</td></tr></table>",
            }
        )

        cls.product_category_without_mrp_notes = cls.env["product.category"].create(
            {
                "name": "Test Category without Mrp Notes",
                "mrp_notes": "",
            }
        )

        cls.product_with_mrp_notes = cls.env["product.product"].create(
            {
                "name": "Test Product with Mrp notes",
                "categ_id": cls.product_category_with_mrp_notes.id,
            }
        )

        cls.product_without_mrp_notes = cls.env["product.product"].create(
            {
                "name": "Test Product without Mrp notes",
                "categ_id": cls.product_category_without_mrp_notes.id,
            }
        )

        cls.uom_id = cls.product_with_mrp_notes.uom_id.id

        cls.mrp_production = cls.env["mrp.production"].create(
            {
                "product_id": cls.product_with_mrp_notes.id,
                "product_uom_id": cls.uom_id,
            }
        )

    def test_get_category_notes(self):
        table_html = self.product_with_mrp_notes.categ_id.get_mrp_notes()
        self.assertEqual(
            table_html,
            "<table><tr><td>Test</td></tr></table>",
            "The category's HTML table should be correctly retrieved.",
        )

        category_grandparent = self.env["product.category"].create(
            {
                "name": "Category Grandparent",
                "mrp_notes": "<table><tr><td>Grandparent</td></tr></table>",
            }
        )
        category_parent = self.env["product.category"].create(
            {"name": "Category Parent", "parent_id": category_grandparent.id}
        )
        category_child = self.env["product.category"].create(
            {"name": "Category Child", "parent_id": category_parent.id}
        )
        product = self.env["product.product"].create(
            {"name": "Product", "categ_id": category_child.id}
        )

        table_html = product.categ_id.get_mrp_notes()
        self.assertEqual(
            table_html,
            "<table><tr><td>Grandparent</td></tr></table>",
            "The notes from the grandparent category should be correctly retrieved.",
        )

    def test_create_mrp_production_without_notes(self):
        mrp_production = self.env["mrp.production"].create(
            {
                "product_id": self.product_without_mrp_notes.id,
                "product_uom_id": self.product_without_mrp_notes.uom_id.id,
            }
        )
        self.assertFalse(
            mrp_production.notes,
            "The notes field should be empty if the category has no predefined notes.",
        )

    def test_create_mrp_production_with_notes(self):
        mrp_production = self.env["mrp.production"].create(
            {
                "product_id": self.product_with_mrp_notes.id,
                "product_uom_id": self.product_with_mrp_notes.uom_id.id,
            }
        )

        self.assertEqual(
            mrp_production.notes,
            "<table><tr><td>Test</td></tr></table>",
            "The 'notes' field should be populated with the predefined category notes.",
        )

    def test_create_mrp_production_with_existing_notes(self):
        mrp_production = self.env["mrp.production"].create(
            {
                "product_id": self.product_with_mrp_notes.id,
                "product_uom_id": self.product_with_mrp_notes.uom_id.id,
                "notes": "Pre-existing notes",
            }
        )
        expected_notes = (
            "<p>Pre-existing notes\n</p><table><tr><td>Test</td></tr></table>"
        )
        current_notes = str(mrp_production.notes)
        self.assertEqual(current_notes, expected_notes)
