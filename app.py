from flask import Flask,request,render_template,session,redirect
from models import init_db,get_db_connection

app = Flask(__name__)
app.secret_key = 'secret123'
init_db()
@app.route('/')
def home():
    return "Tutor Booking System Running 🚀"
# ✅ Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', (name, email, password, role))

        conn.commit()
        conn.close()

        return "User Registered Successfully ✅"

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM users WHERE email = ? AND password = ?
        ''', (email, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            # store session
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']

            return redirect('/dashboard')
        else:
            return "Invalid Credentials ❌"

    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f"Welcome {session['name']} ({session['role']}) 🎉"
    else:
        return redirect('/login')
 
@app.route('/add-slot', methods=['GET', 'POST'])
def add_slot():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        tutor_id = session['user_id']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO slots (tutor_id, date, time)
            VALUES (?, ?, ?)
        ''', (tutor_id, date, time))

        conn.commit()
        conn.close()

        return "Slot Added Successfully ✅"

    return render_template('add_slot.html')
@app.route('/my-slots')
def my_slots():
    if 'user_id' not in session:
        return redirect('/login')

    tutor_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM slots WHERE tutor_id = ?
    ''', (tutor_id,))

    slots = cursor.fetchall()
    conn.close()

    return render_template('view_slots.html', slots=slots)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')   
if __name__ == '__main__':
    app.run(debug=True)


 