import csv
import datetime

class Transaction:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, item, harga, jumlah):
        self.items.append({"item": item, "harga": harga, "jumlah": jumlah})
        self.total += self.hitung_total(harga, jumlah)

    def hitung_total(self, harga, jumlah):
        return harga * jumlah

    def format_harga(self, harga):
        return f"Rp.{harga:,.0f}"

    def input_angka(self, prompt):
        while True:
            try:
                angka = int(input(prompt))
                return angka
            except ValueError:
                print("Input harus berupa angka bulat. Silakan coba lagi.")

    def input_item(self, prompt):
        return input(prompt).upper()

    def input_cs_name(self, prompt):
        while True:
            nama_cs = input(prompt)
            if nama_cs.isalpha():
                return nama_cs.upper()
            else:
                print("Format input salah. Masukkan nama panggilan CS menggunakan huruf saja.")

    def input_counter(self, prompt):
        while True:
            counter = input(prompt)
            if counter.isdigit() and len(counter) == 3:
                return int(counter)
            else:
                print("Input harus dalam bentuk angka 3 digit. Silakan coba lagi.")

    def buat_id_transaksi(self, nama_cs, counter):
        tanggal = datetime.date.today().strftime("%y%m%d")
        return f"{nama_cs}{tanggal}-{counter:03d}"

    def transaksi_belanja(self):
        belanjaan = []

        total_belanja = 0
        print("Kejora Shop")

        # Input nama panggilan CS
        nama_cs = self.input_cs_name("Nama panggilan CS: ")

        # Input counter untuk ID transaksi
        counter = self.input_counter("No. Transaksi: ")

        while True:
            item = self.input_item('Item (Ketik "0" untuk menyelesaikan transaksi): ')

            if item == "0":
                break

            harga = self.input_angka("Harga: Rp.")
            jumlah = self.input_angka("Jumlah: ")

            belanjaan.append({"jumlah": jumlah, "item": item, "harga": harga})

            total_harga = self.hitung_total(harga, jumlah)
            total_belanja += total_harga

        if belanjaan:
            print("\nStruk Belanja:")
            print("---------------------------")
            for belanja in belanjaan:
                jumlah = belanja["jumlah"]
                item = belanja["item"]
                harga = belanja["harga"]
                total_harga = self.hitung_total(harga, jumlah)
                print(
                    f"{item.upper().ljust(15)}{self.format_harga(harga).ljust(10)}{str(jumlah).ljust(5)}{self.format_harga(total_harga)}")
            print("---------------------------")
            print(f"Total Belanja:\t{self.format_harga(total_belanja)}")

            uang_tunai = self.input_angka("\nUang Tunai: Rp.")
            kembali = uang_tunai - total_belanja

            print(f"Kembali: {self.format_harga(kembali)}")

            # Membuat ID Transaksi
            id_transaksi = self.buat_id_transaksi(nama_cs, counter)

            receipt_writer = ReceiptWriter()
            receipt_writer.save_receipt_to_csv(id_transaksi, belanjaan, total_belanja, uang_tunai, kembali)

            print("\nStruk telah disimpan.\n")

        else:
            print("Belanjaan kosong. Transaksi dibatalkan.")


class ReceiptWriter:
    def save_receipt_to_csv(self, id_transaksi, belanjaan, total_belanja, uang_tunai, kembali):
        nama_file = f"{id_transaksi}.csv"

        with open(nama_file, mode="w", newline="") as file:
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
                total_harga = harga * jumlah
                writer.writerow([item.upper(), jumlah, f"Rp.{harga:,.0f}", f"Rp.{total_harga:,.0f}"])

            writer.writerow([])
            writer.writerow(["TOTAL BELANJA", "", "", f"Rp.{total_belanja:,.0f}"])
            writer.writerow(["UANG TUNAI", "", "", f"Rp.{uang_tunai:,.0f}"])
            writer.writerow(["KEMBALIAN", "", "", f"Rp.{kembali:,.0f}"])
            writer.writerow([])
            writer.writerow(["TERIMAKASIH DAN SELAMAT BERBELANJA LAGI"])


if __name__ == '__main__':
    transaksi = Transaction()
    transaksi.transaksi_belanja()
