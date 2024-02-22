# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def pre_init_hook(cr):
    """
    With this pre-init-hook we want to avoid error when creating the UNIQUE
    code constraint when the module is installed and before the post-init-hook
    is launched.
    """
    cr.execute("ALTER TABLE mrp_production ADD COLUMN type_id INTEGER;")


def post_init_hook(cr, registry):
    cr.execute(
        """
    UPDATE
        mrp_production mo
    SET
        type_id = t.id
    FROM
        mrp_production_type t
    WHERE
        t.code = 'T0001'
        AND mo.type_id IS NULL;
    """
    )
