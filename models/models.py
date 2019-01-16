# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
    """

    """
    _name = 'construction.project'

    name = fields.Char(string='Name Project')
    commencement_date = fields.Date(string='Commencement Date')
    investor = fields.Char(string='Investor')
    company_id = fields.Many2one('res.')
    type_project = fields.Selection(selection=[('bridge', 'Bridge'), ('street', 'Street'), ('building', 'Building')])
    list_state = fields.One2many(comodel_name='construction.state_project', inverse_name='project_id', string='List State')

class Result(models.Model):
    """
    
    """
    _name = 'construction.result'

    state_id = fields.Many2one('construction.state_project', string='State')
    block_id = fields.Many2one('construction.block', string='Block')
    result = fields.Selection(selection=[('processing', 'Processing'), ('cancel', 'Cancel'), ('success', 'Success')], required=True, default='processing')


class State_Project(models.Model):
    """

    """
    _name = 'construction.state_project'

    name = fields.Char(string='Name')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')
    project_id = fields.Many2one('construction.project', string="Project")
    list_result = fields.One2many('construction.result', inverse_name='state_id', string='List Result')


class Block(models.Model):
    """

    """
    _name = 'construction.block'
    _inherit = 'construction.material_requirements'

    name = fields.Char(string='Name')
    project_id = fields.Many2one('construction.project', string='Project')
    state = fields.Many2one('construction.state_project', string='State')
    list_requirement = fields.One2many('construction.material_requirements', inverse_name='block_id', string='Requirements')
    list_result = fields.One2mnay('construction.result', inverse_id='block_id', string='List Result')

class Material_Requirements(models.Model):
    """

    """
    _name = 'construction.material_requirements'

    name = fields.Char(string="Name")
    block_id = field.Many2one('construction.block', string='Block')
    list_material = fields.One2many('construction.material_detail', inverse_name='required_id', string='List Materials')

    
class Material_Detail(models.Model):
    """

    """
    _name = 'construction.material_detail'
    _inherit = 'product.product'

    required_id = fields.Many2one('construction.material_requirements', string='Required')
    quantity = fields.Integer(string="Quanity")
    state = fields.Selection() # trang thai vat da da nhan



class Product_For_Construction(models.Model):
    """
    
    """
    _inherit = 'product.template'

    type = fields.Selection(selection_add=[('construction', 'Construction')])
