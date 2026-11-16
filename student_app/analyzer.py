"""Modul analisis data mahasiswa: status, filter, ranking, dan statistik."""

from operator import itemgetter


def determine_status(score, attendance):
    """Menentukan status kelulusan berdasarkan prioritas kehadiran dan nilai."""
    if attendance < 75:
        return "Peringatan Kehadiran"
    if score >= 90 and attendance >= 90:
        return "Lulus dengan Pujian"
    if score >= 80:
        return "Lulus"
    if score >= 60:
        return "Remedial"
    return "Tidak Lulus"


def get_unique_programs(students):
    """Mengambil daftar program studi unik menggunakan set comprehension."""
    return {student["program"] for student in students}


def filter_by_status(students, target_status):
    """Memfilter mahasiswa yang memiliki status tertentu menggunakan list comprehension."""
    return [
        {**student, "status": determine_status(student["score"], student["attendance"])}
        for student in students
        if determine_status(student["score"], student["attendance"]).lower() == target_status.strip().lower()
    ]


def find_by_nim(students, target_nim):
    """Mencari satu mahasiswa berdasarkan NIM menggunakan dictionary index."""
    index_by_nim = {student["nim"]: student for student in students}
    return index_by_nim.get(target_nim.strip())


def create_ranking(students):
    """Membuat daftar ranking mahasiswa berdasarkan nilai tertinggi tanpa mengubah data asli."""
    sorted_students = sorted(students, key=itemgetter("score", "attendance"), reverse=True)
    ranked = []
    for rank, student in enumerate(sorted_students, start=1):
        ranked.append(
            {
                "rank": rank,
                "nim": student["nim"],
                "name": student["name"],
                "program": student["program"],
                "score": student["score"],
                "attendance": student["attendance"],
                "status": determine_status(student["score"], student["attendance"]),
            }
        )
    return ranked


def group_by_status(students):
    """Mengelompokkan jumlah mahasiswa berdasarkan status kelulusan."""
    summary = {}
    for student in students:
        status = determine_status(student["score"], student["attendance"])
        summary[status] = summary.get(status, 0) + 1
    return summary


def calculate_statistics(students):
    """Menghitung statistik dasar nilai mahasiswa (aman untuk list kosong)."""
    if not students:
        return {
            "total_students": 0,
            "average_score": None,
            "highest_score": None,
            "lowest_score": None,
            "passed_count": 0,
            "status_counts": {},
        }

    total_score = sum(student["score"] for student in students)
    highest = max(student["score"] for student in students)
    lowest = min(student["score"] for student in students)
    passed_count = sum(
        1
        for student in students
        if determine_status(student["score"], student["attendance"]) in ("Lulus", "Lulus dengan Pujian")
    )

    return {
        "total_students": len(students),
        "average_score": round(total_score / len(students), 2),
        "highest_score": highest,
        "lowest_score": lowest,
        "passed_count": passed_count,
        "status_counts": group_by_status(students),
    }
