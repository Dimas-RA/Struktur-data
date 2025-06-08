import heapq
import itertools

#==== Struktur Graph ====
class MultiModeGraph:
    def __init__(self):
        self.vertices = set()
        self.edges = {}

    def tambah_kota(self, nama):
        self.vertices.add(nama)
        self.edges[nama] = []

    def tambah_jalan(self, dari, ke, waktu_mobil, waktu_motor, waktu_jalan,
                     jarak):
        bobot = {
            "mobil": {"waktu": waktu_mobil, "jarak": jarak},
            "motor": {"waktu": waktu_motor, "jarak": jarak},
            "jalan kaki": {"waktu": waktu_jalan, "jarak": jarak}
        }
        self.edges[dari].append((ke, bobot))
        self.edges[ke].append((dari, bobot))

    def dijkstra(self, awal, tujuan, moda):
        antrian = [(0, 0, awal, [])]  # Urutan input(total_waktu, total_jarak, kota, jalur)
        sudah_dikunjungi = set()

        while antrian:
            waktu, jarak, kota, jalur = heapq.heappop(antrian)
            if kota in sudah_dikunjungi:
                continue
            sudah_dikunjungi.add(kota)
            jalur = jalur + [kota]

            if kota == tujuan:
                return waktu, jarak, jalur

            for tetangga, bobot in self.edges[kota]:
                if tetangga not in sudah_dikunjungi:
                    waktu_tambah = bobot[moda]["waktu"]
                    jarak_tambah = bobot[moda]["jarak"]
                    heapq.heappush(antrian, (waktu + waktu_tambah, jarak + jarak_tambah, tetangga, jalur))

        return float('inf'), float('inf'), []

    def tsp_brute_force(self, moda):
        kota_list = list(self.vertices)
        min_waktu = float('inf')
        min_jarak = float('inf')
        rute_terbaik = None

        for urutan in itertools.permutations(kota_list):
            total_waktu = 0
            total_jarak = 0
            valid = True
            for i in range(len(urutan) - 1):
                tetangga_dict = {n: w for n, w in self.edges[urutan[i]]}
                if urutan[i + 1] in tetangga_dict:
                    total_waktu += tetangga_dict[urutan[i + 1]][moda]["waktu"]
                    total_jarak += tetangga_dict[urutan[i + 1]][moda]["jarak"]
                else:
                    valid = False
                    break
            if valid and total_waktu < min_waktu:
                min_waktu = total_waktu
                min_jarak = total_jarak
                rute_terbaik = urutan

        return min_waktu, min_jarak, rute_terbaik

