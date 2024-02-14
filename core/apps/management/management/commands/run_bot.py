from django.core.management.base import BaseCommand
from core.apps.bot.main_bot import bot
import asyncio

class Command(BaseCommand):
    help = 'Запуск бота'

    def handle(self, *args, **options):
        asyncio.run(bot.polling(non_stop=True))