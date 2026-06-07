import pytest
from sistem_kampus import (
    StateError, PenggunaKampus, Petugas, Mahasiswa, MahasiswaReguler, 
    MahasiswaAsistenLab, ProsesorLaptop, PenyimpananLaptop, Laptop, 
    DaftarLaptop, Peminjaman, Pengembalian, Denda
)

# ==========================================
# BAGIAN 1: UNIT TESTS (1 - 25)
# ==========================================

def test_1_profil_mahasiswa():
    mhs = MahasiswaReguler(id_pengguna="M01", nama="Budi", email="budi@kampus", nim="12345")
    assert mhs.nama == "Budi"
    assert "NIM: 12345" in mhs.get_profil()
    assert mhs.batas_pinjam_hari == 3

def test_2_inisialisasi_laptop():
    laptop = Laptop("LPT-01", "Asus", "Intel i7", "16GB", "512GB")
    assert laptop.merek == "Asus"
    assert laptop.status == "Tersedia"
    assert laptop.prosesor.merek == "Intel i7"

def test_3_dunder_methods_daftar_laptop():
    inventaris = DaftarLaptop()
    laptop_1 = Laptop("LPT-01", "Asus", "Intel", "8GB", "256GB")
    inventaris.tambah_laptop(laptop_1)
    assert len(inventaris) == 1
    assert laptop_1 in inventaris

def test_4_alur_peminjaman_sukses():
    mhs = MahasiswaReguler("M01", "Budi", "budi@kampus", "12345")
    admin = Petugas("P01", "Liza", "liza@kampus", "Admin")
    laptop = Laptop("LPT-01", "Asus", "Intel i7", "16GB", "512GB")
    transaksi = Peminjaman("TX-01", mhs, laptop)
    assert transaksi.status == "Diajukan"
    transaksi.setujui(admin)
    assert transaksi.status == "Disetujui"
    transaksi.aktifkan()
    assert transaksi.status == "Aktif"

def test_5_pelanggaran_state_machine():
    mhs = MahasiswaReguler("M01", "Budi", "budi@kampus", "12345")
    laptop = Laptop("LPT-01", "Asus", "Intel i7", "16GB", "512GB")
    transaksi = Peminjaman("TX-01", mhs, laptop)
    with pytest.raises(StateError):
        transaksi.aktifkan()

def test_6_profil_petugas():
    admin = Petugas("P01", "Liza", "liza@kampus", "Kepala Lab")
    assert "Kepala Lab" in admin.get_profil()
    assert admin.nama == "Liza"

def test_7_mahasiswa_asisten_lab():
    asisten = MahasiswaAsistenLab("M02", "Siti", "siti@kampus", "54321", "LAB-01")
    assert asisten.id_lab == "LAB-01"
    assert asisten.batas_pinjam_hari == 7

def test_8_proses_pengembalian():
    mhs = MahasiswaReguler("M01", "Budi", "budi@kampus", "12345")
    admin = Petugas("P01", "Liza", "liza@kampus", "Admin")
    laptop = Laptop("LPT-01", "Asus", "Intel i7", "16GB", "512GB")
    transaksi = Peminjaman("TX-01", mhs, laptop)
    transaksi.setujui(admin)
    transaksi.aktifkan()
    kembali = Pengembalian("KMB-01", transaksi)
    kembali.proses_kembali()
    assert transaksi.status == "Selesai"
    assert laptop.status == "Tersedia"

def test_9_denda_inisialisasi():
    denda = Denda("DND-01", 50000.0)
    assert denda.id_denda == "DND-01"
    assert denda.total == 50000.0

def test_10_daftar_laptop_lanjutan():
    inventaris = DaftarLaptop()
    laptop_1 = Laptop("LPT-01", "Asus", "Intel", "8GB", "256GB")
    laptop_2 = Laptop("LPT-02", "MacBook", "M1", "8GB", "256GB")
    inventaris.tambah_laptop(laptop_1)
    inventaris.tambah_laptop(laptop_2)
    assert inventaris[1].merek == "MacBook"
    kumpulan_merek = [laptop.merek for laptop in inventaris]
    assert "Asus" in kumpulan_merek

def test_11_error_setujui_berulang():
    mhs = MahasiswaReguler("M01", "Budi", "budi@kampus", "12345")
    admin = Petugas("P01", "Liza", "liza@kampus", "Admin")
    laptop = Laptop("LPT-01", "Asus", "Intel i7", "16GB", "512GB")
    transaksi = Peminjaman("TX-01", mhs, laptop)
    transaksi.setujui(admin)
    with pytest.raises(StateError):
        transaksi.setujui(admin)

def test_12_abc_penggunakampus_error():
    with pytest.raises(TypeError):
        PenggunaKampus("U01", "Anonim", "anon@kampus")

def test_13_logtracker_output(capsys):
    mhs = MahasiswaReguler("M01", "Budi", "budi@kampus", "123")
    mhs.write_log("Testing Log")
    captured = capsys.readouterr()
    assert "Testing Log" in captured.out

def test_14_notifikasimixin_output(capsys):
    denda = Denda("D01", 50000)
    denda.kirim_notifikasi("Pesan Uji Coba")
    captured = capsys.readouterr()
    assert "Mengirim pesan: Pesan Uji Coba" in captured.out

def test_15_atribut_mahasiswa_reguler():
    mhs = MahasiswaReguler("M01", "A", "a@a.com", "111")
    assert mhs._id_pengguna == "M01"
    assert mhs._email == "a@a.com"

