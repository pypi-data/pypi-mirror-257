# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinAnalyticGroupM2OConfigurator(models.AbstractModel):
    _name = "mixin.analytic_group_m2o_configurator"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "account.analytic.group Many2one Configurator Mixin"

    _analytic_group_m2o_configurator_insert_form_element_ok = False
    _analytic_group_m2o_configurator_form_xpath = False

    analytic_group_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Analytic Group Selection Method",
        required=True,
    )
    analytic_group_ids = fields.Many2many(
        comodel_name="account.analytic.group",
        string="Analytic Groups",
        relation="rel_m2o_mixin_2_analytic_group",
    )
    analytic_group_domain = fields.Text(default="[]", string="Analytic Group Domain")
    analytic_group_python_code = fields.Text(
        default="result = []", string="Analytic Group Python Code"
    )

    @ssi_decorator.insert_on_form_view()
    def _analytic_group_m2o_configurator_insert_form_element(self, view_arch):
        # TODO
        template_xml = "ssi_cost_accounting."
        template_xml += "analytic_group_m2o_configurator_template"
        if self._analytic_group_m2o_configurator_insert_form_element_ok:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._analytic_group_m2o_configurator_form_xpath,
                position="inside",
            )
        return view_arch
