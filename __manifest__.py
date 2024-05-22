{
    'name': 'Employee Assets',
    'description': '''
    This module is to track the company assets per employee
    ''',
    'license': 'AGPL-3',
    'author': 'Victor O. ekwueme',
    'version': '14.0.1',
    'depends': ['mail'],
    'data': ['security/groups.xml','security/ir.model.access.csv','data/data_seq.xml','views/ove_asset_view.xml'],
    'application': True,
    'auto_install': False,
}
