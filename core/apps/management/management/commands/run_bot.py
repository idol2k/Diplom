from django.core.management.base import BaseCommand
from core.apps.bot.main_bot import bot
import asyncio


class Command(BaseCommand):
    help = 'Запуск бота'

    def handle(self, *args, **options):
        async def run_bot():
            await bot.polling(non_stop=True)

        asyncio.get_event_loop().run_until_complete(run_bot())
