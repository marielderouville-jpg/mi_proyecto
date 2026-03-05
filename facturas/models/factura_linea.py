from odoo import models, fields, api


class FacturaFacturaLinea(models.Model):
    _name = 'facturas.factura.linea'
    _description = 'Línea de Factura'
    _order = 'sequence, id'

    # Relación con la factura principal
    factura_id = fields.Many2one(
        'facturas.factura',
        string='Factura',
        required=True,
        ondelete='cascade',
        help='Factura a la que pertenece esta línea'
    )

    # Producto
    producto_id = fields.Many2one(
        'product.product',
        string='Producto',
        required=True,
        help='Selecciona el producto'
    )

    # Cantidad
    cantidad = fields.Float(
        string='Cantidad',
        default=1.0,
        required=True,
        help='Cantidad del producto'
    )

    # Precio unitario
    precio = fields.Float(
        string='Precio Unitario',
        required=True,
        help='Precio por unidad del producto'
    )

    # Subtotal calculado
    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
        help='Subtotal de la línea (cantidad × precio)'
    )

    # Orden de visualización
    sequence = fields.Integer(
        string='Orden',
        default=10,
        help='Orden de visualización de las líneas'
    )

    # Descripción adicional (opcional)
    descripcion = fields.Text(
        string='Descripción',
        help='Descripción adicional del producto'
    )

    @api.depends('cantidad', 'precio')
    def _compute_subtotal(self):
        """Calcula el subtotal de la línea"""
        for linea in self:
            linea.subtotal = linea.cantidad * linea.precio

    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        """Cuando se selecciona un producto, trae su información"""
        if self.producto_id:
            # Asigna la descripción del producto
            self.descripcion = self.producto_id.description or self.producto_id.name
            # Asigna el precio de venta del producto
            if self.producto_id.list_price:
                self.precio = self.producto_id.list_price