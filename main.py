# Program Manajemen Siswa Magang
# Versi: 2.0 (Disempurnakan dengan log dan edit nama)

import os
from datetime import datetime
import json

# List untuk menyimpan data siswa
data_siswa = []

# Path log file
LOG_PATH = 'data/log.txt'
DATA_PATH = 'data/siswa.json'

def log_aktivitas(aksi, detail):
    os.makedirs('data', exist_ok=True)
    with open(LOG_PATH, 'a') as f:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{waktu}] {aksi.upper()}: {detail}\n")

def clear_screen():
    print("\n" * 8)

def tampilkan_menu():
    clear_screen()
    print("\n=== APLIKASI MANAJEMEN SISWA MAGANG ===")
    print("1. Tambah Data Siswa")
    print("2. Tampilkan Semua Data Siswa")
    print("3. Cari Data Siswa")
    print("4. Hapus Data Siswa")
    print("5. Ubah Nama Siswa")
    print("6. Lihat Riwayat Log")
    print("7. Keluar")
    print("=======================================")

def tekan_enter_kembali():
    input("\nTekan Enter untuk kembali ke menu utama...")

def validasi_input(prompt, tipe='str', allow_empty=False, pilihan=None):
    while True:
        try:
            nilai = input(prompt).strip()
            if not nilai and not allow_empty:
                print("Input tidak boleh kosong!")
                continue
            if tipe == 'int':
                return int(nilai)
            elif tipe == 'str':
                if pilihan and nilai.lower() not in [p.lower() for p in pilihan]:
                    print(f"Input harus salah satu dari: {', '.join(pilihan)}")
                    continue
                return nilai
        except ValueError:
            print("Input tidak valid. Silakan coba lagi.")

def simpan_data():
    os.makedirs('data', exist_ok=True)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data_siswa, f, ensure_ascii=False, indent=2)

def muat_data():
    global data_siswa
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            try:
                data_siswa = json.load(f)
            except Exception:
                data_siswa = []

def tambah_siswa():
    while True:
        clear_screen()
        print("\n--- Tambah Data Siswa ---")
        nis = validasi_input("Masukkan NIS (angka): ", tipe='int')
        for siswa in data_siswa:
            if siswa['nis'] == nis:
                print(f"\nNIS {nis} sudah terdaftar atas nama {siswa['nama']}")
                pilihan = validasi_input("Lanjutkan? (Ya / Tidak): ", tipe='str', pilihan=['Ya', 'Tidak'])
                if pilihan.lower() == 'tidak':
                    return
                break
        nama = validasi_input("Masukkan Nama: ")
        jurusan = validasi_input("Masukkan Jurusan: ")
        sekolah = validasi_input("Masukkan Sekolah: ")
        status = validasi_input("Masukkan Status Magang (Aktif/Selesai): ", pilihan=['Aktif', 'Selesai']).capitalize()
        siswa = {'nis': nis, 'nama': nama, 'jurusan': jurusan, 'sekolah': sekolah, 'status': status}
        data_siswa.append(siswa)
        simpan_data()
        log_aktivitas("ADD", f"Data siswa {nama} (NIS: {nis}) ditambahkan.")
        print("\n\u2713 Data siswa berhasil ditambahkan!")
        lagi = validasi_input("\nTambah data siswa lagi? (Ya/Tidak): ", tipe='str', pilihan=['Ya', 'Tidak'])
        if lagi.lower() == 'tidak':
            return

def format_tabel_siswa(data):
    # Lebar maksimal tiap kolom
    col_widths = {
        'No.': 5,
        'NIS': 10,
        'Nama': 20,
        'Jurusan': 15,
        'Sekolah': 15,
        'Status': 10
    }

    import textwrap

    def wrap(teks, lebar):
        return textwrap.wrap(str(teks), lebar) or [""]

    if not data:
        print("Tidak ada data siswa.")
        return

    print("-" * 80)
    print(f"{'No.':<{col_widths['No.']}} {'NIS':<{col_widths['NIS']}} {'Nama':<{col_widths['Nama']}} {'Jurusan':<{col_widths['Jurusan']}} {'Sekolah':<{col_widths['Sekolah']}} {'Status':<{col_widths['Status']}}")
    print("-" * 80)
    for idx, siswa in enumerate(data, 1):
        # Bungkus setiap field sesuai lebar kolom
        lines = [
            wrap(idx, col_widths['No.']),
            wrap(siswa['nis'], col_widths['NIS']),
            wrap(siswa['nama'], col_widths['Nama']),
            wrap(siswa['jurusan'], col_widths['Jurusan']),
            wrap(siswa['sekolah'], col_widths['Sekolah']),
            wrap(siswa['status'], col_widths['Status'])
        ]
        max_lines = max(len(l) for l in lines)
        # Print baris per baris
        for i in range(max_lines):
            print(
                f"{lines[0][i] if i < len(lines[0]) else '':<{col_widths['No.']}} "
                f"{lines[1][i] if i < len(lines[1]) else '':<{col_widths['NIS']}} "
                f"{lines[2][i] if i < len(lines[2]) else '':<{col_widths['Nama']}} "
                f"{lines[3][i] if i < len(lines[3]) else '':<{col_widths['Jurusan']}} "
                f"{lines[4][i] if i < len(lines[4]) else '':<{col_widths['Sekolah']}} "
                f"{lines[5][i] if i < len(lines[5]) else '':<{col_widths['Status']}}"
            )
    print("-" * 80)
    print(f"Total: {len(data)} siswa")

