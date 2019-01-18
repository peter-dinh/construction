# Module Construction ()

Field | Infomation
------------ | -------------
Name | Construction
Author | [Peter Dinh](https://github.com/peter-dinh)
Odoo version | 12.0
Module version | 1.0.0
Depends | `base`, `stock`

## Description:
Hệ thống cần một module quản lý xây dựng; tập trung vào quản lý vật liệu trong xây dựng. Trong đó, hỗ trợ tồn kho trong hệ thống.
Hệ thống đã tích hợp sẵn module Stock. Moduel quản lý xây dựng cần kế thừa module này

## Relationship
### BFD Diagram:
![BFD](https://github.com/peter-dinh/construction/blob/master/static/src/img/BFD.png "BFD Diagram")

### DFD Diagram:
#### Context Level
![Context Level](https://github.com/peter-dinh/construction/blob/master/static/src/img/Context.png "Context Level")

#### Action Project
![Action Project](https://github.com/peter-dinh/construction/blob/master/static/src/img/Project.png "Action Project")

#### Action Proccessing
![Action Proccessing](https://github.com/peter-dinh/construction/blob/master/static/src/img/Proccessing.png "Action Proccessing")

#### Action Receipt
![Action Receipt](https://github.com/peter-dinh/construction/blob/master/static/src/img/Receipt.png "Action Receipt")

#### Action Return
![Action Return](https://github.com/peter-dinh/construction/blob/master/static/src/img/Return.png "Action Return")

### Model Class:

``` python
class Project(models.Model):
    """
    Danh sách dự án của công ty
    """
    _name = 'construction.project'
```

``` python
class Proccessing(models.Model):
    """
    Kết quả và yêu cầu của các giai đoạn thực hiện các hạng mục
    """
    _name = 'construction.proccessing'
```

``` python
class State_Project(models.Model):
    """
    Các giai đoạn của dự án
    """
    _name = 'construction.state_project'
```

``` python
class Block(models.Model):
    """
    Các hạng mục của dự án 
    """
    _name = 'construction.block'
```

``` python
class Material_Requirements(models.Model):
    """
    Danh sách yêu cầu vật tư cho giai đoạn triển khai hạng mục
    """
    _name = 'construction.material_requirements'
```

``` python
class Material_Detail(models.Model):
    """
    Chi tiết Vật tư cần sử dụng
    """
    _name = 'construction.material_detail'
```

``` python
class Receipt(models.Model):
    """
    Danh sách phiếu xuất vật tư
    """
    _name = 'construction.receipt'
```

``` python
class Receipt_Detail(models.Model):
    """
    Chi tiết vật tư đã xuất kho
    """
    _name = 'construction.receipt_detail'
```

``` python
class Return(models.Model):
    """
    Danh sách phiếu hoàn trả
    """
    _name = 'construction.return'
```

``` python
class Return_Detail(models.Model):
    """
    Danh sách phiếu hoàn trả
    """
    _name = 'construction.return_detail'
```

``` python
class Product_For_Construction(models.Model):
    """
    Thêm loại sản phẩm dành cho xây dựng.
    """
    _inherit = 'product.template'
```

### Method decorators:

> Not Data

## Views

### Menu:
```
Construction
|-- Project
    |-- Projects
    |-- Proccessing
    |-- State
    `-- Blocks

`-- Stock
    |-- Products
    |-- Receipts
    `-- Return
```

### Actions:

> Not Data

## Testing
TestCase         | Description 
------------ | -------------
??? | ???

## Security
> Tất cả các user đều có quyền truy cập

## Release: 
> v.1.0

## Features need improvement:
> Cần thêm tính năng tạo phiếu xuất khi số lượng yêu cầu không đủ để hoàn thành cho qúa trình thực hiện
