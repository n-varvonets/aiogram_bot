from aiogram.utils import executor
from create_bot import dp

async def on_startup(_):
    print('Бот вышел в онлайн')


from handlers import client, admin, others
# и теперь перед запуском pooling executer-a вьізьіваем наши уже зареганнье хендлерьі из импортированньіх модулей,
# тем самьім разделив догику вьіполнения попакетно
client.register_handlers_client(dp)  # передаем в нашу функцию dispatcher, т.к. он в ней используется
admin.register_handlres_admin(dp)
others.register_handlers_other(dp)  # т.к. єто пустой хендлер и он реагирует на все действия, то должен біть последним

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
