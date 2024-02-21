# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAnalyticGroup(models.Model):
    _name = "account.analytic.group"
    _inherit = [
        "account.analytic.group",
    ]
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
