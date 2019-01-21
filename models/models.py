# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Project(models.Model):
    """
    Danh sách dự án của công ty
    """
    _name = 'construction.project'

    name = fields.Char(string='Name Project')
    commencement_date = fields.Date(string='Commencement Date')
    investor = fields.Char(string='Investor')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id.id)
    type_project = fields.Selection(selection=[('bridge', 'Bridge'), ('street', 'Street'), ('building', 'Building')])
    list_stage = fields.One2many('construction.stage_project', inverse_name='project_id', string='List Stage')
    list_block = fields.One2many('construction.block', inverse_name='project_id', string='List Block')
    list_proccessing = fields.One2many('construction.proccessing', inverse_name='project_id', string='List Proccessing')


class Stage_Project(models.Model):
    """
    Các giai đoạn của dự án
    """
    _name = 'construction.stage_project'

    name = fields.Char(string='Name')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')
    project_id = fields.Many2one('construction.project', string="Project", required=True)
    list_proccessing = fields.One2many('construction.proccessing', inverse_name='stage_id', string='List Result')
    finish = fields.Boolean(string='Finish')

    @api.depends('date_start')
    @api.constrains('date_end')
    def _check_date_end(self):
        for item in self:
            if item.date_end <= item.date_start:
                raise ValidationError('Ngay ket thuc phai lon hon ngay bat dau')


class Block(models.Model):
    """
    Các hạng mục của dự án 
    """
    _name = 'construction.block'

    name = fields.Char(string='Name')
    project_id = fields.Many2one('construction.project', string='Project')
    list_proccessing = fields.One2many('construction.proccessing', inverse_name='block_id', string='List Result')



class Proccessing(models.Model):
    """
    Kết quả và yêu cầu của các giai đoạn thực hiện các hạng mục
    """
    _name = 'construction.proccessing'

    stage_id = fields.Many2one('construction.stage_project', string='Stage')
    block_id = fields.Many2one('construction.block', string='Block')
    project_id = fields.Many2one('construction.project', string='Project', required=True)
    requirement = fields.Many2one('construction.material_requirements', string='Requirements')
    date_start = fields.Date(string='Date Start', compute='_get_date_start', store=False)
    date_end = fields.Date(string='Date End', compute='_get_date_end', store=False)
    result = fields.Selection(selection=[('proccessing', 'Proccessing'), ('expired', 'Expired'), ('finish', 'Finish'), ('fail', 'Fail'), ('success', 'Success')], required=True, default='proccessing')

    @api.constrains('block_id')
    def _check_block_id(self):
        """
        Kiểm tra blocks co cùng dự án không?
        """
        for item in self:
            if item.block_id.project_id !=  item.project_id:
                raise ValidationError('Hang muc khong hop le!')
        return 
    
    @api.constrains('stage_id')
    def _check_stage_id(self):
        """
        Kiem tra giai doan co cung dua an khong?
        """
        for item in self:
            if item.stage_id.project_id == item.project_id:
                raise ValidationError('Giai doan khong hop le!')

    ## Can dieu huong result sau moi trang thai chon

    @api.multi
    def update_result_expired(self):
        """
        Cập nhật các quá trình thực hiện hết hạn
        """
        item_expired = self.search([('date_end', '>=', date.today())])
        item_expired.write({'result': 'expired'})
        return True
            

    @api.multi
    def _get_date_start(self):
        """
            Lấy ngày bắt đầu của giai đoạn
        """
        for item in self:
            item.date_start = self.env['construction.stage_project'].search([('id', '=', item.stage_id.id)], limit=1).date_start

    @api.multi
    def _get_date_end(self):
        """
            Lấy ngày kết thúc của giai 
        """
        for item in self:
            item.date_end = self.env['construction.stage_project'].search([('id', '=', item.stage_id.id)], limit=1).date_end


