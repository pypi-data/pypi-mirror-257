import logging
from aiogram import Router
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import User as TgUser, ChatMemberUpdated, Message
from aiogram.utils.deep_linking import create_start_link
from antifragility_schema.models import Client
from tortoise_api_model import User
from tortoise_api_model.enum import UserStatus

main = Router()


@main.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def start_handler(msg: Message, command: CommandObject):
    me: TgUser = msg.from_user
    ref_id: int = command.args.isnumeric() and int(command.args)
    client: Client
    client, cr = await user_upsert(me)
    if cr:
        rs = 'You have registered already😉'
    elif client.id == ref_id:
        rs = 'You can not to ref yourself😒'
    elif not (ref := await Client.get_or_none(id=ref_id)):
        rs = f'No registered user #{ref_id}😬'
    else:
        rs = f'Please wait for {ref.name} approving...'
        await client.update_from_dict({'ref': ref}).save()
    return await msg.answer(rs)


@main.message(CommandStart(deep_link=True))
async def fraud_handler(msg: Message):
    logging.info(f'Start: {msg.from_user.id}. Msg: {msg}')
    # todo: alert to admins! Fraud attempt!
    await msg.answer('🤔')


@main.message(CommandStart())
async def start_no_ref_handler(msg: Message):
    me = msg.from_user
    # client, cr = await user_upsert(me) # todo: baskdoor for first user
    logging.info(f'Start: {me.id}. Msg: {msg}')
    await msg.answer(f'Sorry {me.full_name}, we do not accept only persons who has a guarantor.\n'
                     'https://telegra.ph/XyncNet-02-13')


@main.message(Command('ref_link'))
async def ref_link_handler(msg: Message):
    my_id = msg.from_user.id
    cl = await Client.get(user_id=my_id)
    link = await create_start_link(msg.bot, str(cl.id), encode=True)
    logging.info(f'Start: {my_id}. Msg: {msg}')
    await msg.answer(f"Give it to your protege: {link}")


async def user_upsert(u: TgUser, status: UserStatus = None) -> (Client, bool):
    udf = {'username': u.username, 'password': ''}
    if status:
        udf.update({'status': status})
    user, is_created = await User.update_or_create(udf, id=u.id)
    return await Client.update_or_create({'name': u.full_name}, user=user)


@main.my_chat_member()
async def user_set_status(my_chat_member: ChatMemberUpdated):
    u: TgUser = my_chat_member.from_user
    new_status = UserStatus[my_chat_member.new_chat_member.status]
    await user_upsert(u, status=new_status)


@main.message()
async def del_msg(msg: Message):
    await msg.delete()
