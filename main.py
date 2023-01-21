import disnake, hashlib, os
from typing import Optional
from config import cursor, connection, token_laucherregister, prefix_bot
from disnake.ext import commands
from disnake import Intents, TextInputStyle, ModalInteraction

class register_button(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=10.0)
        self.value: Optional[bool] = None
    @disnake.ui.button(label="Зарегистрироваться", emoji="💼", style=disnake.ButtonStyle.blurple, custom_id="button_register")
    async def register(self):
        pass
class register_launch(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Ведите свой никнейм.",
                placeholder="",
                custom_id="username",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Ведите пароль.",
                placeholder="",
                custom_id="password",
                style=TextInputStyle.short,
            ),
        ]
        super().__init__(
            title="Регистрация",
            custom_id="register_laucher",
            components=components,
        )

bot = commands.Bot(command_prefix=prefix_bot, intents=Intents.all())

@bot.event
async def on_ready():
    cursor.execute("""CREATE TABLE IF NOT EXISTS laucher (id BIGINT, username varchar(40), password varchar(255), uuid char(36), accessToken char(32), serverID varchar(41), hwidId bigint(20))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS `hwids` (`id` bigint(20) NOT NULL,`publickey` blob,`hwDiskId` varchar(255) DEFAULT NULL,`baseboardSerialNumber` varchar(255) DEFAULT NULL,`graphicCard` varchar(255) DEFAULT NULL,`displayId` blob,`bitness` int(11) DEFAULT NULL,`totalMemory` bigint(20) DEFAULT NULL,`logicalProcessors` int(11) DEFAULT NULL,`physicalProcessors` int(11) DEFAULT NULL,`processorMaxFreq` bigint(11) DEFAULT NULL,`battery` tinyint(1) NOT NULL DEFAULT "0",`banned` tinyint(1) NOT NULL DEFAULT "0")""")
    connection.commit()
    print("Я запустился")

@bot.command()
@commands.has_permissions(administrator=True)
async def register(ctx):
    await ctx.send(embed=disnake.Embed(title="Регистрация", description="Для регистрации нажмите ниже кнопку(все данные шифрутся)!", colour=disnake.Colour.purple()),view=register_button())

@bot.event
async def on_modal_submit(inter: ModalInteraction):
    if inter.custom_id == "register_laucher":
        for key, value in inter.text_values.items():
            if key == "username":
                value1=value
            if key == "password":
                value2=value
        cursor.execute(f"SELECT id FROM laucher WHERE id = {inter.author.id}")
        if cursor.fetchone() is None:
            cursor.execute(f"SELECT username FROM laucher WHERE username = '{value1}'")
            if cursor.fetchone() is None:
                h=hashlib.sha256(value2.encode())
                passh=h.hexdigest()
                cursor.execute(f"INSERT INTO laucher VALUES ({inter.author.id},'{value1}', '{passh}',NULL,NULL,NULL,NULL)")
                connection.commit()
                await inter.response.send_message(embed=disnake.Embed(title="Аккаунт", description="Вы успешно зарегистрированы", colour=disnake.Colour.purple()),ephemeral=True)
            else:
                cursor.execute(f"SELECT id FROM laucher WHERE username = '{value1}'")
                guild=bot.get_guild(1060899660065153074)
                member=guild.get_member(cursor.fetchone()[0])
                await inter.response.send_message(embed=disnake.Embed(title="Данный акаунт уже зарегистрирован", description=f"Вот аккаунт в дискорде {member.id} зарегистрированый на данный никнейм **{value1}**!", colour=disnake.Colour.purple()),ephemeral=True)
        else:
            cursor.execute(f"SELECT username FROM laucher WHERE id = {inter.author.id}")
            await inter.response.send_message(embed=disnake.Embed(title="Аккаунт", description=f"Вы уже создали свой аккаунт {cursor.fetchone()[0]}!", colour=disnake.Colour.purple()),ephemeral=True)

@bot.event
async def on_button_click(inter):
    if inter.component.custom_id == "button_register":
        await inter.response.send_modal(modal=register_launch())

bot.run(token_laucherregister)