from odoo import api, fields, models

class AssetCategory(models.Model):
    _name = 'ove.asset.category'
    _description = 'Asset Category'

    name = fields.Char('Asset Category')
    parent_id = fields.Many2one('ove.asset.category', string='Parent')
    children_ids = fields.One2many('ove.asset.category','parent_id', string='Children', copy=True)
    asset_ids = fields.One2many('ove.asset', 'parent_id', 'Assets')

        


class EmployeeAsset(models.Model):
    _name = 'ove.employee.asset'
    _description = 'Organisational Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Reference', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    asset_line = fields.One2many('ove.employee.asset.line','employee_asset_id', string='Asset Lines')
    total_assets = fields.Float(string='Total Asset Value', compute='_compute_total_value', readonly=True)


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('ove.asset') or '/'
        return  super().create(vals)

    @api.depends('asset_line.asset_value')
    def _compute_total_value(self):
        for record in self:
            total = 0.0
            for line in record.asset_line:
                total += line.asset_value
            record.total_assets = total

class AssetLine(models.Model):
    _name = 'ove.employee.asset.line'
    _description = 'Asset Lines'

    employee_asset_id = fields.Many2one('ove.employee.asset', string='Employee Asset Lines')
    asset_id = fields.Many2one('ove.asset', name='Asset', required=True)
    date_assigned = fields.Date('Date Assigned', default=fields.Date.today)
    date_returned = fields.Date('Date Returned')
    asset_value = fields.Monetary(related='asset_id.asset_value', currency='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency')


class Asset(models.Model):
    _name = 'ove.asset'
    _description = 'Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Asset Name')
    description = fields.Char('Description')
    parent_id = fields.Many2one('ove.asset.category', string='Asset Category')
    asset_value = fields.Monetary(string='Asset Value', currency='currency_id')
    serial_number = fields.Char('Serial Number')
    part_number = fields.Char('Part Number')
    currency_id = fields.Many2one('res.currency', string='Currency')
    asset_state = fields.Text('Asset State After Return')
    asset_writeoff_date = fields.Date('Write Off Date')
    date_purchased = fields.Date('Date Purchased', required=True, default=fields.Date.today())
