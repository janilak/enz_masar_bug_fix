from odoo import fields,models,api


class RfqComparison(models.TransientModel):
    _inherit = 'rfq.comparison'

    @api.onchange('enquiry_id')
    def compute_comparison_lines(self):
        res = super(RfqComparison, self).compute_comparison_lines()
        for p_line in self.comparison_lines:
            p_line.lowest = False
        products = self.comparison_lines.mapped('product_id')
        for product in products:
            price = self.comparison_lines.filtered(
                lambda product_line: product_line.product_id.id == product.id).mapped('landed_cost')
            price = [num for num in price if num != 0]
            if price:
                lowest = min(price)
                for line in self.comparison_lines:
                    if line.product_id.id == product.id:
                        if lowest == line.landed_cost:
                            line.lowest = True
            else:
                for line in self.comparison_lines:
                    if line.product_id.id == product.id:
                        line.lowest = False
        return res