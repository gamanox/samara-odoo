{
    "name": "parish_intentions_eshop",
    "summary": "Capture and manage mass intentions from the Odoo eCommerce shop (Odoo 17)",
    "version": "17.0.1.0.0",
    "category": "Website",
    "author": "Parroquia",
    "license": "LGPL-3",
    "depends": ["website_sale", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/parish_intention_views.xml",
        "views/templates.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "parish_intentions_eshop/static/src/scss/style.scss"
        ]
    },
    "post_init_hook": "cleanup_duplicate_modules",
    "installable": True,
    "application": False
}
