from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Venta(models.Model):
    # Nombre y descripción
    _name = 'streetzone.venta'
    _description = 'Venta de StreetZone'
    # Las ventas salen ordenadas de la más nueva a la más vieja
    _order = 'fecha desc'

    # Un nombre para la referencia
    nombre = fields.Char(string='Referencia', required=True)
    # Fecha de la venta (hoy por defecto)
    fecha = fields.Date(string='Fecha de venta', default=fields.Date.today, required=True)
    # Cada venta la hace un solo empleado 
    empleado_ventas = fields.Many2one('streetzone.empleado', string='Empleado', required=True)
    # Cada venta es de un solo producto
    producto_ventas = fields.Many2one('streetzone.producto', string='Producto', required=True)
    # Cuántas unidades se venden (mínimo y por defecto 1)
    cantidad = fields.Integer(string='Cantidad', default=1, required=True)
    # El importe total se calcula solo
    importe_total = fields.Float(string='Importe total', compute='_calcular_total', store=True)

    # Desplegable de cómo paga el cliente
    metodo_pago = fields.Selection([
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia')
    ], string='Metodo de pago', required=True)

    # Desplegable de cómo va la venta, empieza en pendiente
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ], string='Estado', default='pendiente', required=True)

    # Un texto para observaciones
    observaciones = fields.Text(string='Observaciones')


    # Se recalcula si cambia el producto, su precio o la cantidad
    @api.depends('producto_ventas', 'producto_ventas.precio', 'cantidad')
    def _calcular_total(self):
        # Recorremos todos las vengtas
        for venta in self:
            # Si hay producto, multiplicamos precio por cantidad
            if venta.producto_ventas:
                venta.importe_total = venta.producto_ventas.precio * venta.cantidad
            # Si no hay producto, el total es 0
            else:
                venta.importe_total = 0.0

    # No dejamos vender menos de 1 unidad
    @api.constrains('cantidad')
    def _comprobar_cantidad(self):
        for venta in self:
            # Comprobamos que no haya stock
            if venta.cantidad < 1:
                #Si no hay stock mostramos un error 
                raise ValidationError('La cantidad debe ser como minimo 1.')