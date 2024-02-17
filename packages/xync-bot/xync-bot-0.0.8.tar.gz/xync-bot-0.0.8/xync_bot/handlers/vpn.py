from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from antifragility_schema.models import Client, Vpn
from python_wireguard import Key

vpn = Router()


@vpn.message(Command('get_vpn'))
async def get_vpn(msg: Message):
    my_id = msg.from_user.id
    cl = await Client.get(user_id=my_id).prefetch_related('vpn')
    if not cl.vpn:
        private, public = Key.key_pair()
        await Vpn.create(priv=private, pub=public, client=cl)
    await msg.answer(f"Take your file!")
    pass
