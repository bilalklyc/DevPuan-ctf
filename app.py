import os
import sqlite3
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "devpuan_ctf_gizli_anahtar_v2"

DB_PATH = "devpuan.db"

FLAG1 = "TUGA{st4jy3r_4hm3t_c30_r0z3t1n1_k4pt1_981a}"
FLAG2 = "TUGA{sql1_1l3_c30_y3tk1s1_v3_m44s_ucuruldu_77b}"

PRODUCTS = [
    {
        "id": 1,
        "name": "DevPuan Şirket Logolu Kupa",
        "description": "Ofiste filtre kahve içerken motivasyon sağlayan stajyer kupası.",
        "price": 20,
        "badge": "Standart",
    },
    {
        "id": 2,
        "name": "Cuma Günü 1 Saat Erken Çıkış İzni",
        "description": "Trafik başlamadan önce kaçmak isteyenlere özel.",
        "price": 50,
        "badge": "Popüler",
    },
    {
        "id": 3,
        "name": "Mekanik Klavye Switch Seti",
        "description": "Ofisteki herkesin duyacağı kadar ses çıkaran Blue switchler.",
        "price": 100,
        "badge": "Tükendi Gibi",
    },
    {
        "id": 4,
        "name": "CEO Odası Giriş Kartı & Kapı Şifresi",
        "description": "Şirketin en tepesine giriş bileti. Kapı şifresi satın alım sonrası teslim edilir.",
        "price": 1000000,
        "badge": "Erişilemez",
    },
]


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_code TEXT UNIQUE,
            name TEXT,
            role TEXT,
            salary INTEGER,
            is_real_ceo INTEGER DEFAULT 0
        )
    """)
    cursor.execute("DELETE FROM employees")
    cursor.execute(
        "INSERT INTO employees (emp_code, name, role, salary, is_real_ceo) VALUES"
        " ('EMP104', 'Ahmet Kaya (Stajyer)', 'Intern', 17002, 0)"
    )
    cursor.execute(
        "INSERT INTO employees (emp_code, name, role, salary, is_real_ceo) VALUES"
        " ('EMP001', 'Kerem Bey (Şirket Kurucusu)', 'CEO', 950000, 1)"
    )
    cursor.execute(
        "INSERT INTO employees (emp_code, name, role, salary, is_real_ceo) VALUES"
        " ('EMP002', 'Banu Hanım (İK Direktörü)', 'HR Director', 320000, 0)"
    )
    conn.commit()
    conn.close()


init_db()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_user_session():
    if "balance" not in session:
        session["balance"] = 50
    if "cart" not in session:
        session["cart"] = []
    if "has_ceo_door_code" not in session:
        session["has_ceo_door_code"] = False
    if "passed_ceo_door" not in session:
        session["passed_ceo_door"] = False


@app.before_request
def setup():
    init_user_session()


@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM employees WHERE emp_code = 'EMP104'")
    ahmet = cursor.fetchone()
    db.close()
    return render_template(
        "index.html",
        products=PRODUCTS,
        balance=session.get("balance", 50),
        has_ceo_door_code=session.get("has_ceo_door_code", False),
        ahmet=ahmet,
    )


@app.route("/api/add-to-cart", methods=["POST"])
def add_to_cart():
    data = request.get_json() or {}
    try:
        product_id = int(data.get("product_id", 0))
        quantity = int(data.get("quantity", 1))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Geçersiz parametre!"}), 400

    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"success": False, "message": "Ürün bulunamadı!"}), 404

    cart = session.get("cart", [])
    cart.append({
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "quantity": quantity,
    })
    session["cart"] = cart
    return jsonify({
        "success": True,
        "message": f"{product['name']} sepete eklendi!",
        "cart": cart,
    })


@app.route("/api/cart", methods=["GET"])
def get_cart():
    cart = session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart)
    return jsonify(
        {"cart": cart, "total": total, "balance": session.get("balance", 50)}
    )


@app.route("/api/clear-cart", methods=["POST"])
def clear_cart():
    session["cart"] = []
    return jsonify({"success": True, "message": "Sepet temizlendi."})


@app.route("/api/reset", methods=["POST"])
def reset():
    session.clear()
    init_db()
    init_user_session()
    return jsonify({"success": True, "message": "Sistem ve oturum sıfırlandı."})


@app.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", [])
    if not cart:
        return jsonify({"success": False, "message": "Sepetiniz boş!"}), 400

    total_cost = sum(item["price"] * item["quantity"] for item in cart)
    current_balance = session.get("balance", 50)

    if current_balance < total_cost:
        return jsonify({
            "success": False,
            "message": (
                f"Yetersiz DevPuan! Gereken: {total_cost} DP, Bakiyeniz:"
                f" {current_balance} DP."
            ),
        }), 400

    session["balance"] = current_balance - total_cost

    bought_door = False
    for item in cart:
        if item["id"] == 4 and item["quantity"] > 0:
            bought_door = True

    session["cart"] = []

    if bought_door:
        session["has_ceo_door_code"] = True
        return jsonify({
            "success": True,
            "door_bought": True,
            "message": (
                "CEO Odası Giriş Kartı satın alındı! Kapı şifreniz (1. Bayrak)"
                " oluşturuldu. Odaya girmek için bu şifreyi kullanın."
            ),
            "flag1": FLAG1,
            "redirect": "/ceo-door",
        })
    else:
        return jsonify({
            "success": True,
            "door_bought": False,
            "message": "Siparişiniz onaylandı.",
        })


@app.route("/ceo-door", methods=["GET", "POST"])
def ceo_door():
    """Flag 1'in girilmesini zorunlu kılan kapı kontrol noktası"""
    message = None
    if request.method == "POST":
        entered_code = request.form.get("door_code", "").strip()
        if entered_code == FLAG1:
            session["passed_ceo_door"] = True
            return redirect(url_for("ik_payroll"))
        else:
            message = "Hatalı kapı şifresi! Erişim reddedildi."

    return render_template("door.html", message=message)


@app.route("/ik-payroll", methods=["GET", "POST"])
def ik_payroll():
    # Kapıdan geçerli şifreyle (Flag 1) geçilmediyse ASLA panele sokma!
    if not session.get("passed_ceo_door"):
        return redirect(url_for("ceo_door"))

    db = get_db()
    cursor = db.cursor()

    message = None
    flag2 = None

    if request.method == "POST":
        emp_code = request.form.get("emp_code", "").strip()
        requested_salary = request.form.get("salary", "17002").strip()

        # is_real_ceo normalde 0 olarak yazılır; spoiler vermeden hata yönetilir
        sql = (
            f"UPDATE employees SET salary = {requested_salary}, is_real_ceo = 0"
            f" WHERE emp_code = '{emp_code}'"
        )

        try:
            cursor.executescript(sql)
            db.commit()

            cursor.execute(
                "SELECT salary, is_real_ceo FROM employees WHERE emp_code = 'EMP104'"
            )
            updated_ahmet = cursor.fetchone()

            if (
                updated_ahmet
                and updated_ahmet["is_real_ceo"] == 1
                and updated_ahmet["salary"] >= 500000
            ):
                message = (
                    "Talebiniz yönetim kurulu tarafından onaylandı. Sistem yetkileriniz"
                    " tanımlandı."
                )
                flag2 = FLAG2
            else:
                message = "Personel maaş güncelleme talebi sisteme iletildi."
        except Exception:
            message = (
                "Sistemde beklenmeyen bir hata oluştu. Lütfen parametreleri kontrol"
                " edin."
            )

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    db.close()

    return render_template(
        "payroll.html", employees=employees, message=message, flag2=flag2
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)