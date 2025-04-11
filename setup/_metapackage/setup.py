import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-sygel-technology-sy-manufacture",
    description="Meta package for sygel-technology-sy-manufacture Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-mrp_bom_warn_message>=15.0dev,<15.1dev',
        'odoo-addon-mrp_production_category_notes>=15.0dev,<15.1dev',
        'odoo-addon-picking_very_high_priority_mrp>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
