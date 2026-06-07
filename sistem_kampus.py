from abc import ABC, abstractmethod
from datetime import datetime

class StateError(Exception):
    pass

class LogTrackerMixin:
    def write_log(self, aktivitas: str) -> None:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG {waktu}] {aktivitas}")

class NotifikasiMixin:
    def kirim_notifikasi(self, pesan: str) -> None:
        print(f"[NOTIFIKASI] Mengirim pesan: {pesan}")

class PenggunaKampus(ABC, LogTrackerMixin):
    def __init__(self, id_pengguna: str, nama: str, email: str, **kwargs):
        super().__init__(**kwargs)
        self._id_pengguna = id_pengguna
        self._nama = nama
        self._email = email

    @property
    def nama(self) -> str:
        return self._nama

    @abstractmethod
    def get_profil(self) -> str:
        pass

class Petugas(PenggunaKampus):
    def __init__(self, id_pengguna: str, nama: str, email: str, jabatan: str, **kwargs):
        super().__init__(id_pengguna=id_pengguna, nama=nama, email=email, **kwargs)
        self.jabatan = jabatan

    def get_profil(self) -> str:
        return f"Petugas: {self.nama} ({self.jabatan})"

class Mahasiswa(PenggunaKampus):
    def __init__(self, id_pengguna: str, nama: str, email: str, nim: str, **kwargs):
        super().__init__(id_pengguna=id_pengguna, nama=nama, email=email, **kwargs)
        self._nim = nim

    def get_profil(self) -> str:
        return f"Mahasiswa: {self.nama} (NIM: {self._nim})"

class MahasiswaReguler(Mahasiswa):
    def __init__(self, id_pengguna: str, nama: str, email: str, nim: str, **kwargs):
        super().__init__(id_pengguna=id_pengguna, nama=nama, email=email, nim=nim, **kwargs)
        self.batas_pinjam_hari = 3

class MahasiswaAsistenLab(Mahasiswa):
    def __init__(self, id_pengguna: str, nama: str, email: str, nim: str, id_lab: str, **kwargs):
        super().__init__(id_pengguna=id_pengguna, nama=nama, email=email, nim=nim, **kwargs)
        self.id_lab = id_lab
        self.batas_pinjam_hari = 7

class ProsesorLaptop:
    def __init__(self, merek: str, clock_speed: str):
        self.merek = merek
        self.clock_speed = clock_speed

class PenyimpananLaptop:
    def __init__(self, ram: str, ssd: str):
        self.ram = ram
        self.ssd = ssd

class Laptop:
    def __init__(self, id_laptop: str, merek: str, merk_cpu: str, ram: str, ssd: str):
        self._id_laptop = id_laptop
        self._merek = merek
        self._status = "Tersedia"
        self.prosesor = ProsesorLaptop(merek=merk_cpu, clock_speed="3.2GHz")
        self.penyimpanan = PenyimpananLaptop(ram=ram, ssd=ssd)

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status_baru: str) -> None:
        self._status = status_baru

    @property
    def merek(self) -> str:
        return self._merek

class DaftarLaptop:
    def __init__(self):
        self._koleksi_laptop = []

    def tambah_laptop(self, laptop: Laptop):
        self._koleksi_laptop.append(laptop)

    def __len__(self):
        return len(self._koleksi_laptop)

    def __iter__(self):
        return iter(self._koleksi_laptop)

    def __contains__(self, laptop: Laptop):
        return laptop in self._koleksi_laptop

    def __getitem__(self, index: int):
        return self._koleksi_laptop[index]

    def __delitem__(self, index: int):
        del self._koleksi_laptop[index]

class Peminjaman(NotifikasiMixin, LogTrackerMixin):
    STATES = ["Diajukan", "Disetujui", "Aktif", "Selesai", "Terlambat"]

    def __init__(self, id_peminjaman: str, mahasiswa: Mahasiswa, laptop: Laptop):
        self.id_peminjaman = id_peminjaman
        self.mahasiswa = mahasiswa
        self.laptop = laptop
        self._status_transaksi = "Diajukan"
        self.write_log(f"Peminjaman {id_peminjaman} diajukan oleh {mahasiswa.nama}")

    @property
    def status(self) -> str:
        return self._status_transaksi

    def setujui(self, petugas: Petugas) -> None:
        if self._status_transaksi != "Diajukan":
            raise StateError("Hanya peminjaman berstatus 'Diajukan' yang bisa disetujui.")
        self._status_transaksi = "Disetujui"
        self.laptop.status = "Dipinjam"
        self.write_log(f"Peminjaman {self.id_peminjaman} disetujui oleh {petugas.nama}")
        self.kirim_notifikasi(f"Halo {self.mahasiswa.nama}, peminjaman laptop Anda disetujui.")

    def aktifkan(self) -> None:
        if self._status_transaksi != "Disetujui":
            raise StateError("Peminjaman harus 'Disetujui' sebelum diaktifkan.")
        self._status_transaksi = "Aktif"
        self.write_log(f"Peminjaman {self.id_peminjaman} berstatus Aktif. Laptop diserahkan.")

class Pengembalian(LogTrackerMixin):
    def __init__(self, id_pengembalian: str, peminjaman: Peminjaman):
        self.id_pengembalian = id_pengembalian
        self.peminjaman = peminjaman
        self.status = "Dicatat"

    def proses_kembali(self):
        self.peminjaman._status_transaksi = "Selesai"
        self.peminjaman.laptop.status = "Tersedia"
        self.write_log(f"Pengembalian {self.id_pengembalian} diproses. Laptop dikembalikan.")

class Denda(NotifikasiMixin):
    def __init__(self, id_denda: str, total: float):
        self.id_denda = id_denda
        self.total = total
        self.status_bayar = "Belum Dibayar"

# ==========================================
# SIMULASI PROGRAM UTAMA DIABAIKAN PYTEST
# ==========================================
if __name__ == "__main__":  # pragma: no cover
    pass