# ===== Graf Kota & Jarak =====
def graf_kota():
    kota_list = [
        "Kuala Lumpur", "Shah Alam", "Petaling Jaya", "Subang Jaya", "Kajang",
        "Putrajaya", "Cyberjaya", "Nilai", "Seremban", "Bangi"
    ]
    graf = MultiModeGraph()
    for kota in kota_list:
        graf.tambah_kota(kota)

    # Format: (dari, ke, waktu_mobil, waktu_motor, waktu_jalan, jarak)
    jalur = [
        ("Kuala Lumpur", "Petaling Jaya", 0.3, 0.35, 3.0, 14),
        ("Kuala Lumpur", "Shah Alam", 0.5, 0.6, 5.0, 25),
        ("Kuala Lumpur", "Subang Jaya", 0.45, 0.5, 4.5, 20),
        ("Kuala Lumpur", "Kajang", 0.6, 0.7, 6.0, 30),
        ("Kuala Lumpur", "Putrajaya", 0.75, 0.85, 7.5, 37),
        ("Kuala Lumpur", "Cyberjaya", 0.8, 0.9, 8.0, 40),
        ("Kuala Lumpur", "Nilai", 1.0, 1.1, 10.0, 50),
        ("Kuala Lumpur", "Seremban", 1.2, 1.3, 12.0, 60),
        ("Kuala Lumpur", "Bangi", 0.5, 0.6, 5.0, 25),
        ("Petaling Jaya", "Shah Alam", 0.4, 0.45, 4.0, 20),
        ("Petaling Jaya", "Subang Jaya", 0.3, 0.35, 3.0, 15),
        ("Petaling Jaya", "Kajang", 0.5, 0.6, 5.0, 25),
        ("Petaling Jaya", "Putrajaya", 0.7, 0.8, 7.0, 35),
        ("Petaling Jaya", "Cyberjaya", 0.75, 0.85, 7.5, 37),
        ("Petaling Jaya", "Nilai", 0.9, 1.0, 9.0, 45),
        ("Petaling Jaya", "Seremban", 1.1, 1.2, 11.0, 55),
        ("Petaling Jaya", "Bangi", 0.6, 0.7, 6.0, 30),
        ("Shah Alam", "Subang Jaya", 0.25, 0.3, 2.5, 12),
        ("Shah Alam", "Kajang", 0.6, 0.7, 6.0, 30),
        ("Shah Alam", "Putrajaya", 0.7, 0.8, 7.0, 35),
        ("Shah Alam", "Cyberjaya", 0.75, 0.85, 7.5, 37),
        ("Shah Alam", "Nilai", 0.9, 1.0, 9.0, 45),
        ("Shah Alam", "Seremban", 1.1, 1.2, 11.0, 55),
        ("Shah Alam", "Bangi", 0.6, 0.7, 6.0, 30),
        ("Subang Jaya", "Kajang", 0.5, 0.6, 5.0, 25),
        ("Putrajaya", "Subang Jaya", 0.6, 0.7, 6.0, 30),
        ("Subang Jaya", "Cyberjaya", 0.65, 0.75, 6.5, 32),
        ("Subang Jaya", "Nilai", 0.8, 0.9, 8.0, 40),
        ("Subang Jaya", "Seremban", 1.0, 1.1, 10.0, 50),
        ("Kajang", "Putrajaya", 0.4, 0.5, 4.0, 20)
    ]

    for data in jalur:
        graf.tambah_jalan(*data)

    return graf, kota_list

# ===== Program Utama =====
def main():
    graf, kota_list = graf_kota()

    print("==== RUTE TERCEPAT MENGGUNAKAN METODE DIJKSTRA ====")
    print("Daftar Kota Yang Tersedia:", ', '.join(kota_list))

    moda = input("Silakan pilih moda transportasi (mobil, motor, atau jalan kaki): ").strip().lower()
    asal = input("Tulis nama kota asal anda: ").strip().title()
    tujuan = input("Tulis nama kota tujuan anda: ").strip().title()

    if asal not in kota_list or tujuan not in kota_list:
        print("Nama kota yang dimasukkan tidak tersedia.")
        return

    if moda not in ["mobil", "motor", "jalan kaki"]:
        print("Jenis transportasi yang dipilih tidak tersedia.")
        return

    waktu, jarak, jalur = graf.dijkstra(asal, tujuan, moda)
    if jalur:
        print(f"\nRute tercepat dari {asal} ke {tujuan} menggunakan {moda}:")
        print(" -> ".join(jalur))
        print(f"Waktu tempuh: {waktu:.2f} jam")
        print(f"Jarak tempuh: {jarak:.2f} km\n")
    else:
        print("Tidak ada rute yang valid.\n")

    print("=== RUTE TSP TERBAIK (Mengunjungi semua kota) ===")
    waktu_tsp, jarak_tsp, rute_tsp = graf.tsp_brute_force(moda)
    if rute_tsp:
        print(f"Rute TSP: {' -> '.join(rute_tsp)}")
        print(f"Total waktu perjalanan: {waktu_tsp:.2f} jam")
        print(f"Total jarak perjalanan: {jarak_tsp:.2f} km\n")
    else:
        print("Tidak ada rute TSP yang valid ditemukan.\n")

if __name__ == "__main__":
    main()
