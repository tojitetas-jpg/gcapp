from flask import Flask

app = Flask(__name__)


# ----------------------------
# FUNCIÓN AUXILIAR
# ----------------------------
def load_html(file):
    with open(f"templates/{file}", "r", encoding="utf-8") as f:
        return f.read()

# --------------------
# HOME
# --------------------
@app.route("/")
def home():
    return load_html("index.html")

# --------------------
# ALL PRODUCTS
# --------------------
@app.route("/products")
def products():
    return load_html("products.html")


# --------------------
# PRODUCT TEMPLATE
# --------------------
@app.route("/product/<id>")
def product(id):
    html = load_html("product.html")

    # mostrar id en la pagina
    html = html.replace("{{product_id}}", str(id))

    return html


# --------------------
# RUN SERVER
# --------------------
if __name__ == "__main__":
    app.run(debug=True)