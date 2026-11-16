# Aplikasi CLI Pengolahan Data & Nilai Mahasiswa (UTS Pemrograman Dasar TK091).

import logging
from pathlib import Path

from student_app import (
    StudentDataError,
    calculate_statistics,
    create_ranking,
    determine_status,
    export_analysis_json,
    export_report_csv,
    filter_by_status,
    find_by_nim,
    get_unique_programs,
    load_students_json,
    save_students_json,
    validate_number,
    validate_text,
)

BASE_DIR = Path(__file__).resolve().parent
INPUT_JSON = BASE_DIR / "data" / "students_input.json"
OUTPUT_CSV = BASE_DIR / "output" / "laporan_mahasiswa.csv"
OUTPUT_JSON = BASE_DIR / "output" / "hasil_analisis.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger("student_cli")


def read_text_input(prompt, field_name):
    """Membaca input teks dari pengguna sampai tidak kosong."""
    while True:
        try:
            raw = input(prompt)
            return validate_text(raw, field_name)
        except StudentDataError as error:
            logger.warning("Input %s ditolak: %s", field_name, error)
            print(f"Input salah: {error}")


def read_int_input(prompt, field_name):
    """Membaca input bilangan bulat 0-100 dari pengguna dengan pesan error ramah."""
    while True:
        raw = input(prompt).strip()
        try:
            number = int(raw)
            return validate_number(number, field_name)
        except ValueError as error:
            if "invalid literal" in str(error):
                msg = f"{field_name} harus berupa bilangan bulat."
            else:
                msg = str(error)
            logger.warning("Input %s ditolak: %s", field_name, msg)
            print(f"Input salah: {msg}")


def show_all_students(students):
    """Menampilkan daftar seluruh mahasiswa beserta statusnya."""
    if not students:
        print("Belum ada data mahasiswa.")
        return

    print("\n=== DAFTAR MAHASISWA ===")
    for number, student in enumerate(students, start=1):
        status = determine_status(student["score"], student["attendance"])
        print(
            f"{number}. {student['nim']} | {student['name']} | "
            f"{student['program']} | Nilai: {student['score']} | "
            f"Hadir: {student['attendance']}% | {status}"
        )


def add_student_flow(students):
    """Menambahkan mahasiswa baru dengan validasi dan penolakan NIM duplikat."""
    print("\n=== TAMBAH MAHASISWA ===")
    nim = read_text_input("NIM: ", "NIM")
    if find_by_nim(students, nim) is not None:
        logger.warning("Penambahan ditolak: NIM %s sudah terdaftar.", nim)
        print(f"Gagal: NIM {nim} sudah terdaftar (duplikat tidak diperbolehkan).")
        return students

    name = read_text_input("Nama: ", "Nama")
    program = read_text_input("Program Studi: ", "Program Studi")
    score = read_int_input("Nilai (0-100): ", "Nilai")
    attendance = read_int_input("Kehadiran % (0-100): ", "Kehadiran")

    new_student = {
        "nim": nim,
        "name": name,
        "program": program,
        "score": score,
        "attendance": attendance,
    }
    updated = [*students, new_student]
    save_students_json(updated, INPUT_JSON)
    print(f"Data {name} ({nim}) berhasil ditambahkan.")
    return updated


def search_student_flow(students):
    """Mencari mahasiswa berdasarkan NIM."""
    if not students:
        print("Belum ada data mahasiswa.")
        return

    target_nim = input("Masukkan NIM yang dicari: ").strip()
    if not target_nim:
        print("Input salah: NIM tidak boleh kosong.")
        return

    found = find_by_nim(students, target_nim)
    if found is None:
        print("Mahasiswa tidak ditemukan.")
        return

    status = determine_status(found["score"], found["attendance"])
    print("\n=== HASIL PENCARIAN ===")
    print(f"NIM       : {found['nim']}")
    print(f"Nama      : {found['name']}")
    print(f"Prodi     : {found['program']}")
    print(f"Nilai     : {found['score']}")
    print(f"Kehadiran : {found['attendance']}%")
    print(f"Status    : {status}")