class Material_Requirements(models.Model):
    """
    Danh sách yêu cầu vật tư cho giai đoạn triển khai hạng mục
    """
    _name = 'construction.material_requirements'

    name = fields.Char(string="Name", compute='get_name_requirement')
    project_id = fields.Many2one('construction.project', string='Project', compute='_get_project')
    proccessing_id = fields.Many2one('construction.proccessing', string='Proccessing', store=False, compute='_get_proccessing')
    list_material = fields.One2many('construction.material_detail', inverse_name='required_id', string='List Materials')
    total_price = fields.Integer(string='Total price', compute='_get_total_price')


    @api.multi
    def _get_total_price(self):
        """"""
        for item in self:
            list_material = item.env['construction.material_detail'].search([('required_id', '=', id)])
            total = 0
            for material_detail in list_material:
                total += material_detail.product_id.product_tmpl_id.list_price
            item.write({'total_price': total})

    @api.multi
    def _get_project(self):
        """
        Lay thong tin du an
        """
        for item in self:
            item.write({'project_id': item.proccessing_id.project_id.id})


class Material_Detail(models.Model):
    """
    Chi tiết Vật tư cần sử dụng
    """
    _name = 'construction.material_detail'

    required_id = fields.Many2one('construction.material_requirements', string='Required')
    product_id = fields.Many2one('product.product', string="Material")
    quantity = fields.Integer(string="Quanity")
    enough = fields.Boolean(string='Enough', default=False)

    @api.multi
    def _get_project(self):
        """
        Lay thong tin du an
        """
        for item in self:
            item.write({'project_id': item.required_id.project_id.id})

    @api.constrains('product_id')
    def check_type_product(self):
        """
        Kiem tra loai vat tu
        """
        for item in self:
            if item.product_id.type != 'construction':
                raise ValidationError('Vat tu khong hop le!')

class Picking_for_construction(models.Model):
    """
    Ke thua module stoke
    """
    _name = 'construction.picking.stock'
    _inherits = {'stock.picking': 'stock_picking_id'}

    required_id = fields.Many2one('construction.material_requirements', string='Required', ondelete='cascade')
    stock_picking_id = fields.Many2one('stock.picking', 'Stock Picking', auto_join=True, index=True, ondelete='cascade', required=True)


    @api.multi
    def get_list_material(self):
        """
        Lay cac vat tu theo yeu cau va tao moi chung.
        Neu san pham da ton tai thi cap nhat so luong yeu cau
        """
        for item in self:
            for material in item.required_id.list_material:
                product = self.evn['stock.move'].search([('product_id', '=', material.product_id.id), ('picking_id', '=', item.id)])
                if not product.exists():
                    self.env['stock.move'].create({'picking_id': item.id, 'product_id': material.product_id.id, 'product_uom_qty': material.quantity})
                else:
                    product.write({'product_uom_qty': material.quantity})


# class Receipt(models.Model):
#     """
#     Danh sách phiếu xuất vật tư
#     """
#     _name = 'construction.receipt'

#     name = fields.Char(string='Name')
#     required_id = fields.Many2one('construction.requirements', string='Required')
#     list_detail = fields.One2many('construction.receipt_detail', string='List Detail')


# class Receipt_Detail(models.Model):
#     """
#     Chi tiết vật tư đã xuất kho
#     """
#     _name = 'construction.receipt_detail'

#     receipt_id = fields.Many2one('construction.receipt', string='Receipt')
#     product_id = fields.Many2one('product.product', string="Material")
#     quantity = fields.Integer(string="Quanity", compute='_get_max_qty')
#     stage = fields.Selection(string='Stage', selection=[])

#     @api.multi
#     def _get_max_qty(self):
#         for item in self:
#             quantity = item.product_id.product_tmpl_id.qty_available
#             qty_required = item.required_id.quantity
            
#             if qty_required > quantity:
#                 item.quantity = quantity
#             else:
#                 item.quantity 


# class Return(models.Model):
#     """
#     Danh sách phiếu hoàn trả
#     """
#     _name = 'construction.return'

#     name = fields.Char(string='Name')
#     required_id = fields.Many2one('construction.requirements', string='Required')
#     list_detail = fields.One2many('construction.return_detail', string='List Detail')


# class Return_Detail(models.Model):
#     """
#     Danh sách phiếu hoàn trả
#     """
#     _name = 'construction.return_detail'

#     receipt_id = fields.Many2one('construction.receipt', string='Receipt')
#     product_id = fields.Many2one('product.product', string="Material")
#     quantity = fields.Integer(string="Quanity")
#     stage = fields.Selection(string='Stage', selection=[])


class Product_For_Construction(models.Model):
    """
    Thêm loại sản phẩm dành cho xây dựng.
    """
    _inherit = 'product.template'

    type = fields.Selection(selection_add=[('construction', 'Construction')], default='construction')
