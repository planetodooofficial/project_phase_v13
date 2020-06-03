{
    'name': 'Project Phases Management',
    'version': '13.1.0',
    "category": "website",
    'summary': 'Project Phases Management',
    "description": """Project management using project methodologies.""",
    "author": "Planet-odoo",
    'website': 'http://www.planet-odoo.com/',
    'depends': ['base', 'web', 'project'],
    'data': [
             'security/ir.model.access.csv',
             'views/project_phases_view.xml',
             'views/project_dashboard.xml',
         ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
