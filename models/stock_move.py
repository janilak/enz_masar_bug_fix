from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.onchange('purchase_order_ids')
    def compute_move_ids_without_packages_purchase_advanced(self):
        if self.purchase_order_ids:
            move_list = []
            for orders in self.purchase_order_ids:
                for line in orders.order_line:
                    print(line.id)
                    if (line.product_qty - line.quantity_recieved) > 0:
                        move_line = (0, 0, {
                            'product_id': line.product_id.id,
                            'product_uom_qty': line.product_qty - line.quantity_recieved,
                            'product_uom': line.product_uom.id,
                            'company_id': self.company_id.id,
                            'date': self.scheduled_date,
                            'date_deadline': self.date_deadline,
                            'picking_code': self.picking_type_code,
                            'picking_id': self.id,
                            'partner_id': self.partner_id.id,
                            'picking_type_id': self.picking_type_id.id,
                            'location_id': self.location_id.id,
                            'location_dest_id': self.location_dest_id.id,
                            'purchase_line_id': line.id,
                            'purchase_advance_line_id': line._origin.id,
                            'name': line.name,
                            'enquiry_line_id': line.enquiry_line_id.id
                        })
                        move_list.append(move_line)
            if move_list:
                self.move_ids_without_package = None
                self.move_ids_without_package = move_list

    @api.onchange('sale_order_ids')
    def compute_move_ids_without_packages_sales_advanced(self):
        if self.sale_order_ids:
            move_list = []
            for orders in self.sale_order_ids:
                for line in orders.order_line:
                    if (line.product_uom_qty - line.quantity_delivered) > 0:
                        move_line = (0, 0, {
                            'product_id': line.product_id.id,
                            'product_uom_qty': line.product_uom_qty - line.quantity_delivered,
                            'product_uom': line.product_uom.id,
                            'company_id': self.company_id.id,
                            'date': self.scheduled_date,
                            'date_deadline': self.date_deadline,
                            'picking_code': self.picking_type_code,
                            'picking_id': self.id,
                            'partner_id': self.partner_id.id,
                            'picking_type_id': self.picking_type_id.id,
                            'location_id': self.location_id.id,
                            'location_dest_id': self.location_dest_id.id,
                            'sale_line_id': line.id,
                            'sale_advance_line_id': line._origin.id,
                            'name': line.name,
                            'enquiry_line_id': line.enquiry_line_id.id,
                            # 'sale_id':line.order_id.id,
                        })
                        move_list.append(move_line)
            if move_list:
                self.move_ids_without_package = None
                self.move_ids_without_package = move_list
                self.sale_id = self.sale_order_ids[-1].id