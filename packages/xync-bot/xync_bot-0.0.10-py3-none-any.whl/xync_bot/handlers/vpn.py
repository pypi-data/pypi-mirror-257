from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile, MessageEntity
from antifragility_schema.models import Client, Vpn
from python_wireguard import Key
from os import getenv as env
from dotenv import load_dotenv

load_dotenv()
vpn = Router()
SWGPUB = env('SWGPUB')


@vpn.message(Command('get_vpn'))
async def get_vpn(msg: Message):
    my_id = msg.from_user.id
    cl = await Client.get(user_id=my_id).prefetch_related('vpn', 'user')
    if not cl.vpn:
        private, public = Key.key_pair()
        v = await Vpn.create(priv=private, pub=public, client=cl)
    else:
        v = cl.vpn
        private = v.priv
    txt = f'''
[Interface]
PrivateKey={private}
Address=10.0.0.{v.id}/24
DNS=1.1.1.1
[Peer]
PublicKey={SWGPUB}
AllowedIPs=0.0.0.0/0
Endpoint=vpn.xync.net:51820
PersistentKeepalive=60
'''
    file = BufferedInputFile(txt.encode(), f'{cl.user.username}_wg.conf')
    apl = MessageEntity(type='text_link', url='https://apps.apple.com/us/app/wireguard/id1441195209')
    await msg.answer_document(file, caption=f"Take your file! [ya](https://ya.ru)", caption_entities=[apl])
