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
    list_block = fields.One2many(comodel_name='construction.block', inverse_name='project_id', string='List Block')


class State_Project(models.Model):
    """
    Các giai đoạn của dự án
    """
    _name = 'construction.state_project'

    name = fields.Char(string='Name')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')
    project_id = fields.Many2one('construction.project', string="Project")
    list_proccessing = fields.One2many('construction.proccessing', inverse_name='state_id', string='List Result')
    finish = fields.Boolean(string='Finish')


class Block(models.Model):
    """
    Các hạng mục của dự án 
    """
    _name = 'construction.block'

    name = fields.Char(string='Name')
    project_id = fields.Many2one('construction.project', string='Project')
    list_proccessing = fields.One2mnay('construction.proccessing', inverse_id='block_id', string='List Result')

class Proccessing(models.Model):
    """
    Kết quả và yêu cầu của các giai đoạn thực hiện các hạng mục
    """
    _name = 'construction.proccessing'

    state_id = fields.Many2one('construction.state_project', string='State')
    block_id = fields.Many2one('construction.block', string='Block')
    project_id = fields.Many2one('construction.project', string='Project', compute='_get_project')
    requirement = fields.Many2one('construction.material_requirements', string='Requirements')
    result = fields.Selection(selection=[('proccessing', 'Proccessing'), ('cancel', 'Cancel'), ('success', 'Success')], required=True, default='proccessing')

    @api.multi
    def _get_project(self):
        return


class Material_Requirements(models.Model):
    """
    Danh sách yêu cầu vật tư cho giai đoạn triển khai hạng mục
    """
    _name = 'construction.material_requirements'

    name = fields.Char(string="Name")
    project_id = fields.Many2one('construction.project', string='Project', compute='_get_project')
    proccessing_id = field.Many2one('construction.proccessing', string='Proccessing', store=False, compute='_get_proccessing')
    list_material = fields.One2many('construction.material_detail', inverse_name='required_id', string='List Materials')
    
class Material_Detail(models.Model):
    """
    Chi tiết Vật tư cần sử dụng
    """
    _name = 'construction.material_detail'

    required_id = fields.Many2one('construction.material_requirements', string='Required')
    product_id = fields.Many2one('product.product', string="Material")
    quantity = fields.Integer(string="Quanity")
    enough = fields.Boolean(string='Enough', default=False)

class Receipt(models.Model):
    """
    Danh sách phiếu xuất vật tư
    """
    _name = 'construction.receipt'


    name = fields.Char(string='Name')
    required_id = fields.Many2one('construction.requirements', string='Required')
    list_detail = fields.One2many('construction.receipt_detail', string='List Detail')

class Receipt_Detail(models.Model):
    """
    Chi tiết vật tư đã xuất kho
    """
    _name = 'construction.receipt_detail'

    receipt_id = fields.Many2one('construction.receipt', string='Receipt')
    product_id = fields.Many2one('product.product', string="Material")
    quantity = fields.Integer(string="Quanity", compute='_get_max_qty')
    state = fields.Selection(string='State', selection=[])

class Return(models.Model):
    """
    Danh sách phiếu hoàn trả
    """
    _name = 'construction.return'

    name = fields.Char(string='Name')
    required_id = fields.Many2one('construction.requirements', string='Required')
    list_detail = fields.One2many('construction.return_detail', string='List Detail')


class Return_Detail(models.Model):
    """
    Danh sách phiếu hoàn trả
    """
    _name = 'construction.return_detail'

    receipt_id = fields.Many2one('construction.receipt', string='Receipt')
    product_id = fields.Many2one('product.product', string="Material")
    quantity = fields.Integer(string="Quanity")
    state = fields.Selection(string='State', selection=[])

class Product_For_Construction(models.Model):
    """
    Thêm loại sản phẩm dành cho xây dựng.
    """
    _inherit = 'product.template'

    type = fields.Selection(selection_add=[('construction', 'Construction')], default='construction')
