from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
import time

ph = PasswordHasher()

akun = {}
percobaan_gagal = {}
waktu_unlock = {}

BATAS_PERCOBAAN = 3
DURASI_LOCK = 60

password_umum = {
    "12345678",
    "password",
    "password123",
    "qwerty123",
    "admin123"
}


# =========================
# CEK PASSWORD
# =========================
def cek_password(password):
    if len(password) < 8:
        return False

    if not any(karakter.isalpha() for karakter in password):
        return False

    if not any(karakter.isdigit() for karakter in password):
        return False

    if password.lower() in password_umum:
        return False

    return True


# =========================
# CEK USERNAME
# =========================
def cek_username(username):
    if len(username) < 3 or len(username) > 20:
        return False

    if not all(
        karakter.isalnum() or karakter == "_"
        for karakter in username
    ):
        return False

    return True


# =========================
# PROGRAM UTAMA
# =========================
while True:
    print("\n=== SECURE LOGIN SYSTEM ===")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    pilihan = input("Pilih: ").strip()

    # =========================
    # REGISTER
    # =========================
    if pilihan == "1":
        username_baru = input("Buat username: ").strip()
        password_baru = input("Buat password: ")

        if not cek_username(username_baru):
            print("Username tidak memenuhi persyaratan keamanan.")

        elif password_baru == "":
            print("Password tidak boleh kosong!")

        elif username_baru in akun:
            print("Username sudah digunakan!")

        elif not cek_password(password_baru):
            print("Password tidak memenuhi persyaratan keamanan.")

        else:
            password_hash = ph.hash(password_baru)

            akun[username_baru] = password_hash
            percobaan_gagal[username_baru] = 0

            print("Akun berhasil dibuat!")

    # =========================
    # LOGIN
    # =========================
    elif pilihan == "2":
        username = input("Username: ").strip()
        password = input("Password: ")

        if username not in akun:
            print("Username atau password salah!")
            continue

        if username not in percobaan_gagal:
            percobaan_gagal[username] = 0

        # =========================
        # CEK COOLDOWN
        # =========================
        if username in waktu_unlock:
            waktu_sekarang = time.time()

            if waktu_sekarang < waktu_unlock[username]:
                sisa_waktu = int(
                    waktu_unlock[username] - waktu_sekarang
                )

                print(
                    f"Akun terkunci. "
                    f"Coba lagi dalam {sisa_waktu} detik."
                )
                continue

            else:
                del waktu_unlock[username]
                percobaan_gagal[username] = 0

        # =========================
        # VERIFIKASI PASSWORD
        # =========================
        try:
            ph.verify(akun[username], password)

            percobaan_gagal[username] = 0

            print("Login berhasil!")

        except VerifyMismatchError:
            percobaan_gagal[username] += 1

            print("Username atau password salah!")
            print(
                f"Percobaan gagal: "
                f"{percobaan_gagal[username]}/{BATAS_PERCOBAAN}"
            )

            if percobaan_gagal[username] >= BATAS_PERCOBAAN:
                waktu_unlock[username] = (
                    time.time() + DURASI_LOCK
                )

                print("Terlalu banyak percobaan gagal!")
                print("Akun dikunci selama 60 detik.")

        except VerificationError:
            print("Terjadi kesalahan saat verifikasi!")

    # =========================
    # EXIT
    # =========================
    elif pilihan == "3":
        print("Program selesai.")
        break

    else:
        print("Pilihan tidak valid!")