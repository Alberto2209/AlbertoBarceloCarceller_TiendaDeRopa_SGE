from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Empleado(models.Model):
    # Establecemos el nombre y la descripción
    _name = 'streetzone.empleado'
    _description = 'Empleado de StreetZone'

    # Campos de texto basicos, con required=True es obligatorio rellenarlo
    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    dni = fields.Char(string='DNI', required=True)
    # Estos dos son opcionales
    telefono = fields.Char(string='Telefono')
    correo = fields.Char(string='Correo')

    # Desplegable para elegir el puesto 
    puesto = fields.Selection([
        ('dependiente', 'Dependiente'),
        ('encargado', 'Encargado'),
        ('almacen', 'Almacen')
    ], string='Puesto', required=True)

    # Fecha de contratación, por defecto pone la de hoy
    fecha_contratacion = fields.Date(string='Fecha contratacion', default=fields.Date.today)
    # Casilla boolean para saber si sigue activo en el trabajo
    activo = fields.Boolean(string='Activo', default=True)
    # Text para escribir notas largas
    descripcion = fields.Text(string='Descripcion')

    # Un empleado puede tener muchas ventas (se enlaza con el campo empleado_ventas de venta.py)
    ventas_realizadas = fields.One2many('streetzone.venta', 'empleado_ventas', string='Ventas')
    # Muchos empleados con muchos productos, con una tabla en medio para guardarlo
    # En producto.py se pone lo mismo pero al revés
    productos_asignados = fields.Many2many('streetzone.producto', relation='streetzone_empleado_producto_rel', column1='empleado_id', column2='producto_id', string='Productos')

    # Indica a Odoo que esta función debe ejecutarse cuando se modifique el campo 'correo' 
    @api.constrains('correo')

    # Definimos una función llamada comprobar_correo.
    # 'self' contiene los registros que Odoo tiene que comprobar.
    def comprobar_correo(self):

        # any compurueba si al menos uno cumple la condición del @ 
        # recorriendo todos los registros viendo, si el correo k esta mirando la cumple
        # si no tiene un @ se ejecuta el error
        if any('@' not in e.correo for e in self if e.correo):

            # Lanza un error mostrando el mensaje 'Correo incorrecto'.
            raise ValidationError('Correo incorrecto')