from typing import Final, Dict, List
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime

# Replace with your bot's token
TOKEN: Final = '8286582793:AAEmx-4VQnjJ38o3j0CtRJKQ-pUyiIHDChg'  
BOT_USERNAME: Final = '@Genricaibot'

# Dictionary to store tasks for each user
tasks: Dict[int, List[Dict]] = {}

# Function to parse and convert priority level
def parse_priority(priority: str) -> str:
    priority_levels = ["high", "medium", "low"]
    return priority.lower() if priority.lower() in priority_levels else "low"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am TaskGenie. Use /help to see what I can do.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Here are the commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/add_task <task> - Add a new task\n"
        "/view_tasks - View all your tasks\n"
        "/remove_task <task number> - Remove a task by its number\n"
        "/set_priority <task number> <priority> - Set priority for a task (high, medium, low)\n"
        "/set_deadline <task number> <YYYY-MM-DD> - Set a deadline for a task\n"
        "/add_category <task number> <category> - Add a category to a task\n"
        "/mark_completed <task number> - Mark a task as completed\n"
        "/view_completed - View completed tasks\n"
        "/find_tasks <category/priority> - Filter tasks by category or priority\n"
    )
    await update.message.reply_text(help_text)

async def add_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args:
        task_description = ' '.join(context.args)
        new_task = {
            "description": task_description,
            "priority": "low",
            "deadline": None,
            "category": "general",
            "completed": False
        }
        if user_id not in tasks:
            tasks[user_id] = []
        tasks[user_id].append(new_task)
        await update.message.reply_text(f'Task added: "{task_description}"')
    else:
        await update.message.reply_text('Please specify a task to add. Usage: /add_task <task>')

async def view_tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in tasks and tasks[user_id]:
        task_list = '\n'.join(
            f'{i + 1}. {task["description"]} [Priority: {task["priority"]}, Deadline: {task["deadline"]}, Category: {task["category"]}]'
            for i, task in enumerate(tasks[user_id]) if not task["completed"]
        )
        await update.message.reply_text(f'Your tasks:\n{task_list}')
    else:
        await update.message.reply_text('You have no tasks.')

async def remove_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args and context.args[0].isdigit():
        task_number = int(context.args[0]) - 1
        if user_id in tasks and 0 <= task_number < len(tasks[user_id]):
            removed_task = tasks[user_id].pop(task_number)
            await update.message.reply_text(f'Task removed: "{removed_task["description"]}"')
        else:
            await update.message.reply_text('Invalid task number.')
    else:
        await update.message.reply_text('Please specify a task number to remove. Usage: /remove_task <task number>')

async def set_priority_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args and len(context.args) == 2 and context.args[0].isdigit():
        task_number = int(context.args[0]) - 1
        priority = parse_priority(context.args[1])
        if user_id in tasks and 0 <= task_number < len(tasks[user_id]):
            tasks[user_id][task_number]["priority"] = priority
            await update.message.reply_text(f'Set priority to "{priority}" for task: "{tasks[user_id][task_number]["description"]}"')
        else:
            await update.message.reply_text('Invalid task number.')
    else:
        await update.message.reply_text('Please specify a task number and priority. Usage: /set_priority <task number> <priority>')

async def set_deadline_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args and len(context.args) == 2 and context.args[0].isdigit():
        task_number = int(context.args[0]) - 1
        try:
            deadline = datetime.strptime(context.args[1], "%Y-%m-%d").date()
            if user_id in tasks and 0 <= task_number < len(tasks[user_id]):
                tasks[user_id][task_number]["deadline"] = deadline
                await update.message.reply_text(f'Set deadline to "{deadline}" for task: "{tasks[user_id][task_number]["description"]}"')
            else:
                await update.message.reply_text('Invalid task number.')
        except ValueError:
            await update.message.reply_text('Invalid date format. Please use YYYY-MM-DD.')
    else:
        await update.message.reply_text('Please specify a task number and deadline. Usage: /set_deadline <task number> <YYYY-MM-DD>')

async def add_category_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args and len(context.args) >= 2 and context.args[0].isdigit():
        task_number = int(context.args[0]) - 1
        category = ' '.join(context.args[1:])
        if user_id in tasks and 0 <= task_number < len(tasks[user_id]):
            tasks[user_id][task_number]["category"] = category
            await update.message.reply_text(f'Added category "{category}" to task: "{tasks[user_id][task_number]["description"]}"')
        else:
            await update.message.reply_text('Invalid task number.')
    else:
        await update.message.reply_text('Please specify a task number and category. Usage: /add_category <task number> <category>')

async def mark_completed_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args and context.args[0].isdigit():
        task_number = int(context.args[0]) - 1
        if user_id in tasks and 0 <= task_number < len(tasks[user_id]):
            tasks[user_id][task_number]["completed"] = True
            await update.message.reply_text(f'Marked as completed: "{tasks[user_id][task_number]["description"]}"')
        else:
            await update.message.reply_text('Invalid task number.')
    else:
        await update.message.reply_text('Please specify a task number. Usage: /mark_completed <task number>')

async def view_completed_tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in tasks and tasks[user_id]:
        completed_task_list = '\n'.join(
            f'{i + 1}. {task["description"]} [Completed]'
            for i, task in enumerate(tasks[user_id]) if task["completed"]
        )
        await update.message.reply_text(f'Your completed tasks:\n{completed_task_list}')
    else:
        await update.message.reply_text('You have no completed tasks.')

async def find_tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args:
        filter_criteria = context.args[0].lower()
        filtered_tasks = [
            f'{i + 1}. {task["description"]} [Priority: {task["priority"]}, Deadline: {task["deadline"]}, Category: {task["category"]}]'
            for i, task in enumerate(tasks[user_id])
            if filter_criteria in (task["priority"].lower(), task["category"].lower())
        ]
        if filtered_tasks:
            await update.message.reply_text(f'Tasks filtered by "{filter_criteria}":\n' + '\n'.join(filtered_tasks))
        else:
            await update.message.reply_text(f'No tasks found with "{filter_criteria}".')
    else:
        await update.message.reply_text('Please specify a category or priority to filter by. Usage: /find_tasks <category/priority>')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handling non-command text
    await update.message.reply_text("I'm sorry, I didn't understand that command. Type /help to see the available commands.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('add_task', add_task_command))
    app.add_handler(CommandHandler('view_tasks', view_tasks_command))
    app.add_handler(CommandHandler('remove_task', remove_task_command))
    app.add_handler(CommandHandler('set_priority', set_priority_command))
    app.add_handler(CommandHandler('set_deadline', set_deadline_command))
    app.add_handler(CommandHandler('add_category', add_category_command))
    app.add_handler(CommandHandler('mark_completed', mark_completed_command))
    app.add_handler(CommandHandler('view_completed', view_completed_tasks_command))
    app.add_handler(CommandHandler('find_tasks', find_tasks_command))

    # Messages (to handle non-command text messages)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error Handling
    app.add_error_handler(error_handler)

    print('Polling...')
    app.run_polling(poll_interval=3)