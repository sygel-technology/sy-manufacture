# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.quality_control_oca.tests.test_quality_control import (
    TestQualityControlOcaBase,
)


class TestQualityControlWaitApproval(TestQualityControlOcaBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wizard = cls.wizard_model.with_context(active_id=cls.inspection1.id).create(
            {"test": cls.test.id}
        )
        cls.wizard.action_create_test()
        cls.inspection1.action_todo()

    def test_inspection_correct_wait_approval(self):
        for line in self.inspection1.inspection_lines:
            if line.question_type == "qualitative":
                line.qualitative_value = self.val_ok
            if line.question_type == "quantitative":
                line.quantitative_value = 5.0
        self.inspection1.action_confirm()
        self.assertEqual(self.inspection1.state, "waiting")
