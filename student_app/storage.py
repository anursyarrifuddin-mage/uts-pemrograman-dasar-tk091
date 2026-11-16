"""Modul penyimpanan dan ekspor data mahasiswa ke JSON dan CSV."""

import csv
import json
import logging
from pathlib import Path

from .validator import StudentDataError, deduplicate_students, validate_student

logger = logging.getLogger("student_app.storage")


def load_students_json(file_path):
    """Membaca data mahasiswa dari file JSON dengan validasi dan exception handling."""
    path = Path(file_path)
    if not path.exists():
        logger.warning("File input %s tidak ditemukan, memulai dengan data kosong.", path)
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
    except json.JSONDecodeError as error:
        logger.error("Format JSON pada %s rusak: %s", path, error)
        return []
    except OSError as error:
        logger.error("Gagal membaca file %s: %s", path, error)
        return []

    if not isinstance(raw_data, list):
        logger.error("Struktur JSON harus berupa list of objects.")
        return []

    valid_students = []
    for index, item in enumerate(raw_data, start=1):
        try:
            valid_students.append(validate_student(item))
        except StudentDataError as error:
            logger.warning("Baris ke-%d dilewati karena tidak valid: %s", index, error)

    cleaned, removed = deduplicate_students(valid_students)
    if removed > 0:
        logger.warning("Ditemukan dan dihapus %d data dengan NIM duplikat.", removed)

    logger.info("Berhasil memuat %d data mahasiswa dari %s.", len(cleaned), path)
    return cleaned


def save_students_json(students, file_path):
    """Menyimpan daftar mahasiswa ke file JSON."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=2, ensure_ascii=False)
    logger.info("Data mahasiswa (%d record) disimpan ke %s.", len(students), path)


def export_report_csv(ranked_students, file_path):
    """Mengekspor hasil ranking dan status mahasiswa ke file CSV."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["rank", "nim", "name", "program", "score", "attendance", "status"]

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ranked_students)

    logger.info("Laporan CSV berhasil diekspor ke %s.", path)


def export_analysis_json(statistics, ranked_students, unique_programs, file_path):
    """Menyimpan hasil ringkasan analisis dan ranking ke file JSON."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "statistics": statistics,
        "unique_programs": sorted(unique_programs),
        "ranked_students": ranked_students,
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)
    logger.info("Hasil analisis JSON berhasil disimpan ke %s.", path)
