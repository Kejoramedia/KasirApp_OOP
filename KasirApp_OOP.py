import datetime
import csv

class IdTransaksi:
    def __init__(self, nama_cs, counter):
        self.nama_cs = self.validasi_nama_cs(nama_cs)
        self.counter = self.validasi_counter(counter)

    def validasi_nama_cs(self, nama_cs):
        while not nama_cs.isalpha():
            print("Format input salah. Masukkan nama panggilan CS menggunakan huruf saja.")
            nama_cs = input('Nama Panggilan CS: ')
        return nama_cs

    def validasi_counter(self, counter):
        while not counter.isdigit() or len(counter) != 3:
            print("Input harus dalam bentuk angka 3 digit. Silakan coba lagi.")
            counter = input('No. Transaksi (3 Digit Angka): ')
        return int(counter)

    def buat_id_transaksi(self):
        tanggal = datetime.date.today().strftime("%y%m%d")
        return f"{self.nama_cs.upper()}{tanggal}-{self.counter:03d}"

class Belanja:
    def __init__(self):
        self.belanjaan = []
        self.total_belanja = 0
        self.nama_cs = None
        self.counter = None

    def hitung_total_harga(self, jumlah, harga):
        return jumlah * harga

    def format_harga(self, harga):
        return f"Rp.{harga:,.0f}"

    def input_angka(self, prompt):
        while True:
            angka = input(prompt)
            if angka.isdigit():
                return int(angka)
            print("Input harus berupa angka bulat. Silakan coba lagi.")

    def input_item(self, prompt):
        return input(prompt).upper()

    def tambah_belanja(self, item, jumlah, harga):
        self.belanjaan.append({"jumlah": jumlah, "item": item, "harga": harga})
        total_harga = self.hitung_total_harga(jumlah, harga)
        self.total_belanja += total_harga

    def transaksi_belanja(self):
        while True:
            item = self.input_item('Item (Ketik "0" untuk menyelesaikan transaksi): ')

            if item == "0":
                break

            harga = self.input_angka("Harga: Rp.")
            jumlah = self.input_angka("Jumlah: ")

            self.tambah_belanja(item, jumlah, harga)

        if self.belanjaan:
            print("\nStruk Belanja:")
            print("---------------------------")
            for belanja in self.belanjaan:
                jumlah = belanja["jumlah"]
                item = belanja["item"]
                harga = belanja["harga"]
                total_harga = self.hitung_total_harga(jumlah, harga)
                print(
                    f"{item.upper().ljust(15)}{self.format_harga(harga).ljust(10)}{str(jumlah).ljust(5)}{self.format_harga(total_harga)}")
            print("---------------------------")
            print(f"Total Belanja:\t{self.format_harga(self.total_belanja)}")

            uang_tunai = self.input_angka("\nUang Tunai: Rp.")
            kembali = uang_tunai - self.total_belanja

            print(f"Kembali: {self.format_harga(kembali)}")

            # Membuat ID Transaksi
            counter_str = str(self.counter)  # Mengubah kembali ke string sebelum validasi
            id_transaksi = IdTransaksi(self.nama_cs, counter_str)  # Gunakan variabel counter_str yang berisi string
            id_transaksi_str = id_transaksi.buat_id_transaksi()
            print(f"ID Transaksi: {id_transaksi_str}")

            struk_belanja = StrukBelanja()
            struk_belanja.simpan_struk_ke_csv(id_transaksi_str, self.belanjaan, self.total_belanja, uang_tunai, kembali)

        else:
            print("Belanjaan kosong. Transaksi dibatalkan.")

class StrukBelanja:
    def simpan_struk_ke_csv(self, nama_file, belanjaan, total_belanja, uang_tunai, kembali):
        with open(nama_file + ".csv", mode="w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["KEJORA SHOP"])
            writer.writerow([nama_file.split('.')[0]])
            writer.writerow([])
            writer.writerow(["ITEM", "JUMLAH", "HARGA", "TOTAL HARGA"])
            writer.writerow([])

            for belanja in belanjaan:
                jumlah = belanja["jumlah"]
                item = belanja["item"]
                harga = belanja["harga"]
                total_harga = Belanja().hitung_total_harga(jumlah, harga)
                writer.writerow([item.upper(), jumlah, Belanja().format_harga(harga), Belanja().format_harga(total_harga)])

            writer.writerow([])
            writer.writerow(["TOTAL BELANJA", "", "", Belanja().format_harga(total_belanja)])
            writer.writerow(["UANG TUNAI", "", "", Belanja().format_harga(uang_tunai)])
            writer.writerow(["KEMBALIAN", "", "", Belanja().format_harga(kembali)])
            writer.writerow([])
            writer.writerow(["TERIMAKASIH DAN SELAMAT BERBELANJA LAGI"])

if __name__ == '__main__':
    print("=== KEJORA  SHOP ===")
    nama_cs = input('Nama Panggilan CS: ')

    while not nama_cs.isalpha():
        print("Format input salah. Masukkan nama panggilan CS menggunakan huruf saja.")
        nama_cs = input('Nama Panggilan CS: ')

    counter = input('No. Transaksi (3 Digit Angka): ')

    while not counter.isdigit() or len(counter) != 3:
        print("Input harus dalam bentuk angka 3 digit. Silakan coba lagi.")
        counter = input('No. Transaksi (3 Digit Angka): ')

    struk_belanja = Belanja()
    struk_belanja.nama_cs = nama_cs
    struk_belanja.counter = int(counter)

    struk_belanja.transaksi_belanja()

    print("\nTerima kasih telah berbelanja di Kejora Shop!")
