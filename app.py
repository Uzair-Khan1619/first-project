import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'crochetttcharm_cozy_yarn_secret_key_2026'

# Products JSON File
PRODUCTS_FILE = os.path.join(app.root_path, 'products.json')


# =========================
# LOAD PRODUCTS
# =========================
def load_products():
    """Load products from products.json or create default products."""

    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            app.logger.error(f"Error reading products.json: {e}")

    # Default Products
    default_products = [
        {
            "id": 1,
            "name": "Crochet flower gajras",
            "category": "Hair Accessories",
            "price": 199,
            "description": "Traditional elegance reimagined with delicate crochet flowers for timeless grace.",
            "image": "/static/Images/pearl-gajra.jpg"
        },
        {
            "id": 2,
            "name": "Tulip + Lily Bouquet",
            "category": "Bouquet",
            "price": 600,
            "description": "A dreamy fusion of tulips and lilies, handcrafted to capture spring's gentle essence forever.",
            "image": "/static/Images/tulip-lily-bouquet.jpg"
        },
        {
            "id": 3,
            "name": "Rose + Tulip Bouquet",
            "category": "Bouquet",
            "price": 600,
            "description": "Romantic roses meet elegant tulips in this timeless bouquet that never wilts or fades.",
            "image": "/static/Images/rose-tulip-bouquet.jpg"
        },
        {
            "id": 4,
            "name": "Chocolate Bouquet",
            "category": "Bouquet",
            "price": 400,
            "description": "Sweet indulgence meets floral beauty in this charming chocolate-inspired bouquet creation.",
            "image": "/static/Images/chocolate-bouquet.jpg"
        },
        {
            "id": 5,
            "name": "Lily Bouquet",
            "category": "Bouquet",
            "price": 400,
            "description": "Delicate lily blooms in soft pastels, eternally preserved through intricate crochet artistry.",
            "image": "/static/Images/lily-bouquet.jpg"
        },
        {
            "id": 6,
            "name": "Phone Case",
            "category": "Phone Cases",
            "price": 350,
            "description": "Wrap your phone in cozy handmade charm with soft, cushioned crochet protection.",
            "image": "/static/Images/phone-case.jpg"
        },
        {
            "id": 7,
            "name": "Crochet T-Shirt",
            "category": "T-Shirts",
            "price": 1200,
            "description": "Boho-chic wearable art featuring intricate crochet patterns that make a statement.",
            "image": "/static/Images/crochet-tshirt.jpg"
        },
        {
            "id": 8,
            "name": "Rose Keychain",
            "category": "Keychains",
            "price": 150,
            "description": "Carry a tiny bloom wherever you go with this adorable mini rose keychain companion.",
            "image": "/static/Images/rose-keychain.jpg"
        },
        {
            "id": 9,
            "name": "Letter Keychain",
            "category": "Keychains",
            "price": 150,
            "description": "Personalized keychain charm featuring your initial, lovingly crafted in soft pastel hues.",
            "image": "/static/Images/letter-keychain.jpg"
        },
        {
            "id": 10,
            "name": "Rose Bag",
            "category": "Bags",
            "price": 999,
            "description": "Luxurious garden-inspired bag adorned with blooming roses, perfect for romantic outings.",
            "image": "/static/Images/rose-bag.jpg"
        },
        {
            "id": 11,
            "name": "Bow Clip",
            "category": "Hair Accessories",
            "price": 180,
            "description": "Sweet bow accent hair clip crafted to add a touch of whimsy and charm to any hairstyle.",
            "image": "/static/Images/bow-clip.jpg"
        },
        {
            "id": 12,
            "name": "Hair Clips Set",
            "category": "Hair Accessories",
            "price": 150,
            "description": "Dainty hair clips that blend functionality with handmade artistry and pastel softness.",
            "image": "/static/Images/bow-clip.jpg"
        },
        {
            "id": 13,
            "name": "Cozy Bloom Hamper",
            "category": "Hampers",
            "price": 1499,
            "description": "A premium gift hamper filled with assorted crochet flowers, a keychain, and a mini basket.",
            "image": "/static/Images/rose-bag.jpg"
        },
        {
            "id": 14,
            "name": "Daisy Ring",
            "category": "Jewelry",
            "price": 120,
            "description": "An elegant, delicate crochet daisy ring that sits comfortably and adds a vintage touch.",
            "image": "/static/Images/bow-clip.jpg"
        },
        {
            "id": 15,
            "name": "Cute Peach Keychain",
            "category": "Keychains",
            "price": 140,
            "description": "Adorable soft plush peach keychain, hand-stitched with vibrant yarn and green leaves.",
            "image": "/static/Images/rose-keychain.jpg"
        },
        {
            "id": 16,
            "name": "Strawberry Phone Case",
            "category": "Phone Cases",
            "price": 380,
            "description": "Cozy phone case adorned with cute mini crochet strawberries for a sweet, playful look.",
            "image": "/static/Images/phone-case.jpg"
        },
        {
            "id": 17,
            "name": "Custom Monogram Banner",
            "category": "Custom Gifts",
            "price": 899,
            "description": "Personalized wall hanging banner hand-crocheted with your custom name or initial.",
            "image": "/static/Images/letter-keychain.jpg"
        }
    ]

    save_products(default_products)
    return default_products


