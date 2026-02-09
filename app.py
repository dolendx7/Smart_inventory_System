from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import date, datetime, timedelta
import mysql.connector
from mysql.connector import Error
import hashlib
import re
import os
from functools import wraps

app = Flask(__name__)
# Use environment variable for secret key in production
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# ============= VALIDATION FUNCTIONS =============

def validate_email(email):
    """Validate email format - must contain @"""
    if not email:
        return False, "Email is required"
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format. Email must contain @ and a valid domain"
    return True, ""

def validate_phone(phone):
    """Validate phone number - must be exactly 10 digits"""
    if not phone:
        return False, "Phone number is required"
    # Remove spaces, dashes, parentheses
    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
    if not phone_clean.isdigit():
        return False, "Phone number must contain only digits"
    if len(phone_clean) != 10:
        return False, "Phone number must be exactly 10 digits"
    return True, ""

def validate_password(password):
    """Validate password - must contain at least one special character"""
    if not password:
        return False, "Password is required"
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    # Check for at least one special character
    special_chars = r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\/;~`]'
    if not re.search(special_chars, password):
        return False, r"Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>_-+=[]\\/;~`)"
    return True, ""

def validate_name(name, field_name="Name"):
    """Validate name - must not contain numbers"""
    if not name:
        return False, f"{field_name} is required"
    if re.search(r'\d', name):
        return False, f"{field_name} cannot contain numbers"
    if len(name.strip()) < 2:
        return False, f"{field_name} must be at least 2 characters long"
    return True, ""

def validate_contact_person(name):
    """Validate contact person name - must not contain numbers"""
    if not name:
        return True, ""  # Contact person is optional
    return validate_name(name, "Contact person name")

# Database Configuration - Use environment variables in production
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'dolen@123')
MASTER_DB = os.environ.get('MASTER_DB', 'inventory_master')

# Database Connection Helper
def get_db_connection(database=None):
    """Connect to specified database or master database"""
    try:
        config = {
            'host': DB_HOST,
            'user': DB_USER,
            'password': DB_PASSWORD
        }
        if database:
            config['database'] = database
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        # Log error properly instead of print
        return None

def get_admin_db():
    """Get database name - now returns the single shared database"""
    return MASTER_DB

def get_admin_id():
    """Get current admin ID from session"""
    return session.get('admin_id', None)

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============= AUTHENTICATION ROUTES =============

