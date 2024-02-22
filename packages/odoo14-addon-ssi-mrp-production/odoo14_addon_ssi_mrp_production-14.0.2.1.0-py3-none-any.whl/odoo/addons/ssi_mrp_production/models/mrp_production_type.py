# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MRPProductionType(models.Model):
    _name = "mrp_production_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Manufacturing Production Type"
