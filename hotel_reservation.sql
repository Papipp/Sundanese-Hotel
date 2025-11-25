-- inisiasi query sqlnya --

-- Buat Database
CREATE DATABASE hotel_reservation;

-- Buat Tabel Rooms
CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    capacity INT NOT NULL,
    description TEXT,
    img_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Buat Tabel Reservations
CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    room_name VARCHAR(100) NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    guest_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    guests INT NOT NULL,
    booking_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
);

-- Insert Data Kamar
INSERT INTO rooms (name, price, capacity, description, img_url) VALUES
('Standard', 500000, 2, 'Pilihan sempurna untuk pelancong yang mencari istirahat nyaman dan fungsional setelah seharian beraktivitas. Dilengkapi fasilitas dasar yang lengkap dan kamar mandi dalam yang bersih.', 'https://github.com/Papipp/pidev/blob/main/img/standar.jpg?raw=true'),
('Standard', 500000, 2, 'Pilihan sempurna untuk pelancong yang mencari istirahat nyaman dan fungsional setelah seharian beraktivitas. Dilengkapi fasilitas dasar yang lengkap dan kamar mandi dalam yang bersih.', 'https://github.com/Papipp/pidev/blob/main/img/standar.jpg?raw=true'),
('Standard', 500000, 2, 'Pilihan sempurna untuk pelancong yang mencari istirahat nyaman dan fungsional setelah seharian beraktivitas. Dilengkapi fasilitas dasar yang lengkap dan kamar mandi dalam yang bersih.', 'https://github.com/Papipp/pidev/blob/main/img/standar.jpg?raw=true'),
('Standard', 500000, 2, 'Pilihan sempurna untuk pelancong yang mencari istirahat nyaman dan fungsional setelah seharian beraktivitas. Dilengkapi fasilitas dasar yang lengkap dan kamar mandi dalam yang bersih.', 'https://github.com/Papipp/pidev/blob/main/img/standar.jpg?raw=true'),
('Superior', 750000, 4, 'Peningkatan dari Standard, menawarkan ruang gerak ekstra dan perabotan yang lebih modern. Nikmati suasana yang lebih tenang dan mungkin pemandangan yang lebih baik dari jendela Anda.', 'https://github.com/Papipp/pidev/blob/main/img/superior.jpg?raw=true'),
('Superior', 750000, 4, 'Peningkatan dari Standard, menawarkan ruang gerak ekstra dan perabotan yang lebih modern. Nikmati suasana yang lebih tenang dan mungkin pemandangan yang lebih baik dari jendela Anda.', 'https://github.com/Papipp/pidev/blob/main/img/superior.jpg?raw=true'),
('Superior', 750000, 4, 'Peningkatan dari Standard, menawarkan ruang gerak ekstra dan perabotan yang lebih modern. Nikmati suasana yang lebih tenang dan mungkin pemandangan yang lebih baik dari jendela Anda.', 'https://github.com/Papipp/pidev/blob/main/img/superior.jpg?raw=true'),
('Superior', 750000, 4, 'Peningkatan dari Standard, menawarkan ruang gerak ekstra dan perabotan yang lebih modern. Nikmati suasana yang lebih tenang dan mungkin pemandangan yang lebih baik dari jendela Anda.', 'https://github.com/Papipp/pidev/blob/main/img/superior.jpg?raw=true'),
('Delux', 1000000, 4, 'Kamar yang luas dengan desain mewah dan tempat tidur king/queen size premium. Ideal untuk relaksasi total, dilengkapi area duduk yang nyaman dan fasilitas kamar mandi yang ditingkatkan.', 'https://github.com/Papipp/pidev/blob/main/img/delux1.jpg?raw=true'),
('Delux', 1000000, 4, 'Kamar yang luas dengan desain mewah dan tempat tidur king/queen size premium. Ideal untuk relaksasi total, dilengkapi area duduk yang nyaman dan fasilitas kamar mandi yang ditingkatkan.', 'https://github.com/Papipp/pidev/blob/main/img/delux1.jpg?raw=true'),
('Delux', 1000000, 4, 'Kamar yang luas dengan desain mewah dan tempat tidur king/queen size premium. Ideal untuk relaksasi total, dilengkapi area duduk yang nyaman dan fasilitas kamar mandi yang ditingkatkan.', 'https://github.com/Papipp/pidev/blob/main/img/delux1.jpg?raw=true'),
('Delux', 1000000, 4, 'Kamar yang luas dengan desain mewah dan tempat tidur king/queen size premium. Ideal untuk relaksasi total, dilengkapi area duduk yang nyaman dan fasilitas kamar mandi yang ditingkatkan.', 'https://github.com/Papipp/pidev/blob/main/img/delux1.jpg?raw=true'),
('Suite', 1500000, 4, 'Suite sejati dengan kamar tidur utama dan ruang tamu/keluarga yang dipisahkan oleh pintu. Ideal untuk keluarga atau tamu yang menerima kunjungan, menawarkan privasi dan kemewahan tingkat tinggi.', 'https://github.com/Papipp/pidev/blob/main/img/suite.jpg?raw=true'),
('Suite', 1500000, 4, 'Suite sejati dengan kamar tidur utama dan ruang tamu/keluarga yang dipisahkan oleh pintu. Ideal untuk keluarga atau tamu yang menerima kunjungan, menawarkan privasi dan kemewahan tingkat tinggi.', 'https://github.com/Papipp/pidev/blob/main/img/suite.jpg?raw=true'),
('Suite', 1500000, 4, 'Suite sejati dengan kamar tidur utama dan ruang tamu/keluarga yang dipisahkan oleh pintu. Ideal untuk keluarga atau tamu yang menerima kunjungan, menawarkan privasi dan kemewahan tingkat tinggi.', 'https://github.com/Papipp/pidev/blob/main/img/suite.jpg?raw=true'),
('Suite', 1500000, 4, 'Suite sejati dengan kamar tidur utama dan ruang tamu/keluarga yang dipisahkan oleh pintu. Ideal untuk keluarga atau tamu yang menerima kunjungan, menawarkan privasi dan kemewahan tingkat tinggi.', 'https://github.com/Papipp/pidev/blob/main/img/suite.jpg?raw=true'),
('Presidential Suite', 2500000, 4, 'Kamar terbesar dan termewah di hotel kami. Menawarkan tata letak seperti apartemen, termasuk ruang makan, dapur kecil, kantor pribadi, dan layanan butler 24 jam. Puncak dari kemewahan dan privasi.', 'https://github.com/Papipp/pidev/blob/main/img/president_suite.jpg?raw=true'),
('Presidential Suite', 2500000, 4, 'Kamar terbesar dan termewah di hotel kami. Menawarkan tata letak seperti apartemen, termasuk ruang makan, dapur kecil, kantor pribadi, dan layanan butler 24 jam. Puncak dari kemewahan dan privasi.', 'https://github.com/Papipp/pidev/blob/main/img/president_suite.jpg?raw=true'),
('Presidential Suite', 2500000, 4, 'Kamar terbesar dan termewah di hotel kami. Menawarkan tata letak seperti apartemen, termasuk ruang makan, dapur kecil, kantor pribadi, dan layanan butler 24 jam. Puncak dari kemewahan dan privasi.', 'https://github.com/Papipp/pidev/blob/main/img/president_suite.jpg?raw=true'),
('Presidential Suite', 2500000, 4, 'Kamar terbesar dan termewah di hotel kami. Menawarkan tata letak seperti apartemen, termasuk ruang makan, dapur kecil, kantor pribadi, dan layanan butler 24 jam. Puncak dari kemewahan dan privasi.', 'https://github.com/Papipp/pidev/blob/main/img/president_suite.jpg?raw=true'),
('Presidential Suite', 2500000, 4, 'Kamar terbesar dan termewah di hotel kami. Menawarkan tata letak seperti apartemen, termasuk ruang makan, dapur kecil, kantor pribadi, dan layanan butler 24 jam. Puncak dari kemewahan dan privasi.', 'https://github.com/Papipp/pidev/blob/main/img/president_suite.jpg?raw=true');