from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

# Database connection
def get_db_connection():
    conn = sqlite3.connect('affiliate_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route('/')
def index():
    referral_id = session.get('referral_id', '')
    return render_template('index.html', referral_id=referral_id)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        referral_id = request.form.get('referral_id')
        pwd = request.form.get('pwd')

        if not referral_id or not pwd:
            flash('Both Referral ID and Password are required!', 'error')
            return redirect('/login')

        conn = get_db_connection()
        affiliate = conn.execute(
            "SELECT * FROM affiliates WHERE referral_id = ? AND pwd = ?",
            (referral_id, pwd)
        ).fetchone()
        conn.close()

        if affiliate:
            # Store affiliate info in session
            session['affiliate_id'] = affiliate['id']
            session['referral_id'] = affiliate['referral_id']
            session['name'] = affiliate['name']
            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid Referral ID or Password. Please try again.', 'error')
            return redirect('/login')

    return render_template('login.html')

# Track referral clicks via GET
@app.route('/referral/<referral_id>', methods=['GET'])
def track_referral_click(referral_id):
    # Validate referral ID
    conn = get_db_connection()
    affiliate = conn.execute("SELECT * FROM affiliates WHERE referral_id = ?", (referral_id,)).fetchone()
    conn.close()

    if not affiliate:
        flash('Invalid referral link.', 'error')
        return redirect('/')

    # Log the click
    conn = get_db_connection()
    click_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute("INSERT INTO clicks (referral_id, click_time) VALUES (?, ?)", (referral_id, click_time))
    conn.commit()
    conn.close()

    return redirect('/')  # Redirect to a relevant page, e.g., the landing page

# Track referral clicks via POST
@app.route('/track_click', methods=['POST'])
def track_click_api():
    data = request.get_json()

    referral_id = data.get('referral_id')
    product_name = data.get('product_name')
    click_time = data.get('click_time')
    customer_name = data.get('customer_name')  # Fetch from frontend

    # Validate referral ID
    conn = get_db_connection()
    affiliate = conn.execute("SELECT * FROM affiliates WHERE referral_id = ?", (referral_id,)).fetchone()

    if not affiliate:
        conn.close()
        return {"error": "Invalid referral ID"}, 400

    # Insert into clicks table
    conn.execute(
        "INSERT INTO clicks (referral_id, click_time, customer_name) VALUES (?, ?, ?)",
        (referral_id, click_time, customer_name)
    )
    conn.commit()
    conn.close()

    return {"message": "Click tracked successfully"}, 200



@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()

    full_name = data.get('customer_name')
    mobile_number = data.get('mobile_number')
    referral_id = data.get('referral_id')

    if not full_name:
        return {"error": "Full name is required"}, 400

    # Insert into `customers` table
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO customers (full_name, mobile_number, timestamp) VALUES (?, ?, CURRENT_TIMESTAMP)",
        (full_name, mobile_number)
    )
    conn.commit()

    # Fetch full name from localStorage and insert into `clicks` table
    conn.execute(
        "UPDATE clicks SET customer_name = ? WHERE referral_id = ? AND customer_name IS NULL",
        (full_name, referral_id)
    )
    conn.commit()
    conn.close()

    return {"message": "Happy Shopping"}, 200



# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'affiliate_id' not in session:
        return redirect('/login')

    referral_id = session['referral_id']
    conn = get_db_connection()

    # Fetch total clicks
    total_clicks = conn.execute(
        "SELECT COUNT(*) FROM clicks WHERE referral_id = ?",
        (referral_id,)
    ).fetchone()[0]

    # Fetch clicks in the last 48 hours
    recent_clicks = conn.execute(
        """
        SELECT COUNT(*) FROM clicks
        WHERE referral_id = ? AND
              click_time >= datetime('now', '-48 hours')
        """,
        (referral_id,)
    ).fetchone()[0]

    # Fetch total commission earned
    total_commission = conn.execute(
        "SELECT SUM(commission) FROM sales WHERE referral_id = ?",
        (referral_id,)
    ).fetchone()[0] or 0

    # Fetch sales details and convert to a list of dictionaries
    sales_query = conn.execute(
        "SELECT product_name, commission, sale_date FROM sales WHERE referral_id = ?",
        (referral_id,)
    ).fetchall()

    # Convert immutable rows to mutable dictionaries
    sales = [dict(row) for row in sales_query]

    # Fetch total sales count
    total_sales = conn.execute(
        "SELECT COUNT(*) FROM sales WHERE referral_id = ?",
        (referral_id,)
    ).fetchone()[0]

    # Fetch sales in the last 48 hours
    recent_sales = conn.execute(
        """
        SELECT COUNT(*) FROM sales
        WHERE referral_id = ? AND
              sale_date >= datetime('now', '-48 hours')
        """,
        (referral_id,)
    ).fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        name=session['name'],
        total_clicks=total_clicks,
        recent_clicks=recent_clicks,
        total_commission=total_commission,
        total_sales=total_sales,
        recent_sales=recent_sales,
        sales=sales
    )



# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
