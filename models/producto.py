
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Producto(models.Model):
    _name = 'streetzone.producto'
    _description = 'Producto de StreetZone'

    nombre = fields.Char(string='Nombre', required=True)
    precio = fields.Float(string='Precio', required=True, default=0.0)

    talla = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
    ], string='Talla')

    color = fields.Char(string='Color')
    stock = fields.Integer(string='Stock', default=0)
    descripcion = fields.Text(string='Descripción')
    disponibilidad = fields.Boolean(string='Disponible', default=True)

    categoria = fields.Selection([
        ('camiseta', 'Camiseta'),
        ('sudadera', 'Sudadera'),
        ('pantalon', 'Pantalón'),
        ('zapatillas', 'Zapatillas'),
        ('accesorio', 'Accesorio'),
    ], string='Categoría', required=True)

    imagen = fields.Binary(string='Imagen')
    fecha_anadido = fields.Date(
        string='Fecha de alta',
        default=fields.Date.today
    )
    ultima_actualizacion = fields.Datetime(
        string='Última actualización',
        default=fields.Datetime.now
    )


    valor_stock = fields.Float(
        string='Valor del stock',
        compute='_calcular_valor_stock',
        store=True
    )

    empleados_ids = fields.Many2many(
        'streetzone.empleado',
        relation='streetzone_empleado_producto_rel',
        column1='producto_id',
        column2='empleado_id',
        string='Empleados asignados'
    )



    @api.depends('precio', 'stock')
    def _calcular_valor_stock(self):
        for producto in self:
            producto.valor_stock = producto.precio * producto.stock

    @api.constrains('precio', 'stock')
    def _comprobar_precio_stock(self):
        for producto in self:
            if producto.precio < 0:
                raise ValidationError('El precio no puede ser negativo.')

            if producto.stock < 0:
                raise ValidationError('El stock no puede ser negativo.')
