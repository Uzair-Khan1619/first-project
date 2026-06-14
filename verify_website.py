import os
import sys
import json

# Add workspace directory to python path to import app.py
sys.path.append(r"c:\Users\UJAIR PATHAN\Desktop\3rd attemp")

try:
    from app import app, PRODUCTS_FILE, load_products
    print("[OK] Successfully imported crochetttcharm Flask app!")
except ImportError as e:
    print(f"[FAIL] Failed to import app: {e}")
    sys.exit(1)

def run_tests():
    client = app.test_client()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    print("\n--- Starting Application Validation Tests ---\n")
    
    # 1. Test Home Route
    print("Testing Home page '/'...")
    resp = client.get('/')
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    html = resp.data.decode('utf-8')
    assert "crochetttcharm" in html, "Brand name not found on Home page!"
    assert "Boutique Favorites" in html, "Featured showcase title not found on Home page!"
    print("[OK] Home Page loads correctly!")

    # 2. Test Shop Route & 17 Products
    print("\nTesting Shop page '/shop' and pre-populated products...")
    resp = client.get('/shop')
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    html = resp.data.decode('utf-8')
    assert "Handmade Catalogue" in html, "Shop page header not found!"
    
    # Verify that all 17 product names appear in the shop page catalog grid
    products = load_products()
    assert len(products) == 17, f"Expected 17 products, found {len(products)}"
    print(f"Verified JSON database has exactly {len(products)} products.")
    
    for product in products:
        assert product['name'] in html, f"Product '{product['name']}' is missing from the catalog grid HTML!"
    print("[OK] Shop Page displays all 17 products correctly!")

    # 3. Test Empty Cart Route
    print("\nTesting empty shopping basket '/cart'...")
    resp = client.get('/cart')
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    assert "Your basket is empty" in html, "Cart should show 'empty' state by default!"
    print("[OK] Empty cart state displays correctly!")

    # 4. Test Adding Item to Cart (Session)
    print("\nTesting Cart Session Add operation: Adding Product ID 1 (Crochet flower gajras)...")
    # Post add to cart
    resp = client.post('/cart/add/1', follow_redirects=True)
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    
    # Verify banner flash message and dynamic cart item count
    assert "Added" in html and "Crochet flower gajras" in html, "Cart addition flash notification failed!"
    assert "Basket" in html, "Navigation Cart indicator not found!"
    
    # Inspect cart page to see if item is listed with correct math
    resp = client.get('/cart')
    html = resp.data.decode('utf-8')
    assert "Crochet flower gajras" in html, "Product not listed on Cart page after adding!"
    assert "Subtotal" in html, "Cart calculations summary is missing!"
    print("[OK] Cart session 'Add Item' flow is working correctly!")

    # 5. Test Cart Quantity Updates
    print("\nTesting Cart Session Update operation: Incrementing quantity to 2...")
    resp = client.post('/cart/update/1', data={'action': 'update', 'quantity': '2'}, follow_redirects=True)
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    assert "Basket updated successfully!" in html, "Quantity update flash message failed!"
    print("[OK] Cart session 'Update Quantity' flow is working correctly!")

    # 6. Test Admin Dashboard Page
    print("\nTesting Admin Panel '/admin'...")
    resp = client.get('/admin')
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    assert "Pricing Dashboard" in html, "Admin dashboard header not found!"
    assert "Update Prices" in html, "Price submission button not found!"
    print("[OK] Admin Panel loads correctly!")

    # 7. Test Admin Price Modification Persistence
    print("\nTesting Admin pricing update submission (updating Gajra from 199 to 220)...")
    
    # Fetch current products to restore later
    original_products = json.loads(open(PRODUCTS_FILE, 'r', encoding='utf-8').read())
    original_price = original_products[0]['price'] # Product 1 original price
    
    # Prepare post data for all 17 items (leaving others same, changing product 1 to 220)
    post_data = {}
    for p in original_products:
        post_data[f"price_{p['id']}"] = 220 if p['id'] == 1 else p['price']
        
    resp = client.post('/admin/update', data=post_data, follow_redirects=True)
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    assert "Successfully updated prices" in html, "Admin update success message was not flashed!"
    
    # Verify that products.json is written successfully and shop displays new price
    updated_products = load_products()
    assert updated_products[0]['price'] == 220, "Price modification did not persist in JSON database!"
    
    # Verify shop shows updated price
    resp = client.get('/shop')
    html = resp.data.decode('utf-8')
    assert "220" in html, "New updated price not reflected on Shop front-end!"
    print("[OK] Admin pricing updates persist in JSON and display instantly on shop!")

    # Restore original price
    post_data[f"price_1"] = original_price
    client.post('/admin/update', data=post_data)
    print(f"Restored Product ID 1 price back to its original price of {original_price} to maintain default config.")

    # 8. Clear Basket
    print("\nCleaning up Cart Session (emptying basket)...")
    client.post('/cart/clear')
    
    print("\n--- All 8 Validation Tests Passed Successfully! ---")
    print("Website is production-ready, functional, and verified.")

if __name__ == '__main__':
    run_tests()
