from flask import Flask, request, jsonify , render_template
import sqlite3


app = Flask(__name__)

# ---------- Database Setup ----------
def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()

# ---------- Routes ----------

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Flask User Manager API!"})

# Serve GUI
@app.route('/ui')
def ui():
    return render_template('index.html')

# ... rest of your routes (register_bulk, users, update_user, delete_user) ...

# Create Users (Bulk)
@app.route('/register_bulk', methods=['POST'])
def register_bulk_users():
    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({"error": "Send a list of users"}), 400

    success = []
    failed = []

    with sqlite3.connect('users.db', timeout=10) as conn:
        cursor = conn.cursor()
        for user in data:
            name = user.get('name')
            email = user.get('email')
            if not name or not email:
                failed.append({"user": user, "error": "Missing name/email"})
                continue
            try:
                cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                success.append(user)
            except sqlite3.IntegrityError:
                failed.append({"user": user, "error": "Email already exists"})
        conn.commit()

    # Prepare response
    response = {"success": success}
    if failed:  # include failed only if not empty
        response["failed"] = failed

    return jsonify(response), 201

# Read Users
@app.route('/users', methods=['GET'])
def get_users():
    with sqlite3.connect('users.db', timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in cursor.fetchall()]
    return jsonify(users), 200

# Update User
@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name and not email:
        return jsonify({"error": "Provide at least one field (name or email) to update"}), 400

    with sqlite3.connect('users.db', timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if name:
            cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
        if email:
            try:
                cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))
            except sqlite3.IntegrityError:
                return jsonify({"error": "Email already exists!"}), 409

        conn.commit()
    return jsonify({"message": f"User with id {user_id} updated successfully"}), 200

# Delete User
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with sqlite3.connect('users.db', timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
    return jsonify({"message": f"User with id {user_id} deleted successfully"}), 200

# ---------- Run ----------
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
