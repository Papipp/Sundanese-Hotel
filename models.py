import datetime
import random

# Dictonary statis untuk menyimpan data kamar dan reservasi
ROOMS = [
    {"id": 1, "name": "Standard", "price": 500000, "capacity": 3, "description": "Kamar yang nyaman untuk satu orang.","img_url": "/static/standar.jpg"},
    {"id": 2, "name": "Deluxe", "price": 850000, "capacity": 2, "description": "Kamar mewah dengan kasur ukuran double.","img_url": "/static/delux1.jpg"},
    {"id": 3, "name": "VIP Suite", "price": 1500000, "capacity": 4, "description": "Suite luas dengan dua kamar tidur, cocok untuk keluarga besar.","img_url": "/static/vip.jpg"}
]

RESERVATIONS = []

# Fungsi Model untuk mengelola data kamar dan reservasi
# Mengembalikan semua kamar
def get_all_rooms():
    return ROOMS

#mengembalikan kamar berdasarkan ID
def get_room_by_id(room_id):
    return next((room for room in ROOMS if room["id"] == room_id), None)

# Mengembalikan semua reservasi
def get_all_reservations():
    return RESERVATIONS

# Cek ketersediaan kamar berdasarkan tanggal
def is_room_available(room_id, check_in_str, check_out_str):
    
    # Konversi tanggal ke dictonary date
    check_in = datetime.datetime.strptime(check_in_str, '%Y-%m-%d').date()
    check_out = datetime.datetime.strptime(check_out_str, '%Y-%m-%d').date()
    
    # Validasi dasar: check-in harus sebelum check-out
    if check_in >= check_out:
        return False
        
    for res in RESERVATIONS:
        if res["room_id"] == room_id:
            res_in = datetime.datetime.strptime(res["check_in"], '%Y-%m-%d').date()
            res_out = datetime.datetime.strptime(res["check_out"], '%Y-%m-%d').date()

            # handling logika tabrakan:
            if check_in < res_out and check_out > res_in:
                return False
                
    return True

# Membuat reservasi baru
def create_reservation(room_id, form_data):
    # Cek ketersediaan lagi sebelum membuat reservasi
    if not is_room_available(room_id, form_data['check_in'], form_data['check_out']):
        return None # Jika Kamar tidak tersedia
    new_id = random.randint(100, 999) # ID Reservasi acak
    room = get_room_by_id(room_id)
    if not room:
        return None
        
    reservation = {
        "id": new_id,
        "room_id": room_id,
        "room_name": room['name'],
        "check_in": form_data['check_in'],
        "check_out": form_data['check_out'],
        "guest_name": form_data['full_name'],
        "email": form_data['email'],
        "phone": form_data['phone'],
        "guests": int(form_data['guests']),
        "booking_date": datetime.date.today().isoformat()
    }
    
    RESERVATIONS.append(reservation)
    return reservation

# Menambah atau mengedit kamar, Create/Update
def add_or_update_room(room_data):
    room_id = room_data.get('id')
    
    if room_id:
        # UPDATE
        room_id = int(room_id)
        room = get_room_by_id(room_id)
        if room:
            room.update({
                "name": room_data['name'],
                "price": int(room_data['price']),
                "capacity": int(room_data['capacity']),
                "description": room_data.get('description', room['description'])
            })
            return True
    else:
        # CREATE
        new_id = ROOMS[-1]['id'] + 1 if ROOMS else 1
        new_room = {
            "id": new_id,
            "name": room_data['name'],
            "price": int(room_data['price']),
            "capacity": int(room_data['capacity']),
            "description": f"Kamar {room_data['name']} yang luar biasa."
        }
        ROOMS.append(new_room)
        return True
        
    return False

# untuk menghapus kamar
def delete_room(room_id):
    global ROOMS
    room_id = int(room_id)
    ROOMS = [room for room in ROOMS if room['id'] != room_id]

    # Hapus juga reservasi terkait
    global RESERVATIONS
    RESERVATIONS = [res for res in RESERVATIONS if res['room_id'] != room_id]
    return True

# Menghapus reservasi
def delete_reservation(res_id):
    global RESERVATIONS
    res_id = int(res_id)
    initial_length = len(RESERVATIONS)
    RESERVATIONS = [res for res in RESERVATIONS if res['id'] != res_id]
    return len(RESERVATIONS) < initial_length