from database import get_subjects

def convert_grade_to_gpa(grade):
    if grade >= 95:
        return 4.0  # A
    elif grade >= 90:
        return 3.67  # A-
    elif grade >= 85:
        return 3.33  # B+
    elif grade >= 80:
        return 3.0  # B
    elif grade >= 75:
        return 2.67  # B-
    elif grade >= 70:
        return 2.33  # C+
    elif grade >= 65:
        return 2.0  # C
    elif grade >= 60:
        return 1.67  # C-
    elif grade >= 55:
        return 1.33  # D+
    elif grade >= 50:
        return 1.0  # D
    elif grade >= 25:
        return 0.5  # FX
    else:
        return 0.0  # F


def calculate_gpa(user_id):
    """
    GPA = (И1*K1 + И2*K2 + ... + Ин*Кн) / (К1 + К2 + ... + Кн)
    """
    subjects = get_subjects(user_id)
    total_credits = 0
    weighted_sum = 0

    for subject in subjects:
        # GPA в числовой эквивалент
        gpa_score = convert_grade_to_gpa(subject.grade)
        weighted_sum += gpa_score * subject.credits
        total_credits += subject.credits

    if total_credits == 0:
        return 0  # 0, если нет предметов

    # результат до двух знаков
    return round(weighted_sum / total_credits, 2)
