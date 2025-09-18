# @author: Armand Polmard (https://arpol.fr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "AFDOC Multi Company Config",
    "version": "1.0",
    "category": "Settings",
    "summary": "Configuration for multi-company setups",
    "description": """
        This module provides configuration settings to manage multi-company environments effectively.
    """,
    "author": "Armand POLMARD",
    "installable": True,
    "application": False,
    "depends": ["base","membership"],
    "data": [
        "views/res_partner_category_views.xml",
        "security/multi_company_security.xml",
    ],
}