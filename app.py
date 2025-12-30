from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# Initialize database
def init_db():
    conn = sqlite3.connect("bloodbank.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            email TEXT,
            blood_group TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route("/")
def home():
    return render_template("index3.html")

# Main menu
@app.route("/main_menu")
def main_menu():
    return render_template("main_menu3.html")

# Add donor
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        blood_group = request.form['blood_group']

        conn = sqlite3.connect("bloodbank.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO donors (name, age, gender, phone, email, blood_group) VALUES (?, ?, ?, ?, ?, ?)",
            (name, age, gender, phone, email, blood_group)
        )
        conn.commit()
        conn.close()
        flash("Donor added successfully!")
        return redirect(url_for('add'))

    return render_template("add_donor.html")

# View donor menu
@app.route("/view")
def view_donor_menu():
    return render_template("view_options.html")

# View all donors
@app.route("/view_all")
def view_all():
    conn = sqlite3.connect("bloodbank.db")
    c = conn.cursor()
    c.execute("SELECT * FROM donors")
    donors = c.fetchall()
    conn.close()
    return render_template("view_all.html", donors=donors)

# Search by name
@app.route("/view_search_name", methods=["GET", "POST"])
def view_search_name():
    donors = []
    if request.method == "POST":
        name = request.form['name']
        conn = sqlite3.connect("bloodbank.db")
        c = conn.cursor()
        c.execute("SELECT * FROM donors WHERE name LIKE ?", ('%' + name + '%',))
        donors = c.fetchall()
        conn.close()
    return render_template("view_search_name.html", donors=donors)

# Search by blood group
@app.route("/view_search_blood", methods=["GET", "POST"])
def view_search_blood():
    donors = []
    if request.method == "POST":
        blood_group = request.form['blood_group']
        conn = sqlite3.connect("bloodbank.db")
        c = conn.cursor()
        c.execute("SELECT * FROM donors WHERE blood_group=?", (blood_group,))
        donors = c.fetchall()
        conn.close()
    return render_template("view_search_blood.html", donors=donors)

# Search by ID
@app.route("/view_search_id", methods=["GET", "POST"])
def view_search_id():
    donors = []
    if request.method == "POST":
        id = request.form['id']
        conn = sqlite3.connect("bloodbank.db")
        c = conn.cursor()
        c.execute("SELECT * FROM donors WHERE id=?", (id,))
        donors = c.fetchall()
        conn.close()
    return render_template("view_search_id.html", donors=donors)

# Delete donor
@app.route("/delete", methods=["GET", "POST"])
def delete():
    donor = None
    if request.method == "POST":
        id = request.form.get('id')
        name = request.form.get('name')

        conn = sqlite3.connect("bloodbank.db")
        c = conn.cursor()

        if 'delete_confirm' in request.form:  # Delete button clicked
            donor_id = request.form['id']
            c.execute("DELETE FROM donors WHERE id=?", (donor_id,))
            conn.commit()
            flash("Donor deleted successfully!")
            donor = None
        else:  # Search donor to display
            if id:
                c.execute("SELECT * FROM donors WHERE id=?", (id,))
            elif name:
                c.execute("SELECT * FROM donors WHERE name LIKE ?", ('%' + name + '%',))
            donor = c.fetchone()

        conn.close()

    return render_template("delete_choose.html", donor=donor)

# Update donor choose
@app.route("/update_choose", methods=["GET", "POST"])
def update_choose():
    donor = None
    if request.method == "POST":
        id = request.form.get('id')
        name = request.form.get('name')
        conn = sqlite3.connect("bloodbank.db")
        c = conn.cursor()
        if id:
            c.execute("SELECT * FROM donors WHERE id=?", (id,))
        elif name:
            c.execute("SELECT * FROM donors WHERE name LIKE ?", ('%' + name + '%',))
        donor = c.fetchone()
        conn.close()
        if donor:
            return redirect(url_for('update_form', id=donor[0]))
        else:
            flash("No donor found!")
    return render_template("update_choose.html", donor=donor)

# Update donor form
@app.route("/update_form/<int:id>", methods=["GET", "POST"])
def update_form(id):
    conn = sqlite3.connect("bloodbank.db")
    c = conn.cursor()
    c.execute("SELECT * FROM donors WHERE id=?", (id,))
    donor = c.fetchone()

    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        blood_group = request.form['blood_group']

        c.execute(
            "UPDATE donors SET name=?, age=?, gender=?, phone=?, email=?, blood_group=? WHERE id=?",
            (name, age, gender, phone, email, blood_group, id)
        )
        conn.commit()
        conn.close()
        flash("Donor updated successfully!")
        return redirect(url_for('main_menu'))

    conn.close()
    return render_template("update_form.html", donor=donor)

if __name__ == "__main__":
    app.run(debug=True)