# =========================
# SAVE PRODUCTS
# =========================
def save_products(products):
    """Save products to JSON."""
    try:
        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=4, ensure_ascii=False)
    except Exception as e:
        app.logger.error(f"Error writing products.json: {e}")


# =========================
# CONTEXT PROCESSOR
# =========================
@app.context_processor
def utility_processor():

    def get_cart_count():
        cart = session.get('cart', {})
        return sum(cart.values())

    return dict(cart_count=get_cart_count)


# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():

    products = load_products()

    featured = [p for p in products if p['id'] in [1, 2, 10]]

    return render_template(
        'home.html',
        featured=featured
    )


# =========================
# SHOP PAGE
# =========================
@app.route('/shop')
def shop():

    products = load_products()

    categories = sorted(list(set(p['category'] for p in products)))

    selected_category = request.args.get('category', '').strip()

    search_query = request.args.get('search', '').strip().lower()

    filtered_products = products

    if selected_category:
        filtered_products = [
            p for p in filtered_products
            if p['category'] == selected_category
        ]

    if search_query:
        filtered_products = [
            p for p in filtered_products
            if search_query in p['name'].lower()
            or search_query in p['description'].lower()
        ]

    return render_template(
        'shop.html',
        products=filtered_products,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query
    )


# =========================
# CART PAGE
# =========================
@app.route('/cart')
def cart():

    cart_session = session.get('cart', {})

    products = load_products()

    cart_items = []

    subtotal = 0

    total_quantity = 0

    prod_map = {str(p['id']): p for p in products}

    for pid, qty in list(cart_session.items()):

        if pid in prod_map and qty > 0:

            product = prod_map[pid]

            item_total = product['price'] * qty

            subtotal += item_total

            total_quantity += qty

            cart_items.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'image': product['image'],
                'description': product['description'],
                'category': product['category'],
                'quantity': qty,
                'total': item_total
            })

    shipping_charge = 0 if subtotal >= 999 or subtotal == 0 else 60

    grand_total = subtotal + shipping_charge

    return render_template(
        'cart.html',
        cart_items=cart_items,
        subtotal=subtotal,
        total_quantity=total_quantity,
        shipping_charge=shipping_charge,
        grand_total=grand_total
    )


# =========================
# ADD TO CART
# =========================
@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):

    products = load_products()

    product = next(
        (p for p in products if p['id'] == product_id),
        None
    )

    if not product:
        flash("Product not found!", "error")
        return redirect(url_for('shop'))

    if 'cart' not in session:
        session['cart'] = {}

    cart_session = session['cart']

    str_pid = str(product_id)

    cart_session[str_pid] = cart_session.get(str_pid, 0) + 1

    session.modified = True

    flash(
        f"✨ Added '{product['name']}' to your basket!",
        "success"
    )

    next_page = request.referrer or url_for('shop')

    return redirect(next_page)


# =========================
# UPDATE CART
# =========================
@app.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):

    action = request.form.get('action')

    str_pid = str(product_id)

    if 'cart' not in session or str_pid not in session['cart']:
        flash("Item not found in your cart!", "error")
        return redirect(url_for('cart'))

    if action == 'remove':

        session['cart'].pop(str_pid, None)

        session.modified = True

        flash("Item removed from your basket.", "info")

    elif action == 'update':

        try:
            qty = int(request.form.get('quantity', 1))

            if qty <= 0:
                session['cart'].pop(str_pid, None)
                flash("Item removed from your basket.", "info")

            else:
                session['cart'][str_pid] = qty
                flash("Basket updated successfully!", "success")

            session.modified = True

        except ValueError:
            flash("Invalid quantity value!", "error")

    return redirect(url_for('cart'))


# =========================
# CLEAR CART
# =========================
@app.route('/cart/clear', methods=['POST'])
def clear_cart():

    session.pop('cart', None)

    flash("Your shopping basket is now empty.", "info")

    return redirect(url_for('cart'))


# =========================
# ADMIN PAGE
# =========================
@app.route('/admin')
def admin():

    products = load_products()

    return render_template(
        'admin.html',
        products=products
    )


# =========================
# UPDATE PRICES
# =========================
@app.route('/admin/update', methods=['POST'])
def update_prices():

    products = load_products()

    updated_count = 0

    for product in products:

        field_name = f"price_{product['id']}"

        if field_name in request.form:

            try:
                new_price = int(request.form[field_name])

                if new_price < 0:
                    flash(
                        f"Price for '{product['name']}' cannot be negative!",
                        "error"
                    )
                    return redirect(url_for('admin'))

                if product['price'] != new_price:
                    product['price'] = new_price
                    updated_count += 1

            except ValueError:

                flash(
                    f"Invalid price entered for '{product['name']}'!",
                    "error"
                )

                return redirect(url_for('admin'))

    if updated_count > 0:

        save_products(products)

        flash(
            f"🎉 Successfully updated prices for {updated_count} product(s)!",
            "success"
        )

    else:
        flash(
            "No price modifications were detected.",
            "info"
        )

    return redirect(url_for('admin'))


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)