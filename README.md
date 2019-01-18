# Module Construction ()

Field | Infomation
------------ | -------------
Name | Construction
Author | ![Peter Dinh](https://github.com/peter-dinh)
Odoo version | 12.0
Module version | 1.0.0
Depends | `base`, `stock`

## Description:
Hệ thống cần một module quản lý xây dựng; tập trung vào quản lý vật liệu trong xây dựng. Trong đó, hỗ trợ tồn kho trong hệ thống.
Hệ thống đã tích hợp sẵn module Stock. Moduel quản lý xây dựng cần kế thừa module này

## Relationship
### BFD Diagram:
![BFD](https://github.com/peter-dinh/construction/tree/master/static/src/img/BFD.png)

### Model Class:

### Method decorators:

## Views

### Menu:
```
Construction
|-- Project
    |-- Projects
    |-- State
    `-- Blocks

`-- Stock
    |-- Products
    |-- Receipts
    `-- Return
```

### Actions:


## Testing
TestCase         | Description 
------------ | -------------
??? | ???

## Security
> Tất cả các user đều có quyền truy cập

## Release: 
> v.1.0