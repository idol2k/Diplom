from aiogram.utils import executor
from django.core.management import BaseCommand
from core.apps.bot.main_bot import dp


class Command(BaseCommand):
    help = 'Запуск бота'

    def handle(self, *args, **options):
        executor.start_polling(dp)