@app.route('/')
def index():
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection(MASTER_DB)
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admins WHERE email = %s AND password = %s", 
                         (email, hash_password(password)))
            admin = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if admin:
                session['admin_id'] = admin['id']
                session['username'] = admin['username']
                session['email'] = admin['email']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'error')
        else:
            flash('Database connection error', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate username
        valid, msg = validate_name(username, "Username")
        if not valid:
            flash(msg, 'error')
            return render_template('signup.html')
        
        # Validate email
        valid, msg = validate_email(email)
        if not valid:
            flash(msg, 'error')
            return render_template('signup.html')
        
        # Validate password
        valid, msg = validate_password(password)
        if not valid:
            flash(msg, 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        conn = get_db_connection(MASTER_DB)
        if conn:
            cursor = conn.cursor()
            try:
                # Create admin account in master database
                cursor.execute(
                    "INSERT INTO admins (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, hash_password(password))
                )
                admin_id = cursor.lastrowid
                
                conn.commit()
                
                # Automatically log in the user after successful signup
                session['admin_id'] = admin_id
                session['username'] = username
                session['email'] = email
                
                flash('Account created successfully! Welcome to your dashboard.', 'success')
                return redirect(url_for('dashboard'))
            except Error as e:
                conn.rollback()
                flash(f'Error creating account: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# ============= DASHBOARD ROUTE =============

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection(get_admin_db())
    if not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('login'))
    
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    
    # Get dashboard metrics
    cursor.execute("SELECT COUNT(*) as total FROM products WHERE admin_id = %s", (admin_id,))
    total_products = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM products WHERE admin_id = %s AND stock_quantity <= reorder_level", (admin_id,))
    low_stock = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM suppliers WHERE admin_id = %s", (admin_id,))
    total_suppliers = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM buyers WHERE admin_id = %s", (admin_id,))
    total_buyers = cursor.fetchone()['total']
    
    cursor.execute("SELECT SUM(total_amount) as revenue FROM sales WHERE admin_id = %s AND YEAR(sale_date) = YEAR(CURDATE())", (admin_id,))
    revenue_result = cursor.fetchone()
    total_revenue = revenue_result['revenue'] if revenue_result['revenue'] else 0
    
    cursor.execute("SELECT SUM(stock_quantity * unit_price) as value FROM products WHERE admin_id = %s", (admin_id,))
    inventory_value_result = cursor.fetchone()
    inventory_value = inventory_value_result['value'] if inventory_value_result['value'] else 0
    
    # Get recent activities (last 10 transactions)
    cursor.execute("""
        SELECT t.*, p.product_name
        FROM transactions t
        JOIN products p ON t.product_id = p.id
        WHERE t.admin_id = %s
        ORDER BY t.transaction_date DESC
        LIMIT 10
    """, (admin_id,))
    recent_activities = cursor.fetchall()
    
    # Get low stock alerts
    cursor.execute("""
        SELECT id, product_name, stock_quantity, reorder_level, category
        FROM products 
        WHERE admin_id = %s AND stock_quantity <= reorder_level
        ORDER BY stock_quantity ASC
        LIMIT 5
    """, (admin_id,))
    alerts = cursor.fetchall()
    
    # Get top selling products
    cursor.execute("""
        SELECT p.product_name, p.category, SUM(si.quantity) as total_sold, SUM(si.subtotal) as revenue
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        JOIN sales s ON si.sale_id = s.id
        WHERE s.admin_id = %s
        GROUP BY si.product_id
        ORDER BY total_sold DESC
        LIMIT 5
    """, (admin_id,))
    top_products = cursor.fetchall()
    
    # Get category distribution
    cursor.execute("""
        SELECT category, COUNT(*) as count, SUM(stock_quantity) as total_stock
        FROM products
        WHERE admin_id = %s
        GROUP BY category
    """, (admin_id,))
    categories = cursor.fetchall()
    
    # Get monthly sales data for chart
    cursor.execute("""
        SELECT 
            DATE_FORMAT(sale_date, '%Y-%m') as month,
            SUM(total_amount) as revenue,
            COUNT(*) as orders
        FROM sales
        WHERE admin_id = %s AND sale_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
        ORDER BY month
    """, (admin_id,))
    monthly_sales = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html',
                         total_products=total_products,
                         low_stock=low_stock,
                         total_suppliers=total_suppliers,
                         total_buyers=total_buyers,
                         total_revenue=total_revenue,
                         inventory_value=inventory_value,
                         recent_activities=recent_activities,
                         alerts=alerts,
                         top_products=top_products,
                         categories=categories,
                         monthly_sales=monthly_sales)

# ============= PRODUCT ROUTES =============

@app.route('/products')
@login_required
def products():
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    
    query = "SELECT * FROM products WHERE admin_id = %s"
    params = [admin_id]
    
    if search:
        query += " AND (product_name LIKE %s OR sku LIKE %s OR description LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])
    
    if category:
        query += " AND category = %s"
        params.append(category)
    
    if status:
        if status == 'in_stock':
            query += " AND stock_quantity > reorder_level"
        elif status == 'low_stock':
            query += " AND stock_quantity <= reorder_level AND stock_quantity > 0"
        elif status == 'out_of_stock':
            query += " AND stock_quantity = 0"
    
    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    products_list = cursor.fetchall()
    
    # Get unique categories for filter
    cursor.execute("SELECT DISTINCT category FROM products WHERE admin_id = %s ORDER BY category", (admin_id,))
    categories = cursor.fetchall()
    
    # Get suppliers for modal dropdown
    cursor.execute("SELECT id, supplier_name FROM suppliers WHERE admin_id = %s ORDER BY supplier_name", (admin_id,))
    suppliers = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('products.html', products=products_list, categories=categories, suppliers=suppliers)

@app.route('/products/add', methods=['POST'])
@login_required
def add_product():
    admin_id = get_admin_id()
    data = request.form
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO products (admin_id, sku, product_name, description, category, unit_price, 
                                stock_quantity, reorder_level, max_stock_level, supplier_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            admin_id,
            data.get('sku'),
            data.get('product_name'),
            data.get('description'),
            data.get('category'),
            data.get('unit_price'),
            data.get('stock_quantity'),
            data.get('reorder_level'),
            data.get('max_stock_level'),
            data.get('supplier_id') if data.get('supplier_id') else None
        ))
        
        product_id = cursor.lastrowid
        
        # Record transaction
        cursor.execute("""
            INSERT INTO transactions (admin_id, product_id, transaction_type, quantity, notes)
            VALUES (%s, %s, 'ADD', %s, 'Initial stock added')
        """, (admin_id, product_id, data.get('stock_quantity')))
        
        conn.commit()
        flash('Product added successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error adding product: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('products'))

@app.route('/products/edit/<int:id>', methods=['POST'])
@login_required
def edit_product(id):
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    data = request.form
    
    try:
        cursor.execute("""
            UPDATE products 
            SET sku=%s, product_name=%s, description=%s, category=%s, unit_price=%s,
                stock_quantity=%s, reorder_level=%s, max_stock_level=%s, supplier_id=%s
            WHERE admin_id=%s AND id=%s
        """, (
            data.get('sku'),
            data.get('product_name'),
            data.get('description'),
            data.get('category'),
            data.get('unit_price'),
            data.get('stock_quantity'),
            data.get('reorder_level'),
            data.get('max_stock_level'),
            data.get('supplier_id') if data.get('supplier_id') else None,
            admin_id,
            id
        ))
        
        # Record transaction
        cursor.execute("""
            INSERT INTO transactions (admin_id, product_id, transaction_type, quantity, notes)
            VALUES (%s, %s, 'UPDATE', 0, 'Product information updated')
        """, (admin_id, id))
        
        conn.commit()
        flash('Product updated successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error updating product: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('products'))

@app.route('/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor()
    admin_id = get_admin_id()
    
    try:
        cursor.execute("DELETE FROM products WHERE admin_id = %s AND id = %s", (admin_id, id))
        conn.commit()
        flash('Product deleted successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error deleting product: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('products'))

@app.route('/products/adjust-stock/<int:id>', methods=['POST'])
@login_required
def adjust_stock(id):
    adjustment_type = request.form.get('adjustment_type')
    quantity = int(request.form.get('quantity'))
    notes = request.form.get('notes', '')
    admin_id = get_admin_id()
    
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT stock_quantity FROM products WHERE admin_id = %s AND id = %s", (admin_id, id))
        product = cursor.fetchone()
        current_stock = product['stock_quantity']
        
        if adjustment_type == 'add':
            new_stock = current_stock + quantity
            transaction_type = 'RESTOCK'
        else:  # subtract
            new_stock = max(0, current_stock - quantity)
            transaction_type = 'REMOVE'
        
        cursor.execute("UPDATE products SET stock_quantity = %s WHERE admin_id = %s AND id = %s", (new_stock, admin_id, id))
        
        cursor.execute("""
            INSERT INTO transactions (admin_id, product_id, transaction_type, quantity, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (admin_id, id, transaction_type, quantity, notes))
        
        conn.commit()
        flash('Stock adjusted successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error adjusting stock: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('products'))

# ============= SUPPLIER ROUTES =============

@app.route('/suppliers')
@login_required
def suppliers():
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    
    search = request.args.get('search', '')
    query = "SELECT s.*, COUNT(p.id) as total_products FROM suppliers s LEFT JOIN products p ON s.id = p.supplier_id AND p.admin_id = %s WHERE s.admin_id = %s"
    params = [admin_id, admin_id]
    
    if search:
        query += " AND (s.supplier_name LIKE %s OR s.contact_person LIKE %s OR s.email LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])
    
    query += " GROUP BY s.id ORDER BY s.id DESC"
    
    cursor.execute(query, params)
    suppliers_list = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('suppliers.html', suppliers=suppliers_list)

@app.route('/suppliers/add', methods=['POST'])
@login_required
def add_supplier():
    admin_id = get_admin_id()
    data = request.form
    
    # Validate supplier name
    valid, msg = validate_name(data.get('supplier_name'), "Supplier name")
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('suppliers'))
    
    # Validate contact person
    valid, msg = validate_contact_person(data.get('contact_person'))
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('suppliers'))
    
    # Validate email
    valid, msg = validate_email(data.get('email'))
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('suppliers'))
    
    # Validate phone
    valid, msg = validate_phone(data.get('phone'))
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('suppliers'))
    
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO suppliers (admin_id, supplier_name, contact_person, email, phone, address, city, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            admin_id,
            data.get('supplier_name'),
            data.get('contact_person'),
            data.get('email'),
            data.get('phone'),
            data.get('address'),
            data.get('city'),
            data.get('country')
        ))
        conn.commit()
        flash('Supplier added successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error adding supplier: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('suppliers'))

@app.route('/sales/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_sale(id):
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()

    # Get sale and items
    cursor.execute("SELECT * FROM sales WHERE admin_id = %s AND id = %s", (admin_id, id))
    sale = cursor.fetchone()
    if not sale:
        cursor.close()
        conn.close()
        flash("Sale not found", "error")
        return redirect(url_for('sales'))

    # POST request: update sale
    if request.method == 'POST':
        try:
            # Get form data
            buyer_id = request.form.get('buyer_id')
            sale_date = request.form.get('sale_date')
            total_amount = request.form.get('total_amount')
            status = request.form.get('status', 'Pending')
            notes = request.form.get('notes', '')
            
            # Get items from form
            product_ids = request.form.getlist('product_id[]')
            quantities = request.form.getlist('quantity[]')
            unit_prices = request.form.getlist('unit_price[]')
            subtotals = request.form.getlist('subtotal[]')
            
            # First, restore stock from old sale items
            cursor.execute("""
                SELECT si.product_id, si.quantity 
                FROM sale_items si
                JOIN products p ON si.product_id = p.id
                WHERE si.sale_id = %s AND p.admin_id = %s
            """, (id, admin_id))
            old_items = cursor.fetchall()
            
            for old_item in old_items:
                cursor.execute("""
                    UPDATE products 
                    SET stock_quantity = stock_quantity + %s 
                    WHERE admin_id = %s AND id = %s
                """, (old_item['quantity'], admin_id, old_item['product_id']))
            
            # Delete old sale items
            cursor.execute("DELETE FROM sale_items WHERE sale_id = %s", (id,))
            
            # Update sale info
            cursor.execute("""
                UPDATE sales 
                SET buyer_id=%s, sale_date=%s, total_amount=%s, status=%s, notes=%s
                WHERE admin_id=%s AND id=%s
            """, (buyer_id, sale_date, total_amount, status, notes, admin_id, id))

            # Insert updated sale items and deduct stock
            for i in range(len(product_ids)):
                cursor.execute("""
                    INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id, product_ids[i], quantities[i], unit_prices[i], subtotals[i]))

                cursor.execute("""
                    UPDATE products
                    SET stock_quantity = stock_quantity - %s
                    WHERE admin_id = %s AND id = %s
                """, (quantities[i], admin_id, product_ids[i]))

                cursor.execute("""
                    INSERT INTO transactions (admin_id, product_id, transaction_type, quantity, notes)
                    VALUES (%s, %s, 'SALE', %s, %s)
                """, (admin_id, product_ids[i], quantities[i], f"Updated Sale: {sale['order_number']}"))

            conn.commit()
            flash('Sale updated successfully!', 'success')
            return redirect(url_for('sales'))

        except Error as e:
            conn.rollback()
            flash(f'Error updating sale: {str(e)}', 'error')
            return redirect(url_for('edit_sale', id=id))
        finally:
            cursor.close()
            conn.close()
    
    # GET request: show form
    cursor.execute("""
        SELECT si.*, p.product_name, p.unit_price, p.stock_quantity
        FROM sale_items si
        JOIN products p ON si.product_id = p.id AND p.admin_id = %s
        WHERE si.sale_id = %s
    """, (admin_id, id))
    items = cursor.fetchall()

    cursor.execute("SELECT id, buyer_name FROM buyers WHERE admin_id = %s ORDER BY buyer_name", (admin_id,))
    buyers_list = cursor.fetchall()

    cursor.execute("SELECT id, product_name, sku, unit_price, stock_quantity FROM products WHERE admin_id = %s ORDER BY product_name", (admin_id,))
    products_list = cursor.fetchall()

    # Format sale_date for HTML input
    if sale.get('sale_date'):
        sale['sale_date'] = sale['sale_date'].strftime('%Y-%m-%d')

    cursor.close()
    conn.close()
    return render_template('edit_sale.html', sale=sale, items=items, buyers=buyers_list, products=products_list)

@app.route('/suppliers/edit/<int:id>', methods=['POST'])
@login_required
def edit_supplier(id):
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    data = request.form
    
    # Validate supplier name
    valid, msg = validate_name(data.get('supplier_name'), "Supplier name")
    if not valid:
        flash(msg, 'error')
        cursor.close()
        conn.close()
        return redirect(url_for('suppliers'))
    
    # Validate contact person
    valid, msg = validate_contact_person(data.get('contact_person'))
    if not valid:
        flash(msg, 'error')
        cursor.close()
        conn.close()
        return redirect(url_for('suppliers'))
    
    # Validate email
    valid, msg = validate_email(data.get('email'))
    if not valid:
        flash(msg, 'error')
        cursor.close()
        conn.close()
        return redirect(url_for('suppliers'))
    
    # Validate phone
    valid, msg = validate_phone(data.get('phone'))
    if not valid:
        flash(msg, 'error')
        cursor.close()
        conn.close()
        return redirect(url_for('suppliers'))
    
    try:
        cursor.execute("""
            UPDATE suppliers 
            SET supplier_name=%s, contact_person=%s, email=%s, phone=%s, 
                address=%s, city=%s, country=%s
            WHERE admin_id=%s AND id=%s
        """, (
            data.get('supplier_name'),
            data.get('contact_person'),
            data.get('email'),
            data.get('phone'),
            data.get('address'),
            data.get('city'),
            data.get('country'),
            admin_id,
            id
        ))
        conn.commit()
        flash('Supplier updated successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error updating supplier: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('suppliers'))

@app.route('/sales/delete/<int:id>', methods=['POST'])
@login_required
def delete_sale(id):
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    
    try:
        # First, restore stock for the sale items
        cursor.execute("""
            SELECT si.product_id, si.quantity 
            FROM sale_items si
            JOIN sales s ON si.sale_id = s.id
            WHERE s.admin_id = %s AND si.sale_id = %s
        """, (admin_id, id))
        items = cursor.fetchall()
        
        for item in items:
            cursor.execute("""
                UPDATE products 
                SET stock_quantity = stock_quantity + %s 
                WHERE admin_id = %s AND id = %s
            """, (item['quantity'], admin_id, item['product_id']))
            
            # Record transaction
            cursor.execute("""
                INSERT INTO transactions (admin_id, product_id, transaction_type, quantity, notes)
                VALUES (%s, %s, 'REMOVE', %s, 'Sale deleted - stock restored')
            """, (admin_id, item['product_id'], item['quantity']))
        
        # Delete sale items
        cursor.execute("DELETE FROM sale_items WHERE sale_id = %s", (id,))
        
        # Delete the sale itself
        cursor.execute("DELETE FROM sales WHERE admin_id = %s AND id = %s", (admin_id, id))
        
        conn.commit()
        flash('Sale deleted successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error deleting sale: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('sales'))


@app.route('/suppliers/delete/<int:id>', methods=['POST'])
@login_required
def delete_supplier(id):
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor()
    admin_id = get_admin_id()
    
    try:
        cursor.execute("DELETE FROM suppliers WHERE admin_id = %s AND id = %s", (admin_id, id))
        conn.commit()
        flash('Supplier deleted successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error deleting supplier: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('suppliers'))

# ============= BUYER ROUTES =============

@app.route('/buyers')
@login_required
def buyers():
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    
    search = request.args.get('search', '')
    query = "SELECT b.*, COUNT(s.id) as total_orders FROM buyers b LEFT JOIN sales s ON b.id = s.buyer_id AND s.admin_id = %s WHERE b.admin_id = %s"
    params = [admin_id, admin_id]
    
    if search:
        query += " AND (b.buyer_name LIKE %s OR b.contact_person LIKE %s OR b.email LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])
    
    query += " GROUP BY b.id ORDER BY b.id DESC"
    
    cursor.execute(query, params)
    buyers_list = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('buyers.html', buyers=buyers_list)

@app.route('/buyers/add', methods=['POST'])
@login_required
def add_buyer():
    admin_id = get_admin_id()
    data = request.form
    
    # Validate buyer name
    valid, msg = validate_name(data.get('buyer_name'), "Buyer name")
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('buyers'))
    
    # Validate contact person
    valid, msg = validate_contact_person(data.get('contact_person'))
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('buyers'))
    
    # Validate email (if provided)
    if data.get('email'):
        valid, msg = validate_email(data.get('email'))
        if not valid:
            flash(msg, 'error')
            return redirect(url_for('buyers'))
    
    # Validate phone (if provided)
    if data.get('phone'):
        valid, msg = validate_phone(data.get('phone'))
        if not valid:
            flash(msg, 'error')
            return redirect(url_for('buyers'))
    
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO buyers (admin_id, buyer_name, contact_person, email, phone, address, city, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            admin_id,
            data.get('buyer_name'),
            data.get('contact_person'),
            data.get('email'),
            data.get('phone'),
            data.get('address'),
            data.get('city'),
            data.get('country')
        ))
        conn.commit()
        flash('Buyer added successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error adding buyer: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('buyers'))

@app.route('/buyers/edit/<int:id>', methods=['POST'])
@login_required
def edit_buyer(id):
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    data = request.form
    
    # Validate buyer name
    valid, msg = validate_name(data.get('buyer_name'), "Buyer name")
    if not valid:
        flash(msg, 'error')
        cursor.close()
        conn.close()
        return redirect(url_for('buyers'))
    
    # Validate contact person
    valid, msg = validate_contact_person(data.get('contact_person'))
    if not valid:
        flash(msg, 'error')
        cursor.close()
        conn.close()
        return redirect(url_for('buyers'))
    
    # Validate email (if provided)
    if data.get('email'):
        valid, msg = validate_email(data.get('email'))
        if not valid:
            flash(msg, 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('buyers'))
    
    # Validate phone (if provided)
    if data.get('phone'):
        valid, msg = validate_phone(data.get('phone'))
        if not valid:
            flash(msg, 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('buyers'))
    
    try:
        cursor.execute("""
            UPDATE buyers 
            SET buyer_name=%s, contact_person=%s, email=%s, phone=%s, 
                address=%s, city=%s, country=%s
            WHERE admin_id=%s AND id=%s
        """, (
            data.get('buyer_name'),
            data.get('contact_person'),
            data.get('email'),
            data.get('phone'),
            data.get('address'),
            data.get('city'),
            data.get('country'),
            admin_id,
            id
        ))
        conn.commit()
        flash('Buyer updated successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error updating buyer: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('buyers'))

@app.route('/buyers/delete/<int:id>', methods=['POST'])
@login_required
def delete_buyer(id):
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor()
    admin_id = get_admin_id()
    
    try:
        cursor.execute("DELETE FROM buyers WHERE admin_id = %s AND id = %s", (admin_id, id))
        conn.commit()
        flash('Buyer deleted successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error deleting buyer: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('buyers'))

# ============= SALES ROUTES =============

@app.route('/sales')
@login_required
def sales():
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = """
        SELECT s.*, b.buyer_name 
        FROM sales s
        LEFT JOIN buyers b ON s.buyer_id = b.id AND b.admin_id = %s
        WHERE s.admin_id = %s
    """
    params = [admin_id, admin_id]
    
    if search:
        query += " AND (s.order_number LIKE %s OR b.buyer_name LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param])
    
    if status:
        query += " AND s.status = %s"
        params.append(status)
    
    query += " ORDER BY s.sale_date DESC"
    
    cursor.execute(query, params)
    sales_list = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('sales.html', sales=sales_list)


@app.route('/sales/add', methods=['GET', 'POST'])
@login_required
def add_sale():
    admin_id = get_admin_id()
    
    if request.method == 'POST':
        try:
            # Get form data
            buyer_id = request.form.get('buyer_id')
            sale_date = request.form.get('sale_date')
            total_amount = request.form.get('total_amount')
            status = request.form.get('status', 'Pending')
            notes = request.form.get('notes', '')
            
            # Get items from form
            product_ids = request.form.getlist('product_id[]')
            quantities = request.form.getlist('quantity[]')
            unit_prices = request.form.getlist('unit_price[]')
            subtotals = request.form.getlist('subtotal[]')
            
            conn = get_db_connection(get_admin_db())
            cursor = conn.cursor(dictionary=True)
            
            # Generate unique order number
            today_str = datetime.now().strftime('%Y%m%d')
            cursor.execute("""
                SELECT COUNT(*) AS count FROM sales 
                WHERE admin_id = %s AND order_number LIKE %s
            """, (admin_id, f"ORD-{today_str}-%"))
            count = cursor.fetchone()['count']
            order_number = f"ORD-{today_str}-{count + 1:04d}"
            
            # Insert sale
            cursor.execute("""
                INSERT INTO sales (admin_id, order_number, buyer_id, sale_date, total_amount, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (admin_id, order_number, buyer_id, sale_date, total_amount, status, notes))
            sale_id = cursor.lastrowid
            
            # Insert sale items and update stock
            for i in range(len(product_ids)):
                cursor.execute("""
                    INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (sale_id, product_ids[i], quantities[i], unit_prices[i], subtotals[i]))
                
                # Update stock
                cursor.execute("""
                    UPDATE products
                    SET stock_quantity = stock_quantity - %s
                    WHERE admin_id = %s AND id = %s
                """, (quantities[i], admin_id, product_ids[i]))
                
                # Record transaction
                cursor.execute("""
                    INSERT INTO transactions (admin_id, product_id, transaction_type, quantity, notes)
                    VALUES (%s, %s, 'SALE', %s, %s)
                """, (admin_id, product_ids[i], quantities[i], f"Sale Order: {order_number}"))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Sale created successfully!', 'success')
            return redirect(url_for('sales'))
        
        except Error as e:
            if 'conn' in locals():
                conn.rollback()
                cursor.close()
                conn.close()
            flash(f'Error creating sale: {str(e)}', 'error')
            return redirect(url_for('add_sale'))
    
    # GET request - show form
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    
    # Buyers
    cursor.execute("SELECT id, buyer_name FROM buyers WHERE admin_id = %s ORDER BY buyer_name", (admin_id,))
    buyers_list = cursor.fetchall()
    
    # Products with stock > 0
    cursor.execute("""
        SELECT id, product_name, sku, unit_price, stock_quantity 
        FROM products 
        WHERE admin_id = %s AND stock_quantity > 0 
        ORDER BY product_name
    """, (admin_id,))
    products_list = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    today = date.today().isoformat()  # Default date for the form
    return render_template('add_sale.html', buyers=buyers_list, products=products_list, today=today)


@app.route('/sales/view/<int:id>')
@login_required
def view_sale(id):
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    
    cursor.execute("""
        SELECT s.*, b.buyer_name, b.email, b.phone, b.address, b.city, b.country
        FROM sales s
        LEFT JOIN buyers b ON s.buyer_id = b.id AND b.admin_id = %s
        WHERE s.admin_id = %s AND s.id = %s
    """, (admin_id, admin_id, id))
    sale = cursor.fetchone()
    
    cursor.execute("""
        SELECT si.*, p.product_name, p.sku
        FROM sale_items si
        JOIN products p ON si.product_id = p.id AND p.admin_id = %s
        WHERE si.sale_id = %s
    """, (admin_id, id))
    items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('view_sale.html', sale=sale, items=items)

@app.route('/sales/update-status/<int:id>', methods=['POST'])
@login_required
def update_sale_status(id):
    status = request.form.get('status')
    admin_id = get_admin_id()
    
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE sales SET status = %s WHERE admin_id = %s AND id = %s", (status, admin_id, id))
        conn.commit()
        flash('Sale status updated successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error updating status: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('view_sale', id=id))

# ============= REPORTS ROUTES =============

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@app.route('/reports/inventory')
@login_required
def inventory_report():
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    
    cursor.execute("""
        SELECT 
            p.*,
            s.supplier_name,
            (p.stock_quantity * p.unit_price) as stock_value,
            CASE 
                WHEN p.stock_quantity = 0 THEN 'Out of Stock'
                WHEN p.stock_quantity <= p.reorder_level THEN 'Low Stock'
                ELSE 'In Stock'
            END as stock_status
        FROM products p
        LEFT JOIN suppliers s ON p.supplier_id = s.id AND s.admin_id = %s
        WHERE p.admin_id = %s
        ORDER BY p.category, p.product_name
    """, (admin_id, admin_id))
    products = cursor.fetchall()
    
    # Calculate totals
    cursor.execute("""
        SELECT 
            COUNT(*) as total_products,
            SUM(stock_quantity) as total_items,
            SUM(stock_quantity * unit_price) as total_value,
            SUM(CASE WHEN stock_quantity = 0 THEN 1 ELSE 0 END) as out_of_stock,
            SUM(CASE WHEN stock_quantity <= reorder_level AND stock_quantity > 0 THEN 1 ELSE 0 END) as low_stock
        FROM products
        WHERE admin_id = %s
    """, (admin_id,))
    summary = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('inventory_report.html', products=products, summary=summary)

@app.route('/reports/sales')
@login_required
def sales_report():
    start_date = request.args.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    admin_id = get_admin_id()
    
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            s.*,
            b.buyer_name
        FROM sales s
        LEFT JOIN buyers b ON s.buyer_id = b.id AND b.admin_id = %s
        WHERE s.admin_id = %s AND s.sale_date BETWEEN %s AND %s
        ORDER BY s.sale_date DESC
    """, (admin_id, admin_id, start_date, end_date))
    sales_data = cursor.fetchall()
    
    # Calculate summary
    cursor.execute("""
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed_orders,
            SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending_orders,
            SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled_orders
        FROM sales
        WHERE admin_id = %s AND sale_date BETWEEN %s AND %s
    """, (admin_id, start_date, end_date))
    summary = cursor.fetchone()
    
    # Top selling products
    cursor.execute("""
        SELECT 
            p.product_name,
            p.category,
            SUM(si.quantity) as total_sold,
            SUM(si.subtotal) as revenue
        FROM sale_items si
        JOIN products p ON si.product_id = p.id AND p.admin_id = %s
        JOIN sales s ON si.sale_id = s.id AND s.admin_id = %s
        WHERE s.sale_date BETWEEN %s AND %s
        GROUP BY si.product_id
        ORDER BY total_sold DESC
        LIMIT 10
    """, (admin_id, admin_id, start_date, end_date))
    top_products = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('sales_report.html', 
                         sales=sales_data, 
                         summary=summary, 
                         top_products=top_products,
                         start_date=start_date,
                         end_date=end_date)

@app.route('/reports/financial')
@login_required
def financial_report():
    start_date = request.args.get('start_date', datetime.now().replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    admin_id = get_admin_id()
    
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    
    # Revenue by month
    cursor.execute("""
        SELECT 
            DATE_FORMAT(sale_date, '%Y-%m') as month,
            SUM(total_amount) as revenue,
            COUNT(*) as orders
        FROM sales
        WHERE admin_id = %s AND sale_date BETWEEN %s AND %s AND status = 'Completed'
        GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
        ORDER BY month
    """, (admin_id, start_date, end_date))
    monthly_revenue = cursor.fetchall()
    
    # Revenue by category
    cursor.execute("""
        SELECT 
            p.category,
            SUM(si.subtotal) as revenue,
            SUM(si.quantity) as units_sold
        FROM sale_items si
        JOIN products p ON si.product_id = p.id AND p.admin_id = %s
        JOIN sales s ON si.sale_id = s.id AND s.admin_id = %s
        WHERE s.sale_date BETWEEN %s AND %s AND s.status = 'Completed'
        GROUP BY p.category
        ORDER BY revenue DESC
    """, (admin_id, admin_id, start_date, end_date))
    category_revenue = cursor.fetchall()
    
    # Financial summary
    cursor.execute("""
        SELECT 
            SUM(total_amount) as total_revenue,
            COUNT(*) as total_transactions,
            AVG(total_amount) as avg_transaction
        FROM sales
        WHERE admin_id = %s AND sale_date BETWEEN %s AND %s AND status = 'Completed'
    """, (admin_id, start_date, end_date))
    summary = cursor.fetchone()
    
    cursor.execute("SELECT SUM(stock_quantity * unit_price) as inventory_value FROM products WHERE admin_id = %s", (admin_id,))
    inventory_value = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('financial_report.html',
                         monthly_revenue=monthly_revenue,
                         category_revenue=category_revenue,
                         summary=summary,
                         inventory_value=inventory_value,
                         start_date=start_date,
                         end_date=end_date)

# ============= ALERTS & NOTIFICATIONS =============

@app.route('/alerts')
@login_required
def alerts():
    conn = get_db_connection(get_admin_db())
    cursor = conn.cursor(dictionary=True)
    admin_id = get_admin_id()
    
    # Get all active alerts
    cursor.execute("""
        SELECT 
            p.id,
            p.product_name,
            p.sku,
            p.stock_quantity,
            p.reorder_level,
            p.category,
            s.supplier_name,
            s.email as supplier_email,
            s.phone as supplier_phone
        FROM products p
        LEFT JOIN suppliers s ON p.supplier_id = s.id AND s.admin_id = %s
        WHERE p.admin_id = %s AND p.stock_quantity <= p.reorder_level
        ORDER BY p.stock_quantity ASC
    """, (admin_id, admin_id))
    alerts_list = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('alerts.html', alerts=alerts_list)

# ============= USER PROFILE =============

@app.route('/profile')
@login_required
def profile():
    admin_id = get_admin_id()
    conn = get_db_connection(MASTER_DB)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM admins WHERE id = %s", (admin_id,))
    admin = cursor.fetchone()
    
    # Get admin activity from their database
    conn2 = get_db_connection(get_admin_db())
    cursor2 = conn2.cursor(dictionary=True)
    cursor2.execute("""
        SELECT COUNT(*) as total_transactions
        FROM transactions
        WHERE admin_id = %s
    """, (admin_id,))
    activity = cursor2.fetchone()
    cursor2.close()
    conn2.close()
    
    cursor.close()
    conn.close()
    
    return render_template('profile.html', user=admin, activity=activity)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    data = request.form
    admin_id = get_admin_id()
    
    # Validate username
    valid, msg = validate_name(data.get('username'), "Username")
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('profile'))
    
    # Validate email
    valid, msg = validate_email(data.get('email'))
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('profile'))
    
    conn = get_db_connection(MASTER_DB)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE admins 
            SET username = %s, email = %s
            WHERE id = %s
        """, (data.get('username'), data.get('email'), admin_id))
        
        conn.commit()
        session['username'] = data.get('username')
        session['email'] = data.get('email')
        flash('Profile updated successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error updating profile: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('profile'))

@app.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    admin_id = get_admin_id()
    
    # Validate new password
    valid, msg = validate_password(new_password)
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('profile'))
    
    conn = get_db_connection(MASTER_DB)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT password FROM admins WHERE id = %s", (admin_id,))
    admin = cursor.fetchone()
    
    if admin['password'] != hash_password(current_password):
        flash('Current password is incorrect', 'error')
        cursor.close()
        conn.close()
        return redirect(url_for('profile'))
    
    try:
        cursor.execute("""
            UPDATE admins 
            SET password = %s
            WHERE id = %s
        """, (hash_password(new_password), admin_id))
        conn.commit()
        flash('Password changed successfully!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Error changing password: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('profile'))

if __name__ == '__main__':
    # Set debug=False in production
    app.run(debug=False, host='0.0.0.0', port=5000)