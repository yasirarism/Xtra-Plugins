# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd
from main_startup import bot, Friday, Config
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from xtraplugins.dB.nightmodedb import is_night_chat_in_db, get_all_night_chats, rm_night_chat, add_night_chat
from pyrogram.types import ChatPermissions
from main_startup.helper_func.logger_s import LogIt
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

@friday_on_cmd(
    ["scgrp"],
    is_official=False,
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Activate Nightmode In Group",
        "example": "{ch}scgrp",
    },
)
async def scgrp(client, message):
    pablo = await edit_or_reply(message, "`Memproses...`")
    lol = await is_night_chat_in_db(message.chat.id)
    if lol:
        await pablo.edit("Obrolan Ini Telah Mengaktifkan Mode Malam.")
        return
    await add_night_chat(message.chat.id)
    await pablo.edit(f"**Ditambahkan Obrolan {message.chat.title} dengan Id {message.chat.id} ke Database. Grup ini akan ditutup pada jam 22PM(WIB) dan akan dibuka pukul 6AM(WIB)**")


@friday_on_cmd(
    ["rsgrp"],
    is_official=False,
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Deactivate Nightmode In Group",
        "example": "{ch}rsgrp",
    },
)
async def scgrp(client, message):
    pablo = await edit_or_reply(message, "`Searching For Anime.....`")
    lol = await is_night_chat_in_db(message.chat.id)
    if not lol:
        await pablo.edit("Obrolan Ini Belum Mengaktifkan Mode Malam.")
        return
    await rm_night_chat(message.chat.id)
    await pablo.edit(f"**Menghapus obrolan {message.chat.title} dengan Id {message.chat.id} dari Database. Grup ini tidak akan ditutup pada 22PM(WIB) dan akan dibuka pada 6AM(WIB)**")


async def job_close():
    lol = await get_all_night_chats()
    if len(lol) == 0:
        return
    for warner in lol:
        try:
            await Friday.send_message(
              int(warner.get("chat_id")), "**🌃 Night Mode Activated**\n\n`Sekarang jam 22:00, Grup ditutup sampai jam 6 pagi. Selamat beristirahat semuanya!!` \n**Powered By YMovieZNew**"
            )
            await Friday.set_chat_permissions(warner.get("chat_id"), ChatPermissions())
            async for member in Friday.iter_chat_members(warner.get("chat_id")):
             if member.user.is_deleted:
                try:
                    await Friday.kick_chat_member(warner.get("chat_id"), member.user.id)
                except:
                    pass
        except Exception as e:
            logging.info(str(e))
            ido = warner.get("chat_id")
            try:
                await Friday.send_message(Config.LOG_GRP, f"[NIGHT MODE]\n\nFailed To Close The Group {ido}.\nError : {e}")
            except:
                pass


scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")
scheduler.add_job(job_close, trigger="cron", hour=22, minute=0)
scheduler.start()

async def job_open():
    lol = await get_all_night_chats()
    if len(lol) == 0:
        return
    for warner in lol:
        try:
            await Friday.send_message(
              int(warner.get("chat_id")), "`Sekarang jam 6 pagi, selamat pagi, grup kini telah dibuka.`\n**Powered By YMovieZNew**"
            )
            await Friday.set_chat_permissions(
                        warner.get("chat_id"),
                        ChatPermissions(
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_stickers=True,
                            can_send_animations=True
                         )
            )
            
        except Exception as e:
            logging.info(str(e))
            ido = warner.get("chat_id")
            try:
                await Friday.send_message(Config.LOG_GRP, f"[NIGHT MODE]\n\nFailed To Open The Group {ido}.\nError : {e}")
            except:
                pass
            

scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")
scheduler.add_job(job_open, trigger="cron", hour=6, minute=0)
scheduler.start()