def test_16_atribut_petugas():
    admin = Petugas("P01", "Admin", "admin@kampus", "Staff")
    assert admin._id_pengguna == "P01"
    assert admin._email == "admin@kampus"

def test_17_prosesor_laptop_atribut():
    laptop = Laptop("L01", "Acer", "Intel i9", "16GB", "1TB")
    assert laptop.prosesor.merek == "Intel i9"

def test_18_penyimpanan_laptop_atribut():
    laptop = Laptop("L01", "Acer", "Intel i9", "16GB", "1TB")
    assert laptop.penyimpanan.ssd == "1TB"

def test_19_laptop_setter_status():
    laptop = Laptop("L01", "Acer", "Intel i9", "16GB", "1TB")
    laptop.status = "Dalam Perbaikan"
    assert laptop.status == "Dalam Perbaikan"

def test_20_peminjaman_id_transaksi():
    mhs = MahasiswaReguler("M", "A", "a", "1")
    laptop = Laptop("L", "A", "A", "A", "A")
    tx = Peminjaman("TX-99", mhs, laptop)
    assert tx.id_peminjaman == "TX-99"

def test_21_pengembalian_inisialisasi():
    mhs = MahasiswaReguler("M", "A", "a", "1")
    laptop = Laptop("L", "A", "A", "A", "A")
    tx = Peminjaman("TX", mhs, laptop)
    kembali = Pengembalian("KMB-99", tx)
    assert kembali.status == "Dicatat"

def test_22_denda_atribut_lengkap():
    denda = Denda("D-02", 75000.0)
    denda.status_bayar = "Sudah Dibayar"
    assert denda.status_bayar == "Sudah Dibayar"

def test_23_daftar_laptop_kosong():
    inventaris = DaftarLaptop()
    assert len(inventaris) == 0

def test_24_peminjaman_state_diajukan_properties():
    mhs = MahasiswaReguler("M", "A", "a", "1")
    laptop = Laptop("L", "A", "A", "A", "A")
    tx = Peminjaman("TX", mhs, laptop)
    assert tx.mahasiswa == mhs

def test_25_pengembalian_proses_kembali_log(capsys):
    mhs = MahasiswaReguler("M", "A", "a", "1")
    laptop = Laptop("L", "A", "A", "A", "A")
    tx = Peminjaman("TX", mhs, laptop)
    kembali = Pengembalian("KMB", tx)
    kembali.proses_kembali()
    captured = capsys.readouterr()
    assert "Laptop dikembalikan" in captured.out


# ==========================================
# BAGIAN 2: INTEGRATION TESTS (26 - 31)
# ==========================================

def test_26_integration_skenario_1_peminjaman_normal():
    kampus_inv = DaftarLaptop()
    kampus_inv.tambah_laptop(Laptop("L01", "Acer", "Intel i3", "8GB", "256GB"))
    mhs = MahasiswaReguler("M01", "Andi", "andi@kampus", "111")
    admin = Petugas("P01", "Budi", "budi@kampus", "Admin")

    tx = Peminjaman("TX-1", mhs, kampus_inv[0])
    tx.setujui(admin)
    tx.aktifkan()
    
    kembali = Pengembalian("K-1", tx)
    kembali.proses_kembali()

    assert tx.status == "Selesai"
    assert kampus_inv[0].status == "Tersedia"

def test_27_integration_skenario_2_asisten_lab_prioritas():
    mhs_asisten = MahasiswaAsistenLab("M02", "Siti", "siti@kampus", "222", "LAB-01")
    laptop = Laptop("L02", "Mac", "M1", "8GB", "256GB")
    tx = Peminjaman("TX-2", mhs_asisten, laptop)
    assert tx.mahasiswa.batas_pinjam_hari == 7
    assert tx.laptop.merek == "Mac"

def test_28_integration_skenario_3_pelanggaran_alur_beruntun():
    mhs = MahasiswaReguler("M03", "Citra", "citra@kampus", "333")
    laptop = Laptop("L03", "HP", "AMD", "8GB", "256GB")
    admin = Petugas("P01", "Budi", "budi@kampus", "Admin")
    tx = Peminjaman("TX-3", mhs, laptop)
    
    with pytest.raises(StateError):
        tx.aktifkan()
    tx.setujui(admin)
    with pytest.raises(StateError):
        tx.setujui(admin)

def test_29_integration_skenario_4_manajemen_inventaris_penuh():
    inventaris = DaftarLaptop()
    for i in range(5):
        inventaris.tambah_laptop(Laptop(f"L{i}", f"Merek-{i}", "CPU", "8GB", "256GB"))
    assert len(inventaris) == 5
    assert all(l.status == "Tersedia" for l in inventaris) is True

def test_30_integration_skenario_5_denda_dan_notifikasi():
    denda = Denda("D-01", 100000.0)
    denda.kirim_notifikasi("Segera bayar denda Anda!")
    assert denda.total == 100000.0
    assert denda.status_bayar == "Belum Dibayar"

def test_31_hapus_laptop_delitem():
    inventaris = DaftarLaptop()
    laptop = Laptop("L01", "Acer", "i3", "8GB", "256GB")
    inventaris.tambah_laptop(laptop)
    
    # Memastikan data ada
    assert len(inventaris) == 1
    
    # Menguji fungsi Delete / Operator __delitem__
    del inventaris[0]
    
    # Memastikan data sudah terhapus
    assert len(inventaris) == 0