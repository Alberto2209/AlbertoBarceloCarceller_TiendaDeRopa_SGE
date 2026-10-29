
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Empleado(models.Model):
    _name = 'streetzone.empleado'
    _description = 'Empleado de StreetZone'

    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    dni = fields.Char(string='DNI', required=True)
    telefono = fields.Char(string='Teléfono')
    correo = fields.Char(string='Correo electrónico')

    puesto = fields.Selection([
        ('dependiente', 'Dependiente'),
        ('encargado', 'Encargado'),
        ('almacen', 'Personal de almacén'),
    ], string='Puesto', required=True)

    fecha_contratacion = fields.Date(
        string='Fecha de contratación',
        default=fields.Date.today
    )

    activo = fields.Boolean(string='Empleado activo', default=True)
    descripcion = fields.Text(string='Descripcion')

    ventas_realizadas = fields.One2many(
    'streetzone.venta',
    'empleado_ventas',
    string='Ventas realizadas'
)

    productos_asignados = fields.Many2many(
        'streetzone.producto',
        relation='streetzone_empleado_producto_rel',
        column1='empleado_id',
        column2='producto_id',
        string='Productos asignados'
    )

    @api.constrains('correo')
    def _comprobar_correo(self):
        for empleado in self:
            if empleado.correo and '@' not in empleado.correo:
                raise ValidationError(
                    'Introduce un correo electrónico válido.'
                )
