from flask import Flask, request, render_template_string, render_template, redirect, url_for

app = Flask(__name__)

# Dummy user database (in-memory)
users = {
    "admin": {"name": "Admin", "bio": "I am the site administrator."},
    "h4f1d0$": {"name": "h4f1d0$", "bio": "I love hacking stuff!"},
}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form.get("username", "Guest")
        bio = request.form.get("bio", "No bio provided")
        
        # 🚨 SSTI Vulnerability 🚨
        template = f"<h2>Profile of {username}</h2><p>Bio: {bio}</p>"
        return render_template_string(template)

    return render_template("profile.html")

if __name__ == '__main__':
    app.run(debug=True)
# from flask import Flask, render_template_string, request

# app = Flask(__name__)

# # Dummy product catalog
# products = {
#     1: {"name": "Laptop", "price": 1200},
#     2: {"name": "Phone", "price": 800},
#     3: {"name": "Headphones", "price": 150},
# }

# @app.route('/')
# def home():
#     return """
#     <html>
#     <head><link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'></head>
#     <body class='container text-center'>
#         <h1 class='mt-5'>Welcome to the Flask E-commerce Store</h1>
#         <a href='/products' class='btn btn-primary mt-3'>View Products</a>
#     </body>
#     </html>
#     """

# @app.route('/products')
# def list_products():
#     product_list = "".join([f"<li class='list-group-item'><a href='/product/{pid}' class='text-decoration-none'>{p['name']} - ${p['price']}</a></li>" for pid, p in products.items()])
#     return f"""
#     <html>
#     <head><link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'></head>
#     <body class='container'>
#         <h2 class='mt-5'>Products</h2>
#         <ul class='list-group mt-3'>{product_list}</ul>
#         <a href='/' class='btn btn-secondary mt-3'>Back</a>
#     </body>
#     </html>
#     """

# # SSTI Vulnerable Route
# @app.route('/product/<product_id>')
# def product_detail(product_id):
#     product = products.get(int(product_id))
#     if not product:
#         return "Product not found", 404
    
#     template = """
#     <html>
#     <head><link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'></head>
#     <body class='container'>
#         <h2 class='mt-5'>{{ product.name }}</h2>
#         <p class='lead'>Price: ${{ product.price }}</p>
#         <p class='text-muted'>Description: {{ description }}</p>
#         <a href='/products' class='btn btn-secondary mt-3'>Back</a>
#     </body>
#     </html>
#     """
    
#     # Injecting user-controlled description (SSTI Vulnerability)
#     description = request.args.get('desc', 'No description available')
#     return render_template_string(template, product=product, description=description)

# @app.route('/checkout')
# def checkout():
#     return """
#     <html>
#     <head><link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'></head>
#     <body class='container text-center'>
#         <h2 class='mt-5'>Checkout Page</h2>
#         <p>Feature coming soon!</p>
#         <a href='/' class='btn btn-secondary mt-3'>Back</a>
#     </body>
#     </html>
#     """

# if __name__ == '__main__':
#     app.run(debug=True)