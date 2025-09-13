from flask import Flask, render_template, request
import os
from datetime import datetime

app = Flask(__name__)

# Save bookings.txt inside project folder
BOOKINGS_FILE = os.path.join(os.path.dirname(__file__), "bookings.txt")

# Ensure bookings.txt exists
def ensure_file():
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "w") as f:
            f.write("Bookings:\n")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")   # your home page

# ---------------- CUSTOMER ----------------
@app.route("/contact")
def booking_form():
    return render_template("form.html")   # booking form page

@app.route("/submit", methods=["POST"])
def submit():
    ensure_file()

    name = request.form.get("name")
    phone = request.form.get("phone")
    service = request.form.get("service")
    date = request.form.get("date")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save booking into bookings.txt
    with open(BOOKINGS_FILE, "a") as f:
        f.write(f"{time} | {name} | {phone} | {service} | {date}\n")

    # Show success page
    return render_template("success.html", name=name)

# ---------------- ADMIN / VIEW BOOKINGS ----------------
@app.route("/book")
def show_bookings():
    ensure_file()
    bookings = []

    # Read file and split lines
    with open(BOOKINGS_FILE, "r") as f:
        lines = f.readlines()[1:]  # skip "Bookings:" header
        for line in lines:
            parts = line.strip().split(" | ")
            if len(parts) == 5:
                bookings.append({
                    "time": parts[0],
                    "name": parts[1],
                    "phone": parts[2],
                    "service": parts[3],
                    "date": parts[4]
                })

    return render_template("bookings.html", bookings=bookings)

if __name__ == "__main__":
    app.run(debug=True)