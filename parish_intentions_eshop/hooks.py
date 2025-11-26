import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

MODULE_NAME = "parish_intentions_eshop"


def cleanup_duplicate_modules(cr, registry):
    """Ensure the module keeps the expected name and remove duplicate entries."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    modules = env["ir.module.module"].sudo().search(
        [("name", "=", MODULE_NAME)], order="id"
    )
    if not modules:
        return

    module_to_keep = modules[0]
    duplicates = modules[1:]
    if duplicates:
        _logger.info(
            "Removing %s duplicate module record(s) for %s: %s",
            len(duplicates),
            MODULE_NAME,
            duplicates.ids,
        )
        duplicates.unlink()

    if module_to_keep.shortdesc != MODULE_NAME:
        module_to_keep.shortdesc = MODULE_NAME
