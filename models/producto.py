from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Producto(models.Model):
    # Establecemos el nombre y la descripción
    _name = 'streetzone.producto'
    _description = 'Producto de StreetZone'

    nombre = fields.Char(string='Nombre', required=True)
    # Un float para el precio, empieza en 0
    precio = fields.Float(string='Precio', required=True, default=0.0)
    # Desplegable de tallas
    talla = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL')
    ], string='Talla')
    color = fields.Char(string='Color')
    # Cuántas unidades quedan, por defecto 0
    stock = fields.Integer(string='Stock', default=0)
    descripcion = fields.Text(string='Descripcion')
    # Boolean para saber si sigue disponible o no
    disponibilidad = fields.Boolean(string='Disponible', default=True)
    # Desplegable del tipo de ropa que es
    categoria = fields.Selection([
        ('camiseta', 'Camiseta'),
        ('sudadera', 'Sudadera'),
        ('pantalon', 'Pantalon'),
        ('zapatillas', 'Zapatillas'),
        ('accesorio', 'Accesorio')
    ], string='Categoria', required=True)
    # Binary, que sirve para poder subir una foto del producto
    imagen = fields.Binary(string='Imagen')
    # Fecha en la que se añadió (hoy por defecto)
    fecha_anadido = fields.Date(string='Fecha de alta', default=fields.Date.today)
    # Fecha y hora de la última vez que se tocó (ahora por defecto)
    ultima_actualizacion = fields.Datetime(string='Ultima actualizacion', default=fields.Datetime.now)

    # Valor_stock se calcula solo
    valor_stock = fields.Float(string='Valor del stock', compute='_calcular_valor_stock', store=True)

    # Muchos productos con muchos empleados. Misma tabla que en empleado.py pero al revés
    empleados_ids = fields.Many2many('streetzone.empleado', relation='streetzone_empleado_producto_rel', column1='producto_id', column2='empleado_id', string='Empleados asignados')

    # Se recalcula cuando cambia el precio o el stock
    @api.depends('precio', 'stock')
    def _calcular_valor_stock(self):
        # Recorremos todos los productos que se están modificando
        for producto in self:
            # Calculamos el valor total del stock 
            producto.valor_stock = producto.precio * producto.stock


    # Comprueba que el precio y el stock sean valores válidos al guardar
    @api.constrains('precio', 'stock')
    def _comprobar_precio_stock(self):
        # Recorremos todos los productos
        for producto in self:
            # Comprobamos que el precio no sea negativo
            if producto.precio < 0:

                # Si es negativo, mostramos un error 
                raise ValidationError('El precio no puede ser negativo.')
            # Comprobamos que el stock no sea negativo
            if producto.stock < 0:
                #Si es negativo, mostramos un error 
                raise ValidationError('El stock no puede ser negativo.')

            