def tampilkan_semua_siswa():
    clear_screen()
    print("\n--- Daftar Semua Siswa Magang ---")
    format_tabel_siswa(data_siswa)
    tekan_enter_kembali()

def cari_siswa():
    while True:
        clear_screen()
        print("\n--- Cari Data Siswa ---")
        if not data_siswa:
            print("Database siswa kosong.")
            tekan_enter_kembali()
            return
        keyword = input("Masukkan NIS atau Nama siswa yang dicari: ").strip().lower()
        hasil_pencarian = [s for s in data_siswa if keyword in str(s['nis']).lower() or keyword in s['nama'].lower()]
        clear_screen()
        print(f"\nHasil Pencarian untuk '{keyword}':")
        if not hasil_pencarian:
            print("Tidak ditemukan siswa dengan kata kunci tersebut.")
        else:
            format_tabel_siswa(hasil_pencarian)
        lagi = validasi_input("\nCari data siswa lagi? (Ya/Tidak): ", tipe='str', pilihan=['Ya', 'Tidak'])
        if lagi.lower() == 'tidak':
            return

def hapus_siswa():
    while True:
        clear_screen()
        print("\n--- Hapus Data Siswa ---")
        if not data_siswa:
            print("Database siswa kosong.")
            tekan_enter_kembali()
            return
        format_tabel_siswa(data_siswa)
        try:
            nis_hapus = int(input("\nMasukkan NIS siswa yang akan dihapus (0 untuk batal): "))
        except ValueError:
            print("NIS harus berupa angka!")
            tekan_enter_kembali()
            continue
        if nis_hapus == 0:
            return
        for i, siswa in enumerate(data_siswa):
            if siswa['nis'] == nis_hapus:
                print("\nData siswa yang akan dihapus:")
                print("-" * 40)
                for k, v in siswa.items():
                    print(f"{k.capitalize():<10}: {v}")
                print("-" * 40)
                konfirmasi = validasi_input("\nYakin hapus? (Ya/Tidak): ", tipe='str', pilihan=['Ya', 'Tidak'])
                if konfirmasi.lower() == 'ya':
                    log_aktivitas("DELETE", f"Data siswa {siswa['nama']} (NIS: {nis_hapus}) dihapus.")
                    del data_siswa[i]
                    simpan_data()
                    print("\n\u2713 Data siswa berhasil dihapus!")
                else:
                    print("\nPenghapusan dibatalkan.")
                break
        else:
            print(f"\nTidak ditemukan siswa dengan NIS {nis_hapus}")
        lagi = validasi_input("\nHapus data siswa lagi? (Ya/Tidak): ", tipe='str', pilihan=['Ya', 'Tidak'])
        if lagi.lower() == 'tidak':
            return

def ubah_nama_siswa():
    clear_screen()
    print("\n--- Ubah Nama Siswa ---")
    if not data_siswa:
        print("Database siswa kosong.")
        tekan_enter_kembali()
        return
    try:
        nis_edit = int(input("Masukkan NIS siswa yang ingin diubah namanya: "))
    except ValueError:
        print("NIS harus berupa angka.")
        tekan_enter_kembali()
        return
    for siswa in data_siswa:
        if siswa['nis'] == nis_edit:
            print(f"Nama sebelumnya: {siswa['nama']}")
            nama_baru = input("Masukkan nama baru: ").strip()
            if nama_baru:
                nama_lama = siswa['nama']
                siswa['nama'] = nama_baru
                simpan_data()
                log_aktivitas("EDIT", f"Nama siswa NIS {nis_edit} diubah dari \"{nama_lama}\" ke \"{nama_baru}\". Status: {siswa['status'].upper()}")
                print("\n\u2713 Nama berhasil diubah.")
            else:
                print("Nama baru tidak boleh kosong.")
            tekan_enter_kembali()
            return
    print("Siswa dengan NIS tersebut tidak ditemukan.")
    tekan_enter_kembali()

def tampilkan_log():
    clear_screen()
    print("\n--- Riwayat Aktivitas ---")
    if not os.path.exists(LOG_PATH):
        print("Belum ada riwayat aktivitas.")
    else:
        with open(LOG_PATH, 'r') as f:
            isi = f.read().strip()
            if not isi:
                print("Belum ada riwayat aktivitas.")
            else:
                print(isi)
    tekan_enter_kembali()

def main():
    clear_screen()
    print("Selamat datang di Aplikasi Manajemen Siswa Magang")
    print("Versi 2.0 - Disempurnakan")
    print("\nTekan Enter untuk melanjutkan...")
    input()
    while True:
        tampilkan_menu()
        try:
            pilihan = int(input("\nMasukkan pilihan menu (1-7): "))
        except ValueError:
            input("Masukkan angka antara 1-7! Tekan Enter untuk melanjutkan...")
            continue
        if pilihan == 1:
            tambah_siswa()
        elif pilihan == 2:
            tampilkan_semua_siswa()
        elif pilihan == 3:
            cari_siswa()
        elif pilihan == 4:
            hapus_siswa()
        elif pilihan == 5:
            ubah_nama_siswa()
        elif pilihan == 6:
            tampilkan_log()
        elif pilihan == 7:
            print("\nTerima kasih telah menggunakan aplikasi ini.")
            print("Data yang telah dimasukkan tidak akan hilang setelah program ditutup.")
            print("Sampai jumpa!")
            break
        else:
            input("Pilihan tidak valid. Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    muat_data()
    main()
