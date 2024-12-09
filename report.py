import matplotlib.pyplot as plt
from io import BytesIO
from database import get_subjects
from gpa_calculator import calculate_gpa


async def generate_report(user_id, update):
    subjects = get_subjects(user_id)
    if not subjects:
        await update.message.reply_text("У вас нет добавленных предметов для генерации отчета.")
        return

    gpa = calculate_gpa(user_id)

    subject_names = [subject.name for subject in subjects]
    subject_grades = [subject.grade for subject in subjects]
    subject_credits = [subject.credits for subject in subjects]

    # график оценок
    fig, ax = plt.subplots()
    ax.bar(subject_names, subject_grades, color='blue')
    ax.set_xlabel('Предметы')
    ax.set_ylabel('Оценки')
    ax.set_title(f"График оценок для GPA: {gpa:.2f}")
    plt.xticks(rotation=45, ha='right')

    # график в буфер
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # отправка графика в Tg
    await update.message.reply_photo(photo=buf, caption=f"Ваш GPA: {gpa:.2f}")

    # график по кредитам
    fig, ax = plt.subplots()
    ax.bar(subject_names, subject_credits, color='green')
    ax.set_xlabel('Предметы')
    ax.set_ylabel('Кредиты')
    ax.set_title("График кредитов по предметам")
    plt.xticks(rotation=45, ha='right')

    # график в буфер
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # отправка кредитов
    await update.message.reply_photo(photo=buf, caption="График кредитов по предметам.")
