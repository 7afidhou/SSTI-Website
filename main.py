from flask import Flask, request, render_template_string, session, redirect, url_for,render_template

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Fake user database
users = {"admin": "adminpass", "user": "userpass"}

# Fake product database
products = {
    1: {"name": "Laptop", "price": 1000, "image": "https://cdn.thewirecutter.com/wp-content/media/2024/11/BEST-WINDOWS-ULTRABOOKS-2048px-5681.jpg"},
    2: {"name": "Smartphone", "price": 500, "image": "https://im.qccdn.fr/node/guide-d-achat-smartphones-4203/inline-105192.jpg"},
    3: {"name": "Headphones", "price": 100, "image": "https://cdn.thewirecutter.com/wp-content/media/2023/07/bluetoothheadphones-2048px-6135-1.jpg?auto=webp&quality=75&crop=1.91:1&width=1200"}
}

# Admin message (Vulnerable to SSTI)
admin_message = "Welcome to our store!"  # Will be evaluated inside render_template_string()

@app.route("/", methods=["GET"])
def home():
    global admin_message
    return render_template_string(
        """ 
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>E-Shop</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        </head>
        <body>
            <nav class="navbar navbar-dark bg-dark p-3">
                <a class="navbar-brand text-light" href="#">🛒 E-Shop</a>
                <div>
                    {% if 'username' in session %}
                        <span class="text-light">Logged in as {{ session['username'] }}</span>
                        <a href="/logout" class="btn btn-outline-light ms-2">Logout</a>
                    {% else %}
                        <a href="/login" class="btn btn-outline-light">Login</a>
                    {% endif %}
                </div>
            </nav>

            <div class="container mt-4">
                <h1 class="mb-3">🛒 Welcome to E-Shop</h1>
                <p class="alert alert-info">""" + admin_message + """</p>  <!-- ⚠️ Now Vulnerable -->

                <div class="row">
                    {% for id, product in products.items() %}
                        <div class="col-md-4">
                            <div class="card">
                                <img src="{{ product.image }}" class="card-img-top" alt="Product Image" height="200">
                                <div class="card-body">
                                    <h5 class="card-title">{{ product.name }}</h5>
                                    <p class="card-text">${{ product.price }}</p>
                                    <a href="/buy/{{ id }}" class="btn btn-primary">Buy Now</a>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            </div>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """,
        session=session, products=products  # Passing session so Jinja can access it
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if users.get(username) == password:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"

    return render_template_string("""
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h1 class="mb-3">🔑 Login</h1>
        <form method="post">
            <label class="form-label">Username:</label>
            <input type="text" name="username" class="form-control mb-3">
            <label class="form-label">Password:</label>
            <input type="password" name="password" class="form-control mb-3">
            <input type="submit" value="Login" class="btn btn-primary">
        </form>
    </div>
</body>
</html>
    """)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

@app.route("/buy/<int:product_id>")
def buy(product_id):
    if "username" not in session:
        return "You must be logged in to buy. <a href='/login'>Login</a>"

    product = products.get(product_id)
    if product:
        return f"Thank you for buying {product['name']} for ${product['price']}!"
    return "Product not found."

@app.route("/admin", methods=["GET", "POST"])
def admin():
    global admin_message
    if "username" not in session or session["username"] != "admin":
        return "Access Denied!"

    if request.method == "POST":
        admin_message = request.form.get("message", "Welcome!")  # ⚠️ Directly Assigning User Input

    return render_template("admin.html", admin_message=admin_message)

if __name__ == "__main__":
    app.run(debug=True)
