{
    'name': 'Time Tracker',
    'version': '13.1.0',
    "category": "website",
    'summary': 'Time Tracker',
    "description": """Project management using project methodologies.""",
    "author": "Planet-odoo",
    'website': 'http://www.planet-odoo.com/',
    'depends': ['base', 'web', 'project', 'account','hr_timesheet', 'calendar', 'web_tree_image'],
    'data': [
        'security/access_groups.xml',
        'security/access_rule.xml',
        'security/ir.model.access.csv',
        'views/timesheet_tracker_views.xml',
        'views/project_views_inherit.xml',
        'views/timesheet_tracker_inherit_views.xml',
        'views/time_tracker_settings_view.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
