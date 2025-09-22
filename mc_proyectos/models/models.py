# -- coding: utf-8 --

from odoo import models, fields, api
from odoo.exceptions import UserError

class mc_proyectos(models.Model):
    _inherit = 'sale.order'
    _description = 'sale.order'

    # Campo computado para mostrar todos los registros de mrp.bom
    bom_ids = fields.Many2many('mrp.bom', string="Lista de materiales")


    # Funcion para generar el albaran de los registros seleccionados y restar el costo al margen bruto
    def action_generate_albaran(self):
        select_boms = self.bom_ids.filtered(lambda bom: bom.is_selected)
        if not select_boms:
            raise UserError("Error. Seleccionar al menos un registro de lista de materiales en página Insumos.")
        
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        if not picking_type:
            raise UserError("No se encontró un tipo de operación de salida.")
        
        picking_value = {
            'partner_id': self.partner_id.id,
            'location_id': self.env.ref('stock.stock_location_stock').id,   
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            'picking_type_id': picking_type.id,
            'origin': self.name,
        }
        picking = self.env['stock.picking'].create(picking_value)

        total_bom_cost = 0.0

        for bom in select_boms:
            # Crear el movimiento de stock para el kit
            move_values = {
                'picking_id': picking.id,
                'product_id': bom.product_tmpl_id.product_variant_id.id,
                'product_uom_qty': 1.0,
                'product_uom': bom.product_tmpl_id.uom_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                'name': bom.product_tmpl_id.name,
            }
            self.env['stock.move'].create(move_values)

            # Calcular el costo total del kit
            for line in bom.bom_line_ids:
                product_cost = line.product_id.standard_price * line.product_qty
                total_bom_cost += product_cost

        # Crear el registro en la cuenta analitica y reflajar el coste total de los kits
        if self.analytic_account_id:
            self.env['account.analytic.line'].create({
                'account_id': self.analytic_account_id.id,
                'name': "Costo de materiales - Albarán {picking.name}",
                'amount': -total_bom_cost, 
                'ref': picking.name,       # Numero del albaran 
                'unit_amount': len(select_boms),  # Cantidad de kits seleccionados
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'res_id': picking.id,
            'target': 'current',
        }
class MrpBomInherit(models.Model): 
    _inherit = "mrp.bom"
    _description = "mrp.bom"

    #Campo y relacion para el modelo sale.order y poder seleccionar los kits 
    sale_order_id = fields.Many2one('sale.order', string="Orden de venta")
    is_selected = fields.Boolean(string="Seleccionar", default=True)

#:)