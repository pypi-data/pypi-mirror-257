# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging


def migrate(cr, version):
    if not version:
        return
    logger = logging.getLogger(__name__)
    logger.info("Updating manufacturing order...")
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
    logger.info("Successfully updated mrp.production tables")
