import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from database import add_subject, get_subjects, delete_subject
from gpa_calculator import calculate_gpa
from report import generate_report
from config import API_KEY

# логи
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привет! Я бот для вычисления GPA. Вот что я могу:\n"
        "/start — Приветствие и инструкция.\n"
        "/add <предмет> <оценка> <кредиты> — Добавить новый предмет.\n"
        "/view — Просмотреть список предметов.\n"
        "/delete <ID> — Удалить предмет по ID.\n"
        "/gpa — Рассчитать GPA.\n"
        "/help — Показать список команд.\n"
        "/report — Сгенерировать отчет с графиками."
    )


# /help
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Вот список доступных команд:\n"
        "/start — Приветствие и инструкция.\n"
        "/add <предмет> <оценка> <кредиты> — Добавить новый предмет.\n"
        "/view — Просмотреть список предметов.\n"
        "/delete <ID> — Удалить предмет по ID.\n"
        "/gpa — Рассчитать GPA.\n"
        "/help — Показать список команд.\n"
        "/report — Сгенерировать отчет с графиками."
    )


# /add
async def add(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if len(context.args) != 3:
        await update.message.reply_text(
            "Для добавления предмета используйте команду /add <предмет> <оценка> <кредиты>.")
        return

    name = context.args[0]
    try:
        grade = float(context.args[1])
        credits = int(context.args[2])
    except ValueError:
        await update.message.reply_text("Оценка должна быть числом от 0 до 100, а кредиты целым числом.")
        return

    if not (0 <= grade <= 100):
        await update.message.reply_text("Оценка должна быть в пределах от 0 до 100.")
        return

    add_subject(user_id, name, grade, credits)
    await update.message.reply_text(f"Предмет {name} с оценкой {grade} и {credits} кредитами добавлен.")


# /view
async def view(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    subjects = get_subjects(user_id)
    if not subjects:
        await update.message.reply_text("У вас нет добавленных предметов.")
        return

    subjects_list = "\n".join(
        [f"ID {subject.id}: {subject.name} — Оценка: {subject.grade}, Кредиты: {subject.credits}" for subject in
         subjects])
    await update.message.reply_text(
        f"Ваши предметы:\n{subjects_list}\n\nДля удаления предмета используйте команду /delete <ID>")


# /delete
async def delete(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    args = context.args
    if len(args) < 1:
        await update.message.reply_text(
            "Нужно указать ID предмета для удаления. Используйте команду /view для получения списка предметов.")
        return

    try:
        subject_id = int(args[0])  # Получаем ID предмета
    except ValueError:
        await update.message.reply_text("ID предмета должен быть числом.")
        return

    subject_to_delete = get_subjects(user_id)
    subject_to_delete = next((s for s in subject_to_delete if s.id == subject_id), None)

    if subject_to_delete:
        delete_subject(subject_id)
        await update.message.reply_text(f"Предмет с ID {subject_id} удален.")
    else:
        await update.message.reply_text(f"Предмет с ID {subject_id} не найден.")


# /gpa
async def gpa(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    gpa = calculate_gpa(user_id)  # Теперь используем функцию из gpa_calculator.py
    await update.message.reply_text(f"Ваш GPA: {gpa:.2f}")


# /report
async def report(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    await update.message.reply_text("Генерация отчета... Это может занять несколько секунд.")
    await generate_report(user_id, update)


# обработка спама
async def unknown(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Извините, я не понял команду. Используйте /help для получения списка доступных команд.")


def main():
    # Настроим Application
    application = Application.builder().token(API_KEY).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("view", view))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("gpa", gpa))
    application.add_handler(CommandHandler("report", report))

    # Регистрируем обработчик для неизвестных команд
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    # Запуск бота
    print("Бот запущен...")
    application.run_polling()


if __name__ == '__main__':
    main()
