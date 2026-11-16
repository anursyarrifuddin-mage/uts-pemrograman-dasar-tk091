"""Modul validasi data mahasiswa dan pencegahan duplikasi."""


class StudentDataError(ValueError):
    """Exception khusus ketika data mahasiswa tidak memenuhi aturan."""


def validate_text(value, field_name):
    """Memastikan input teks tidak kosong setelah spasi tepi dihapus."""
    if not isinstance(value, str) or not value.strip():
        raise StudentDataError(f"{field_name} wajib diisi dan tidak boleh kosong.")
    return value.strip()


def validate_number(value, field_name):
    """Memastikan nilai atau kehadiran berupa bilangan bulat 0-100 (True ditolak)."""
    if type(value) is not int:
        raise StudentDataError(f"{field_name} harus berupa bilangan bulat.")
    if not 0 <= value <= 100:
        raise StudentDataError(f"{field_name} harus berada pada rentang 0 sampai 100.")
    return value


def validate_student(student):
    """Memvalidasi satu dictionary data mahasiswa dan mengembalikan data yang bersih."""
    if not isinstance(student, dict):
        raise StudentDataError("Data mahasiswa harus berupa dictionary.")

    nim = validate_text(student.get("nim"), "NIM")
    name = validate_text(student.get("name"), "Nama")
    program = validate_text(student.get("program"), "Program Studi")
    score = validate_number(student.get("score"), "Nilai")
    attendance = validate_number(student.get("attendance"), "Kehadiran")

    return {
        "nim": nim,
        "name": name,
        "program": program,
        "score": score,
        "attendance": attendance,
    }


def deduplicate_students(records):
    """Menghapus data mahasiswa dengan NIM duplikat (menyimpan kemunculan pertama)."""
    seen_nims = set()
    unique_records = []
    removed_count = 0

    for item in records:
        nim = item["nim"]
        if nim in seen_nims:
            removed_count += 1
            continue
        seen_nims.add(nim)
        unique_records.append(item)

    return unique_records, removed_count
