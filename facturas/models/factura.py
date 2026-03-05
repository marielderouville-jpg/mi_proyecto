from odoo import models, fields, api
from datetime import datetime


class FacturaFactura(models.Model):
    _name = 'facturas.factura'
    _description = 'Factura'
    _order = 'fecha desc'

    # Campos principales
    cliente_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True,
        help='Selecciona el cliente para esta factura'
    )
    
    fecha = fields.Date(
        string='Fecha de Factura',
        default=lambda self: fields.Date.context_today(self),
        required=True,
        help='Fecha en la que se emite la factura'
    )
    
    # Relación One2many con las líneas de factura
    lineas_ids = fields.One2many(
        'facturas.factura.linea',
        'factura_id',
        string='Líneas de Factura',
        help='Productos incluidos en esta factura'
    )
    
    # Campos calculados
    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True,
        help='Total de la factura'
    )
    
    cantidad_lineas = fields.Integer(
        string='Cantidad de Líneas',
        compute='_compute_cantidad_lineas',
        store=True,
        help='Número de líneas en la factura'
    )
    
    estado = fields.Selection(
        [
            ('borrador', 'Borrador'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada'),
        ],
        string='Estado',
        default='borrador',
        help='Estado actual de la factura'
    )

    @api.depends('lineas_ids.subtotal')
    def _compute_total(self):
        """Calcula el total de la factura sumando el subtotal de las líneas"""
        for factura in self:
            factura.total = sum(linea.subtotal for linea in factura.lineas_ids)

    @api.depends('lineas_ids')
    def _compute_cantidad_lineas(self):
        """Calcula la cantidad de líneas en la factura"""
        for factura in self:
            factura.cantidad_lineas = len(factura.lineas_ids)

    def action_confirmar(self):
        """Acción para confirmar la factura"""
        self.estado = 'confirmada'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Éxito',
                'message': 'Factura confirmada correctamente',
                'type': 'success',
            }
        }

    def action_cancelar(self):
        """Acción para cancelar la factura"""
        self.estado = 'cancelada'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Éxito',
                'message': 'Factura cancelada correctamente',
                'type': 'success',
            }
        }