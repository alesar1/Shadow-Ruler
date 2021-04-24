# bot.py
# potrei ottimizzare tutto con delle funzioni ma al momento non ne ho voglia
# in futuro probabilmente lo farò
import discord
import datetime
import random
import os


TOKEN = "ODM0NDU5NDU5NDA0NDMxNDkw.YIBM7g.wTCbevovCVNDU8QqVcj4gmYYJ0c"

client = discord.Client()


@client.event
async def on_ready():
    print("{0.user} è online!".format(client))


@client.event
async def on_message(message):

# RICKROLL

    # no rickroll
    if (
        "dQw4w9WgXcQ" in message.content
        or "oHg5SJYRHA0" in message.content
        or "j5a0jTc9S10" in message.content
        or "!play never gonna give you up" in message.content.lower()
    ):
        await message.delete()
        await message.channel.send("Non mi RickRollerai hahaha")
        await message.channel.send(file=discord.File("imgs/ET.jpg"))
        print(
            "tentativo di rickroll alle " + datetime.datetime.now().strftime("%H:%M:%S")
        )
        return

# GOOGLE

    # cerca su Google (pagina principale)
    elif message.content.startswith("!googla "):
        query = message.content[8:]
        if "." in query:
            await message.channel.send("Forse il comando che vuoi usare è **!cerca**")
            return
        query = query.replace(" ", "+")
        await message.channel.send(f"https://google.com/search?q={query.lower()}")
        print(
            f"ricerca generica su Google ({query}) alle "
            + datetime.datetime.now().strftime("%H:%M:%S")
        )
        return

    # cerca su Google (nome sito)
    elif message.content.startswith("!cerca "):
        query = message.content[7:]
        if "." not in query:
            await message.channel.send("Forse il comando che vuoi usare è **!googla**")
            return
        query = query.replace(" ", "")
        url = "https://"
        await message.channel.send(url + query.lower())
        print(
            f"ricerca specifica su Google ({query}) alle "
            + datetime.datetime.now().strftime("%H:%M:%S")
        )
        return

# HELP

    # help comandi
    elif message.content.startswith("!comandi"):
        await message.channel.send(
            "Ecco i comandi disponibili (per ora): \n\n**Bot**\n- !bot_pic --> immagine profilo del bot\n\n**Google**\n- !googla [query] --> effettua ricerca su Google\n- !cerca [sito] --> cerca il sito specifico su Google\n\n**Avviso Online**\n- !prenota [ora] --> prenotati per un orario\n- !annulla_prn [ora] --> annulla prenotazione\n- !schedule --> visualizza elenco prenotazioni"
        )
        print(
            "visualizzata lista comandi alle "
            + datetime.datetime.now().strftime("%H:%M:%S")
        )
        return

# BOT

    # mostra foto profilo
    elif message.content.startswith("!bot_pic"):
        await message.channel.send("Ecco la mia immagine profilo")
        await message.channel.send(file=discord.File("image.png"))

# SCHEDULE

    # prenota quando online
    elif message.content.startswith("!prenota "):

        ora = message.content[9:]

        if len(ora[-4:]) != 4:
            await message.channel.send(
                "Il formato dell'ora non è corretto.\n(deve essere **[ore]:[minuti (con anche secondi)]**)"
            )
            return
        nome = message.author.name

        schedule_fl_r = open("schedule.txt", "r")
        schedule = schedule_fl_r.readlines()
        schedule.sort()
        schedule_fl_r.close()

        # controlla che non ci siano orari duplicati
        if f"{nome}: {ora}\n" in schedule:
            await message.channel.send(f"{nome} ti sei già segnato per quell'orario!")
            return

        # appende il nome e l'ora nel file
        schedule_fl_w = open("schedule.txt", "a")
        schedule_fl_w.write(f"{nome}: {ora}\n")
        schedule_fl_w.close()
        await message.channel.send(
            "Ho registrato la prenotazione.\nDigita **!schedule** per visualizzare l'elenco delle prenotazioni."
        )
        return

    # rimuovi prenotazione
    elif message.content.startswith("!annulla_prn "):

        ora = message.content[13:]
        if len(ora[-4:]) != 4:
            await message.channel.send(
                "Il formato dell'ora non è corretto.\n (deve essere **[ore]:[minuti (con anche secondi)]**)"
            )
            return
        nome = message.author.name

        schedule_fl_r = open("schedule.txt", "r")
        schedule = schedule_fl_r.readlines()
        schedule_fl_r.close()

        print(schedule)
        print(f"{nome}: {ora}\n")

        # controlla che l'orario che si vuole rimuovere esista
        if f"{nome}: {ora}\n" not in schedule:
            await message.channel.send(
                f"{nome} non ti sei mai prenotato per quest'orario!"
            )
            return

        # elimina la prenotazione
        schedule.remove(f"{nome}: {ora}\n")
        print(schedule)

        # riscrive nel file le altre prenotazioni
        schedule_fl_w = open("schedule.txt", "w")
        for prenotazione in schedule:
            schedule_fl_w.write(prenotazione)
        schedule_fl_w.close()
        await message.channel.send(
            "Prenotazione rimossa.\nDigita **!schedule** per visualizzare l'elenco delle prenotazioni."
        )
        return

    # mostra schedule
    elif message.content.startswith("!schedule"):
        schedule_fl_r2 = open("schedule.txt", "r")
        schedule = schedule_fl_r2.readlines()
        if schedule == []:
            await message.channel.send("Attualmente non ci sono prenotazioni.\nPer prenotarti per un orario digita **!prenota [ora]**")
        schedule.sort()
        try:
            schedule.remove("\n")
        except ValueError:
            pass
        schedule_fl_r2.close()
        for prenotazione in schedule:
            await message.channel.send(prenotazione)
        return


client.run(TOKEN)
