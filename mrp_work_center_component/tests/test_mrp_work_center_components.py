# Copyright 2025 Angel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMrpWorkCenterComponents(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product_table = cls.env["product.product"].create(
            {
                "name": "Table",
                "type": "product",
            }
        )
        cls.product_leg = cls.env["product.product"].create(
            {
                "name": "Leg",
                "type": "product",
            }
        )
        cls.product_top = cls.env["product.product"].create(
            {
                "name": "Tabletop",
                "type": "product",
            }
        )
        cls.product_screw = cls.env["product.product"].create(
            {
                "name": "Screw",
                "type": "product",
            }
        )
        cls.product_washer = cls.env["product.product"].create(
            {
                "name": "Washer",
                "type": "product",
            }
        )

        cls.workcenter = cls.env["mrp.workcenter"].create({"name": "Table Workcenter"})

        cls.env["mrp.workcenter.component"].create(
            {
                "work_center_id": cls.workcenter.id,
                "product_id": cls.product_screw.id,
                "quantity": 8,
            }
        )
        cls.env["mrp.workcenter.component"].create(
            {
                "work_center_id": cls.workcenter.id,
                "product_id": cls.product_washer.id,
                "quantity": 4,
            }
        )

        cls.bom = cls.env["mrp.bom"].create(
            {
                "product_tmpl_id": cls.product_table.product_tmpl_id.id,
                "product_qty": 1.0,
                "type": "normal",
                "bom_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_leg.id,
                            "product_qty": 4,
                            "product_uom_id": cls.product_leg.uom_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_top.id,
                            "product_qty": 1,
                            "product_uom_id": cls.product_top.uom_id.id,
                        },
                    ),
                ],
            }
        )

    def test_add_workcenter_components(self):
        production = self.env["mrp.production"].create(
            {
                "product_id": self.product_table.id,
                "product_qty": 1.0,
                "product_uom_id": self.product_table.uom_id.id,
                "bom_id": self.bom.id,
                "location_src_id": self.env.ref("stock.stock_location_stock").id,
                "location_dest_id": self.env.ref("stock.stock_location_stock").id,
            }
        )
        production.action_confirm()
        self.env["mrp.workorder"].create(
            {
                "production_id": production.id,
                "workcenter_id": self.workcenter.id,
                "product_id": production.product_id.id,
                "product_uom_id": production.product_uom_id.id,
                "name": "Manual Workorder",
            }
        )
        production._add_workcenter_components()
        self.assertEqual(len(production.move_raw_ids), 4)

    def test_write_updates_workcenter_components_sin_additional(self):
        component_old = self.env["product.product"].create(
            {"name": "Old Component", "type": "product"}
        )
        component_new = self.env["product.product"].create(
            {"name": "New Component", "type": "product"}
        )

        workcenter_old = self.env["mrp.workcenter"].create({"name": "Old WC"})
        workcenter_new = self.env["mrp.workcenter"].create({"name": "New WC"})

        self.env["mrp.workcenter.component"].create(
            {
                "work_center_id": workcenter_old.id,
                "product_id": component_old.id,
                "quantity": 1,
                "company_id": self.env.company.id,
            }
        )
        self.env["mrp.workcenter.component"].create(
            {
                "work_center_id": workcenter_new.id,
                "product_id": component_new.id,
                "quantity": 2,
                "company_id": self.env.company.id,
            }
        )

        product = self.env["product.product"].create(
            {"name": "Product", "type": "product"}
        )
        bom = self.env["mrp.bom"].create(
            {
                "product_tmpl_id": product.product_tmpl_id.id,
                "product_qty": 1.0,
                "type": "normal",
            }
        )

        production = self.env["mrp.production"].create(
            {
                "product_id": product.id,
                "product_qty": 1.0,
                "product_uom_id": product.uom_id.id,
                "bom_id": bom.id,
                "location_src_id": self.env.ref("stock.stock_location_stock").id,
                "location_dest_id": self.env.ref("stock.stock_location_stock").id,
            }
        )

        workorder = self.env["mrp.workorder"].create(
            {
                "production_id": production.id,
                "workcenter_id": workcenter_old.id,
                "product_id": product.id,
                "product_uom_id": product.uom_id.id,
                "name": "Test Workorder",
            }
        )

        production._add_workcenter_components(workcenter_id=workcenter_old.id)

        move_old = production.move_raw_ids.filtered(
            lambda m: m.product_id == component_old and m.state == "draft"
        )
        self.assertEqual(len(move_old), 1)

        workorder.write({"workcenter_id": workcenter_new.id})

        move_old_after = production.move_raw_ids.filtered(
            lambda m: m.product_id == component_old and m.state == "draft"
        )
        self.assertEqual(len(move_old_after), 0)

        move_new = production.move_raw_ids.filtered(
            lambda m: m.product_id == component_new and m.state == "draft"
        )
        self.assertEqual(len(move_new), 1)
        self.assertEqual(move_new.product_uom_qty, 2)