def filter_and_programs_flow(students):
    """Menampilkan daftar program studi unik dan filter berdasarkan status."""
    if not students:
        print("Belum ada data mahasiswa.")
        return

    programs = sorted(get_unique_programs(students))
    print("\n=== PROGRAM STUDI UNIK ===")
    for prog in programs:
        print(f"- {prog}")
    print(f"Total prodi unik: {len(programs)}")

    print("\nPilihan status: Peringatan Kehadiran, Lulus dengan Pujian, Lulus, Remedial, Tidak Lulus")
    target = input("Filter status: ").strip()
    if not target:
        print("Filter dibatalkan.")
        return

    filtered = filter_by_status(students, target)
    if not filtered:
        print(f"Tidak ada mahasiswa dengan status '{target}'.")
        return

    print(f"\n=== MAHASISWA STATUS: {target.upper()} ===")
    for number, student in enumerate(filtered, start=1):
        print(f"{number}. {student['nim']} | {student['name']} | Nilai: {student['score']} | Hadir: {student['attendance']}%")


def show_ranking_and_stats(students):
    """Menampilkan ranking mahasiswa dan ringkasan statistik."""
    if not students:
        print("Belum ada data mahasiswa untuk dihitung.")
        return

    ranked = create_ranking(students)
    stats = calculate_statistics(students)

    print("\n=== RANKING MAHASISWA ===")
    for item in ranked:
        print(
            f"Rank {item['rank']}: {item['name']} ({item['nim']}) - "
            f"Nilai: {item['score']} | Hadir: {item['attendance']}% | {item['status']}"
        )

    print("\n=== STATISTIK NILAI ===")
    print(f"Jumlah mahasiswa : {stats['total_students']}")
    print(f"Rata-rata nilai  : {stats['average_score']:.2f}")
    print(f"Nilai tertinggi  : {stats['highest_score']}")
    print(f"Nilai terendah   : {stats['lowest_score']}")
    print(f"Jumlah lulus     : {stats['passed_count']}")
    print("Rekap per status :")
    for status_name, count in stats["status_counts"].items():
        print(f"  - {status_name}: {count}")


def export_reports_flow(students):
    """Mengekspor laporan CSV dan hasil analisis JSON."""
    if not students:
        print("Data kosong, tidak ada laporan yang diekspor.")
        return

    ranked = create_ranking(students)
    stats = calculate_statistics(students)
    programs = get_unique_programs(students)

    export_report_csv(ranked, OUTPUT_CSV)
    export_analysis_json(stats, ranked, programs, OUTPUT_JSON)
    print(f"Laporan berhasil diekspor ke:\n- {OUTPUT_CSV}\n- {OUTPUT_JSON}")


def print_menu():
    """Menampilkan menu utama aplikasi CLI."""
    print("\n========================================")
    print("   STUDENT DATA & GRADE PROCESSOR CLI   ")
    print("========================================")
    print("1. Tampilkan Semua Mahasiswa")
    print("2. Tambah Mahasiswa Baru")
    print("3. Cari Mahasiswa (NIM)")
    print("4. Prodi Unik & Filter Status")
    print("5. Ranking & Statistik Nilai")
    print("6. Ekspor Laporan (CSV & JSON)")
    print("7. Keluar")
    print("========================================")


def main():
    """Titik masuk utama aplikasi CLI."""
    students = load_students_json(INPUT_JSON)

    while True:
        print_menu()
        try:
            choice = input("Pilih menu (1-7): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nProgram dihentikan oleh pengguna.")
            break

        if choice == "1":
            show_all_students(students)
        elif choice == "2":
            students = add_student_flow(students)
        elif choice == "3":
            search_student_flow(students)
        elif choice == "4":
            filter_and_programs_flow(students)
        elif choice == "5":
            show_ranking_and_stats(students)
        elif choice == "6":
            export_reports_flow(students)
        elif choice == "7":
            logger.info("Program selesai.")
            print("Terima kasih. Program selesai.")
            break
        else:
            logger.warning("Pilihan menu tidak valid: %s", choice)
            print("Pilihan tidak tersedia. Silakan masukkan angka 1 sampai 7.")


if __name__ == "__main__":
    main()
