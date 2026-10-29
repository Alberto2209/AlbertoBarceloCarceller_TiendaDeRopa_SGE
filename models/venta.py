
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Venta(models.Model):
    _name = 'streetzone.venta'
    _description = 'Venta de StreetZone'
    _order = 'fecha desc'

    nombre = fields.Char(string='Referencia', required=True)

    fecha = fields.Date(string='Fecha de venta', default=fields.Date.today, required=True)

    empleado_ventas = fields.Many2one(
        'streetzone.empleado',
        string='Empleado',
        required=True
    )

    producto_ventas = fields.Many2one(
        'streetzone.producto',
        string='Producto',
        required=True
    )

    cantidad = fields.Integer( string='Cantidad', default=1, required=True)

    importe_total = fields.Float(
        string='Importe total',
        compute='_calcular_total',
        store=True
    )

    metodo_pago = fields.Selection([
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ], string='Método de pago', required=True)

    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', default='pendiente', required=True)

    observaciones = fields.Text(string='Observaciones')

    @api.depends('producto_ventas', 'producto_ventas.precio', 'cantidad')
    def _calcular_total(self):
        for venta in self:
            precio = (
                venta.producto_ventas.precio
                if venta.producto_ventas else 0.0
            )
            venta.importe_total = precio * venta.cantidad

    @api.constrains('cantidad')
    def _comprobar_cantidad(self):
        for venta in self:
            if venta.cantidad < 1:
                raise ValidationError(
                    'La cantidad debe ser como mínimo 1.'
                )

    
