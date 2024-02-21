# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _has_analytic_distribution(self):
        # If the move line has an analytic tag with distribution, the field
        # analytic_account_id may be empty. So in this case, we do not check it.
        tags_with_analytic_distribution = self.analytic_tag_ids.filtered(
            "active_analytic_distribution"
        )
        return bool(tags_with_analytic_distribution.analytic_distribution_ids)

    def _check_analytic_required_msg(self):
        self.ensure_one()
        company_cur = self.company_currency_id
        if company_cur.is_zero(self.debit) and company_cur.is_zero(self.credit):
            return None
        analytic_policy = self.account_id._get_analytic_policy()
        if (
            analytic_policy == "always"
            and not self.analytic_account_id
            and not self._has_analytic_distribution()
        ):
            return _(
                "Analytic policy is set to 'Always' with account "
                "'%s' but the analytic account is missing in "
                "the account move line with label '%s'."
            ) % (
                self.account_id.display_name,
                self.name or "",
            )
        elif analytic_policy == "never" and (
            self.analytic_account_id or self._has_analytic_distribution()
        ):
            analytic_account = (
                self.analytic_account_id
                or self.analytic_tag_ids.analytic_distribution_ids[:1]
            )
            return _(
                "Analytic policy is set to 'Never' with account "
                "'%s' but the account move line with label '%s' "
                "has an analytic account '%s'."
            ) % (
                self.account_id.display_name,
                self.name or "",
                analytic_account.display_name,
            )
        elif (
            analytic_policy == "posted"
            and not self.analytic_account_id
            and self.move_id.state == "posted"
            and not self._has_analytic_distribution()
        ):
            return _(
                "Analytic policy is set to 'Posted moves' with "
                "account '%s' but the analytic account is missing "
                "in the account move line with label '%s'."
            ) % (
                self.account_id.display_name,
                self.name or "",
            )
        return None

    @api.constrains("analytic_account_id", "account_id", "debit", "credit")
    def _check_analytic_required(self):
        for rec in self:
            message = rec._check_analytic_required_msg()
            if message:
                raise exceptions.ValidationError(message)
