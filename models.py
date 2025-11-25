import datetime
import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Membuat koneksi ke database MySQL
def get_db_connection():
    
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Class untuk mengelola data kamar hotel
class Room:
    
#Mengambil semua data kamar dari database
    @staticmethod
    def get_all():

        connection = get_db_connection()
        if not connection:
            return []
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM rooms ORDER BY id")
                rooms = cursor.fetchall()
                return rooms
        except Exception as e:
            print(f"Error getting rooms: {e}")
            return []
        finally:
            connection.close()
# Mengambil data kamar berdasarkan ID
    @staticmethod
    def get_by_id(room_id):

        connection = get_db_connection()
        if not connection:
            return None
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
                room = cursor.fetchone()
                return room
        except Exception as e:
            print(f"Error getting room by id: {e}")
            return None
        finally:
            connection.close()
    
#Mengecek ketersediaan kamar pada tanggal tertentu
    @staticmethod
    def is_available(room_id, check_in_str, check_out_str):

        try:
            check_in = datetime.datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.datetime.strptime(check_out_str, '%Y-%m-%d').date()
            
            # Validasi: check-in harus sebelum check-out
            if check_in >= check_out:
                return False
            
            connection = get_db_connection()
            if not connection:
                return False
            
            try:
                with connection.cursor() as cursor:
                    # Query untuk mencari tabrakan tanggal
                    cursor.execute("""
                        SELECT COUNT(*) as count FROM reservations
                        WHERE room_id = %s
                        AND check_in < %s
                        AND check_out > %s
                    """, (room_id, check_out_str, check_in_str))
                    
                    result = cursor.fetchone()
                    return result['count'] == 0
                    
            finally:
                connection.close()
                
        except ValueError:
            return False
        except Exception as e:
            print(f"Error checking availability: {e}")
            return False

# Menambah atau mengupdate data kamar
    @staticmethod
    def add_or_update(room_data):
        connection = get_db_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                room_id = room_data.get('id')
                
                if room_id:
                    # UPDATE
                    cursor.execute("""
                        UPDATE rooms
                        SET name = %s, price = %s, capacity = %s, description = %s
                        WHERE id = %s
                    """, (
                        room_data['name'],
                        int(room_data['price']),
                        int(room_data['capacity']),
                        room_data.get('description', ''),
                        int(room_id)
                    ))
                else:
                    # CREATE
                    cursor.execute("""
                        INSERT INTO rooms (name, price, capacity, description, img_url)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        room_data['name'],
                        int(room_data['price']),
                        int(room_data['capacity']),
                        room_data.get('description', f"Kamar {room_data['name']}"),
                        room_data.get('img_url', '/static/bg-hotel.png')
                    ))
                
                connection.commit()
                return True
                
        except Exception as e:
            print(f"Error add/update room: {e}")
            connection.rollback()
            return False
        finally:
            connection.close()

#Menghapus kamar berdasarkan ID Reservasi terkait akan terhapus otomatis karena ON DELETE CASCADE
    @staticmethod
    def delete(room_id):

        connection = get_db_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
                connection.commit()
                return True
                
        except Exception as e:
            print(f"Error delete room: {e}")
            connection.rollback()
            return False
        finally:
            connection.close()

# Class untuk mengelola data reservasi
class Reservation:
    
    @staticmethod
    def get_all():  
        connection = get_db_connection()
        if not connection:
            return []
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM reservations 
                    ORDER BY booking_date DESC, id DESC
                """)
                reservations = cursor.fetchall()
                return reservations
        except Exception as e:
            print(f"Error getting reservations: {e}")
            return []
        finally:
            connection.close()

# Membuat reservasi baru
    @staticmethod
    def create(room_id, form_data):
     
        # Cek ketersediaan terlebih dahulu
        if not Room.is_available(room_id, form_data['check_in'], form_data['check_out']):
            return None
        
        room = Room.get_by_id(room_id)
        if not room:
            return None
        
        connection = get_db_connection()
        if not connection:
            return None
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO reservations 
                    (room_id, room_name, check_in, check_out, guest_name, email, phone, guests, booking_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    room_id,
                    room['name'],
                    form_data['check_in'],
                    form_data['check_out'],
                    form_data['full_name'],
                    form_data['email'],
                    form_data['phone'],
                    int(form_data['guests']),
                    datetime.date.today().isoformat()
                ))
                
                connection.commit()
                
                # Ambil ID yang baru dibuat
                reservation_id = cursor.lastrowid
                
                # Return data reservasi lengkap
                return {
                    "id": reservation_id,
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
                
        except Exception as e:
            print(f"Error creating reservation: {e}")
            connection.rollback()
            return None
        finally:
            connection.close()

# Menghapus reservasi berdasarkan  ID
    @staticmethod
    def delete(res_id):
        connection = get_db_connection()
        if not connection:
            return False
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM reservations WHERE id = %s", (res_id,))
                connection.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Error deleting reservation: {e}")
            connection.rollback()
            return False
        finally:
            connection.close()


# Export semua fungsi yang dibutuhkan
__all__ = [
    'Room',
    'Reservation',
    'get_all_rooms',
    'get_room_by_id',
    'is_room_available',
    'add_or_update_room',
    'delete_room',
    'get_all_reservations',
    'create_reservation',
    'delete_reservation'
]

# Fungsi wrapper untuk kompatibilitas dengan kode lama, karena disinio saya mhanya mengganti models dan app nya saja, tyidak dengan html atau template jinjanya.
def get_all_rooms():
    return Room.get_all()

def get_room_by_id(room_id):
    return Room.get_by_id(room_id)

def is_room_available(room_id, check_in_str, check_out_str):
    return Room.is_available(room_id, check_in_str, check_out_str)

def add_or_update_room(room_data):
    return Room.add_or_update(room_data)

def delete_room(room_id):
    return Room.delete(room_id)

def get_all_reservations():
    return Reservation.get_all()

def create_reservation(room_id, form_data):
    return Reservation.create(room_id, form_data)

def delete_reservation(res_id):
    return Reservation.delete(res_id)