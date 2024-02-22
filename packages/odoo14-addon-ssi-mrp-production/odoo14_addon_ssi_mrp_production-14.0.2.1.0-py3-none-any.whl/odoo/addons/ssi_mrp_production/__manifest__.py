# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MRP Production",
    "version": "14.0.2.1.0",
    "category": "Manufacturing/Manufacturing",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "website": "https://simetri-sinergi.id",
    "depends": [
        "mrp",
        "stock_move_backdating",
        "ssi_master_data_mixin",
        "ssi_policy_mixin",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "data/mrp_production_type.xml",
        "data/policy_template_data.xml",
        "views/mrp_production_views.xml",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/stock_production_lot_views.xml",
        "views/stock_scheduler_compute_views.xml",
        "views/mrp_unbuild_views.xml",
        "views/stock_scrap_views.xml",
        "views/mrp_bom_views.xml",
        "views/mrp_production_type_views.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
}
