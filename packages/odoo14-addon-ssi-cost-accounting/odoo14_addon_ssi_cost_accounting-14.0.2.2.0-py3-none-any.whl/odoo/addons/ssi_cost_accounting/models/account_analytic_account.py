# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountAnalyticAccount(models.Model):
    _name = "account.analytic.account"
    _inherit = [
        "account.analytic.account",
        "mixin.date_duration",
    ]
    _order = "group_id, id"

    # Mixin duration attribute
    _date_start_readonly = False
    _date_end_readonly = False
    _date_start_required = False
    _date_end_required = False
