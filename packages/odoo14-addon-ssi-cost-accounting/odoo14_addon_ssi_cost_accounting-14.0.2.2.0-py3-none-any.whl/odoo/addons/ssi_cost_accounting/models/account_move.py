# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        res = super()._post(soft=soft)
        self.mapped("line_ids")._check_analytic_required()
        return res
