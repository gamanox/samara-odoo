from odoo import http
from odoo.http import request
from odoo.exceptions import UserError

class ParishIntentionsController(http.Controller):

    @http.route(['/shop/intention/add'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def add_intention_to_cart(self, **post):
        # Get or create current website sale order
        order = request.website.sale_get_order(force_create=True)
        partner = request.env.user.partner_id or request.env.ref('base.public_partner')

        # Read form params
        product_id = post.get("product_id")
        if not product_id:
            raise UserError("Falta product_id en el formulario.")
        try:
            product_id = int(product_id)
        except:
            raise UserError("product_id inválido.")

        name = post.get("name") or ""
        message = post.get("message") or ""
        church = post.get("church") or "main"
        date_time = post.get("date_time")
        amount = post.get("amount")
        amount = float(amount) if amount else 0.0

        # Create the intention record
        vals = {
            "name": name,
            "partner_id": partner.id if partner and partner.id else request.env.ref("base.public_partner").id,
            "message": message,
            "church": church,
            "date_time": date_time,
            "amount": amount,
            "website_id": request.website.id,
            "state": "in_cart",
        }
        intention = request.env["parish.intention"].sudo().create(vals)

        # Add product to cart
        product = request.env["product.product"].browse(product_id)
        if not product.exists():
            raise UserError("Producto no encontrado.")
        res = order._cart_update(product_id=product.id, add_qty=1)
        line = request.env["sale.order.line"].browse(res.get("line_id"))
        # Link intention to the line and adjust name/price if needed
        line.sudo().write({
            "parish_intention_id": intention.id,
            "name": f"{product.display_name} — {name} @ {date_time}" if name or date_time else product.display_name,
            "price_unit": amount if amount and amount > 0 else line.price_unit,
        })
        intention.sudo().write({"sol_id": line.id})

        return request.redirect("/shop/cart")
