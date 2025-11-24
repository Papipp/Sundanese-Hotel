from flask import Flask, render_template, request, redirect, url_for, flash, session
import datetime
import models

app = Flask(__name__)
app.secret_key = 'Sundanese' 

# --- Pembatasan sesi ---
# Decorator untuk membatasi akses ke admin

def login_required(f):
    def dash(*posisi, **konfigurasi):
        if not session.get('logged_in'):
            flash('Anda perlu login sebagai administrator.', 'danger')
            return redirect(url_for('admin_login'))
        return f(*posisi, **konfigurasi)
    dash.__name__ = f.__name__
    return dash

# --- Route User ---
# Homepage dan Pencarian Kamar

@app.route('/', methods=['GET', 'POST'])
def index():
    available_rooms = []
    
    # Set tanggal default untuk form
    today = datetime.date.today().isoformat()
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    
    # Parameter pencarian default
    search_params = {
        'check_in': today,
        'check_out': tomorrow,
        'guests': 1
    }

    if request.method == 'POST':
        # Proses pencarian kamar (dari form)
        check_in = request.form.get('check_in')
        check_out = request.form.get('check_out')
        guests = int(request.form.get('guests', 1))
        
        search_params.update({'check_in': check_in, 'check_out': check_out, 'guests': guests})

        if check_in and check_out:
            all_rooms = models.get_all_rooms()
            
            for room in all_rooms:
                # 1. Cek Kapasitas
                if room['capacity'] >= guests:
                    # 2. Cek Ketersediaan
                    if models.is_room_available(room['id'], check_in, check_out):
                        available_rooms.append(room)
            
            if not available_rooms:
                flash("Maaf, tidak ada kamar yang tersedia untuk kriteria tersebut.", "warning")

    return render_template('index.html', rooms=available_rooms, search_params=search_params)

#Halaman Booking dan Reservasi

@app.route('/book/<int:room_id>', methods=['GET'])
def booking(room_id):
    room = models.get_room_by_id(room_id)
    
    # Ambil parameter tanggal dari URL (jika ada)
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    guests = request.args.get('guests', 1)
    
    if not room or not check_in or not check_out:
        flash('Data kamar atau tanggal tidak valid.', 'danger')
        return redirect(url_for('index'))
        
    # Hitung total biaya
    try:
        date_in = datetime.datetime.strptime(check_in, '%Y-%m-%d').date()
        date_out = datetime.datetime.strptime(check_out, '%Y-%m-%d').date()
        days = (date_out - date_in).days
        total_cost = room['price'] * days if days > 0 else 0
    except ValueError:
        flash('Format tanggal tidak valid.', 'danger')
        return redirect(url_for('index'))

    if not models.is_room_available(room_id, check_in, check_out):
        flash('Kamar tidak tersedia pada tanggal yang dipilih. Silakan coba tanggal lain.', 'danger')
        return redirect(url_for('index'))
        
    return render_template('booking.html', room=room, check_in=check_in, check_out=check_out, guests=guests, total_cost=total_cost, days=days)

#memproses formulir reservasi dan menyimpan data / create
@app.route('/reserve', methods=['POST'])
def reserve():
    room_id = int(request.form.get('room_id'))
    
    # Membuat objek form_data sederhana
    form_data = {
        'check_in': request.form.get('check_in'),
        'check_out': request.form.get('check_out'),
        'guests': request.form.get('guests'),
        'full_name': request.form.get('full_name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone')
    }
    
    reservation = models.create_reservation(room_id, form_data)
    
    if reservation:
        flash(f'Reservasi berhasil! ID Anda: {reservation["id"]}. Mohon cek email Anda.', 'success')
        return redirect(url_for('index'))
    else:
        flash('Gagal membuat reservasi. Kamar mungkin sudah terisi atau tanggal tidak valid.', 'danger')
        return redirect(url_for('index'))

# --- Admin Routes ---
#Login Admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('logged_in'):
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validasi Login
        if username == 'admin' and password == 'sundanese':
            session['logged_in'] = True
            flash('Login Admin Berhasil!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Username atau Password salah!', 'danger')
            
    return render_template('admin/login.html')

#Logout Admin
@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    flash('Anda telah logout.', 'warning')
    return redirect(url_for('index'))

#Dashboard yang bisa dikses admin setelah login, serta menampilkan data kamar dan reservasi
@app.route('/admin/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    rooms = models.get_all_rooms()
    reservations = models.get_all_reservations()
    
    # Ambil data kamar untuk pre-fill form edit (jika ada parameter edit_id)
    edit_room = None
    edit_id = request.args.get('edit_id', type=int)
    if edit_id:
        edit_room = models.get_room_by_id(edit_id)

    return render_template('admin/dashboard.html', rooms=rooms, reservations=reservations, edit_room=edit_room)

# --- Route Admin ---
# Untuk menambah atau mengedit kamar serta menghapus kamar dan reservasi yang berada pada dashboard admin
@app.route('/admin/rooms/add_or_edit', methods=['POST'])
@login_required
def admin_room_crud():
    if models.add_or_update_room(request.form):
        flash('Data kamar berhasil disimpan!', 'success')
    else:
        flash('Gagal menyimpan data kamar.', 'danger')
        
    return redirect(url_for('admin_dashboard'))

# untuk penghapusan kamar
@app.route('/admin/rooms/delete/<int:room_id>')
@login_required
def admin_room_delete(room_id):
    if models.delete_room(room_id):
        flash(f'Kamar ID {room_id} dan reservasi terkait berhasil dihapus.', 'success')
    else:
        flash('Gagal menghapus kamar.', 'danger')
        
    return redirect(url_for('admin_dashboard'))

#Menghapus reservasi
@app.route('/admin/reservations/delete/<int:res_id>')
@login_required
def admin_reservation_delete(res_id):
    if models.delete_reservation(res_id):
        flash(f'Reservasi ID {res_id} berhasil dibatalkan.', 'success')
    else:
        flash('Gagal membatalkan reservasi.', 'danger')
        
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)