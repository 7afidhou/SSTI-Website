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
