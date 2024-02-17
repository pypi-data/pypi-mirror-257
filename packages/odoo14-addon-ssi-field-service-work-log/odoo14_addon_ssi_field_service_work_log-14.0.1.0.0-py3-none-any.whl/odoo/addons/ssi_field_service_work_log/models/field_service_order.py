# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class FieldServiceOrder(models.Model):
    _name = "field_service_order"
    _inherit = [
        "field_service_order",
        "mixin.work_object",
    ]

    _work_log_create_page = True
