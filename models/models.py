# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
    """
    Danh sách dự án của công ty
    """
    _name = 'construction.project'

    name = fields.Char(string='Name Project')
    commencement_date = fields.Date(string='Commencement Date')
    investor = fields.Char(string='Investor')
    company_id = fields.Many2one('res.company', string="Company", default=lamda self: self.env.user.company_id.id)
    type_project = fields.Selection(selection=[('bridge', 'Bridge'), ('street', 'Street'), ('building', 'Building')])
    list_state = fields.One2many(comodel_name='construction.state_project', inverse_name='project_id', string='List State')

class Perform(models.Model):
    """
    Kết quả và yêu cầu của các giai đoạn thực hiện các hạng mục
    """
    _name = 'construction.perform'

    state_id = fields.Many2one('construction.state_project', string='State')
    block_id = fields.Many2one('construction.block', string='Block', domain=)
    project_id = fields.Many2one('construction.project', string='Project')
    requirement = fields.Many2one('construction.material_requirements', string='Requirements')
    result = fields.Selection(selection=[('processing', 'Processing'), ('cancel', 'Cancel'), ('success', 'Success')], required=True, default='processing')


class State_Project(models.Model):
    """
    Các giai đoạn của dự án
    """
    _name = 'construction.state_project'

    name = fields.Char(string='Name')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')
    project_id = fields.Many2one('construction.project', string="Project")
    list_perform = fields.One2many('construction.perform', inverse_name='state_id', string='List Result')
    finish = fields.Boolean(string='Finish')


class Block(models.Model):
    """
    Các hạng mục của dự án 
    """
    _name = 'construction.block'
    _inherit = 'construction.material_requirements'

    name = fields.Char(string='Name')
    project_id = fields.Many2one('construction.project', string='Project')
    list_perform = fields.One2mnay('construction.perform', inverse_id='block_id', string='List Result')

class Material_Requirements(models.Model):
    """
    Danh sách yêu cầu vật tư cho giai đoạn triển khai hạng mục
    """
    _name = 'construction.material_requirements'

    name = fields.Char(string="Name")
    block_id = field.Many2one('construction.block', string='Block', store=False, compute='_get_block')
    list_material = fields.One2many('construction.material_detail', inverse_name='required_id', string='List Materials')

    
class Material_Detail(models.Model):
    """
    Chi tiết Vật tư cần sử dụng
    """
    _name = 'construction.material_detail'
    _inherit = 'product.product'

    required_id = fields.Many2one('construction.material_requirements', string='Required')
    quantity = fields.Integer(string="Quanity")
    state = fields.Selection() # trang thai vat da da nhan



class Product_For_Construction(models.Model):
    """
    Thêm loại sản phẩm dành cho xây dựng.
    """
    _inherit = 'product.template'

    type = fields.Selection(selection_add=[('construction', 'Construction')], default='construction')
