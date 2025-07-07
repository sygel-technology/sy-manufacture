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
        additional_moves = production.move_raw_ids.filtered(lambda m: m.additional)
        self.assertEqual(len(additional_moves), 2)
        self.assertSetEqual(
            set(additional_moves.mapped("product_id.id")),
            {self.product_screw.id, self.product_washer.id},
        )

    def test_write_updates_workcenter_components_real(self):
        new_workcenter = self.env["mrp.workcenter"].create({"name": "New WC"})
        self.env["mrp.workcenter.component"].create(
            {
                "work_center_id": new_workcenter.id,
                "product_id": self.product_leg.id,
                "quantity": 2,
                "company_id": self.env.company.id,
            }
        )

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

        workorder = self.env["mrp.workorder"].create(
            {
                "production_id": production.id,
                "workcenter_id": self.workcenter.id,
                "product_id": production.product_id.id,
                "product_uom_id": production.product_uom_id.id,
                "name": "Initial Workorder",
            }
        )

        production._update_workcenter_components()
        additional_moves_initial = production.move_raw_ids.filtered(
            lambda m: m.additional
        )
        self.assertEqual(len(additional_moves_initial), 2)

        workorder.write({"workcenter_id": new_workcenter.id})
        production._update_workcenter_components()

        additional_moves_after = production.move_raw_ids.filtered(
            lambda m: m.additional
        )
        self.assertEqual(len(additional_moves_after), 1)
        self.assertEqual(additional_moves_after.product_id, self.product_leg)

        production.write(
            {
                "workorder_ids": [
                    (
                        0,
                        0,
                        {
                            "workcenter_id": new_workcenter.id,
                            "product_id": production.product_id.id,
                            "product_uom_id": production.product_uom_id.id,
                            "name": "Nuevo WO desde write",
                        },
                    )
                ]
            }
        )

        additional_moves_write = production.move_raw_ids.filtered(
            lambda m: m.additional
        )
        self.assertEqual(len(additional_moves_write), 1)
        self.assertEqual(additional_moves_write.product_id, self.product_leg)

        product_qty_before = production.product_qty
        production.write({"product_qty": product_qty_before + 1})
        additional_moves_final = production.move_raw_ids.filtered(
            lambda m: m.additional
        )
        self.assertEqual(len(additional_moves_final), 1)
