from flask import Flask, request, render_template, redirect, url_for, session

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
admin_message = "Welcome to our store!"

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", admin_message=admin_message, products=products)

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

    return render_template("login.html")

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
        admin_message = request.form.get("message", "Welcome!")  # ⚠️ SSTI Vulnerability

    return render_template("admin.html", admin_message=admin_message)

if __name__ == "__main__":
    app.run(debug=True)
