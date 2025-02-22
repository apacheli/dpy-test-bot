import aiohttp
import asyncio
import discord
from discord.ext import commands
from discord.ui import button, Button, Modal, TextInput, View
import json


levels = (
    0,
    17.165605545043945,
    18.53504753112793,
    19.90485382080078,
    21.27490234375,
    22.6454,
    24.649612426757812,
    26.640642166137695,
    28.868587493896484,
    31.36768,
    34.14334487915039,
    37.201,
    40.66,
    44.4466667175293,
    48.56352,
    53.74848,
    59.0818977355957,
    64.4200439453125,
    69.72446,
    75.12314,
    80.58478,
    86.11203,
    91.70374,
    97.24463,
    102.8126449584961,
    108.40956,
    113.20169,
    118.1029052734375,
    122.97932,
    129.72732543945312,
    136.29291,
    142.6708526611328,
    149.02902,
    155.41699,
    161.8255,
    169.10631,
    176.51808,
    184.07274,
    191.70952,
    199.55691528320312,
    207.38205,
    215.3989,
    224.16566467285156,
    233.50216674804688,
    243.35057,
    256.0630798339844,
    268.5435,
    281.52606201171875,
    295.0136413574219,
    309.0672,
    323.6016,
    336.7575378417969,
    350.5303,
    364.4827,
    378.6191711425781,
    398.6004,
    416.39825439453125,
    434.387,
    452.9510498046875,
    472.6062316894531,
    492.8849,
    513.5685424804688,
    539.1032,
    565.5105590820312,
    592.5387573242188,
    624.4434,
    651.4701538085938,
    679.4968,
    707.7940673828125,
    736.6714477539062,
    765.6402587890625,
    794.7734,
    824.6773681640625,
    851.1578,
    877.7420654296875,
    914.2291,
    946.7467651367188,
    979.4114,
    1011.223,
    1044.791748046875,
    1077.4437,
    1109.99755859375,
    1142.9766,
    1176.3695,
    1210.1844482421875,
    1253.8357,
    1288.9527587890625,
    1325.4841,
    1363.4569,
    1405.0974,
    1446.8535,
    1488.2156,
    1528.4446,
    1580.3679,
    1630.8475,
    1711.19775390625,
    1780.454,
    1847.32275390625,
    1911.4744,
    1972.8644,
    2030.0718,
)

shields = (
    0,
    91.1791,
    98.7076644897461,
    106.23622,
    113.76477,
    121.29332,
    128.82188415527344,
    136.35042,
    143.8789825439453,
    151.4075164794922,
    158.93608,
    169.99148559570312,
    181.07625,
    192.19037,
    204.0482,
    215.939,
    227.8627471923828,
    247.68594360351562,
    267.5421,
    287.4312,
    303.826416015625,
    320.2252197265625,
    336.62762451171875,
    352.31927490234375,
    368.01092529296875,
    383.7025451660156,
    394.432373046875,
    405.18145751953125,
    415.9499206542969,
    426.7376403808594,
    437.5447,
    450.6,
    463.7003,
    476.8455810546875,
    491.1275,
    502.5545654296875,
    514.0121,
    531.4096,
    549.9796,
    568.5849,
    584.9965,
    605.6703491210938,
    626.3862,
    646.0523,
    665.7556,
    685.4961,
    700.8394,
    723.3331,
    745.8653,
    768.4357,
    786.7919311523438,
    809.5388,
    832.3290405273438,
    855.1626586914062,
    878.0396,
    899.4848,
    919.362,
    946.0396,
    974.7642,
    1003.5786,
    1030.077,
    1056.635,
    1085.2463,
    1113.9244,
    1149.2587,
    1178.0648,
    1200.2237548828125,
    1227.6603,
    1257.243,
    1284.9173583984375,
    1314.7529,
    1342.6652,
    1372.75244140625,
    1396.321,
    1427.3124,
    1458.3745,
    1482.3358,
    1511.9109,
    1541.5493,
    1569.1537,
    1596.8143,
    1622.4197,
    1648.074,
    1666.3761,
    1684.6782,
    1702.9803466796875,
    1726.1047,
    1754.6715,
    1785.8666,
    1817.137451171875,
    1851.0603,
    1885.0671,
    1921.7493,
    1958.5233,
    2006.1941,
    2041.569,
    2054.47216796875,
    2065.975,
    2174.72265625,
    2186.768310546875,
    2198.814,
)


class ThinkView(View):
    def __init__(self, think):
        super().__init__(timeout=None)
        self.think = think or "..."

    @button(label="See Thoughts", style=discord.ButtonStyle.gray, emoji="\N{THOUGHT BALLOON}")
    async def think_button(self, interaction: discord.Interaction, _):
        await interaction.response.send_message(self.think, ephemeral=True)


def parse_message(message):
    end_think = message.find("</think>")
    return message[7:end_think].strip(), message[end_think + 8:].strip()


class ElementalMasteryModal(Modal):
    level = TextInput(
        label="Level",
        placeholder="What is the character's level?",
        default="90",
        max_length=8,
    )
    elemental_mastery = TextInput(
        label="Elemental Mastery",
        placeholder="What is the character's Elemental Mastery?",
        max_length=8,
    )
    reaction_bonus = TextInput(
        label="Reaction Bonus",
        placeholder="Any additional damage bonus for reactions.",
        default="0",
        max_length=8,
    )

    def __init__(self, view):
        super().__init__(title="Elemental Mastery Calculator")
        self.view = view

    def is_finished(*args, **kwargs):
        return False

    async def on_submit(self, interaction: discord.Interaction):
        level = self.level.default = self.level.value
        elemental_mastery = self.elemental_mastery.default = self.elemental_mastery.value
        reaction_bonus = self.reaction_bonus.default = self.reaction_bonus.value
        if not level.isdigit():
            return await interaction.response.edit_message(content=":x: Invalid **Level**. Please try again.", embeds=[])
        level = int(level)
        if level < 1 or level > 100:
            return await interaction.response.edit_message(content=":x: Invalid **Level**. Please try again.", embeds=[])
        if not elemental_mastery.isdigit():
            return await interaction.response.edit_message(content=":x: Invalid **Elemental Mastery**. Please try again.", embeds=[])
        if not reaction_bonus.isdigit():
            return await interaction.response.edit_message(content=":x: Invalid **Reaction Bonus**. Please try again.", embeds=[])
        elemental_mastery = int(elemental_mastery)
        reaction_bonus = int(reaction_bonus)
        x = 2.78 * elemental_mastery / (elemental_mastery + 1_400) * 100 + reaction_bonus
        y = 16 * elemental_mastery / (elemental_mastery + 2000) * 100 + reaction_bonus
        z = 5 * elemental_mastery / (elemental_mastery + 1_200) * 100 + reaction_bonus
        w = 4.44 * elemental_mastery / (elemental_mastery + 1_400) * 100 + reaction_bonus
        rb_embed = discord.Embed(title="Elemental Reaction Bonus", color=0x4cc2f0)
        rb_embed.add_field(name="Level", value=level)
        rb_embed.add_field(name="Elemental Mastery", value=elemental_mastery)
        rb_embed.add_field(name="Reaction Bonus", value=f"{reaction_bonus}%")
        rb_embed.add_field(name="Amplifying Bonus", value=f"{x:.2f}%")
        rb_embed.add_field(name="Transformative Bonus", value=f"{y:.2f}%")
        rb_embed.add_field(name="Additive Bonus", value=f"{z:.2f}%")
        rb_embed.add_field(name="Crystallize Bonus", value=f"{w:.2f}%")
        rdy = levels[level] * (y + 100) / 100
        rdz = levels[level] * (z + 100) / 100
        rdw = shields[level] * (w + 100) / 100
        rd_embed = discord.Embed(title="Elemental Reaction Damage", color=0xaf8ec1)
        rd_embed.add_field(name="Burning", value=f"{.25 * rdy:.2f}")
        rd_embed.add_field(name="Swirl", value=f"{.6 * rdy:.2f}")
        rd_embed.add_field(name="Superconduct", value=f"{1.5 * rdy:.2f}")
        rd_embed.add_field(name="Electro-Charged, Bloom", value=f"{2 * rdy:.2f}")
        rd_embed.add_field(name="Overloaded", value=f"{2.75 * rdy:.2f}")
        rd_embed.add_field(name="Burgeon, Hyperbloom, Shatter", value=f"{3 * rdy:.2f}")
        rd_embed.add_field(name="Aggravate", value=f"{rdz * 1.15:.2f}")
        rd_embed.add_field(name="Spread", value=f"{rdz * 1.25:.2f}")
        rd_embed.add_field(name="Crystallize", value=f"{rdw:.2f}")
        await interaction.response.edit_message(content="", embeds=[rb_embed, rd_embed])


class ElementalMasteryView(View):
    def __init__(self, ctx: commands.Context):
        super().__init__()
        self.ctx = ctx
        self.modal = ElementalMasteryModal(self)

    @button(style=discord.ButtonStyle.secondary, label="Calculate", emoji="\N{CYCLONE}")
    async def calculate(self, interaction: discord.Interaction, _):
        await interaction.response.send_modal(self.modal)

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.ctx.author.id


class Entertainment(commands.Cog):
    """A bunch of fun commands for the squad to use whenever you're bored."""
    help_emoji = "\N{VIDEO GAME}"
    help_color = 0xd4c44a

    @commands.command()
    async def em(self, ctx: commands.Context):
        """Calculate Elemental Mastery"""
        await ctx.reply("Click **\N{CYCLONE} Calculate** to get started.", view=ElementalMasteryView(ctx))

    def _handle_bloons_document(self, ctx: commands.Context):
        pass

    @commands.group()
    async def bloons(self, ctx: commands.Context):
        """Really useful Bloons TD 6 commands"""
        pass

    @bloons.command()
    async def boss(self, ctx: commands.Context):
        """Get boss information"""
        await ctx.reply("ur mom")

    @bloons.command()
    async def daily(self, ctx: commands.Context):
        """Get daily challenge information"""
        pass

    @bloons.command()
    async def race(self, ctx: commands.Context):
        """Get race information"""
        pass

    @bloons.command()
    async def odyssey(self, ctx: commands.Context):
        """Get odyssey information"""
        pass

    @bloons.command()
    async def ct(self, ctx: commands.Context):
        """Get contested territory information"""
        pass

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ai(self, ctx: commands.Context, *, prompt):
        """Ask the AI something"""
        ollama = ctx.bot.config["ollama"]
        body = {
            "model": ollama["model"],
            "prompt": prompt,
            "stream": False,
        }
        url = f"http://{ollama["host"]}:{ollama["port"]}/api/generate"
        message = await ctx.reply(f":hourglass: Coming up with something creative...")
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            try:
                async with session.post(url, json=body) as response:
                    data = await response.json()
                    think, reply = parse_message(data["response"])
                    await message.edit(content=reply, view=ThinkView(think))
            except asyncio.TimeoutError:
                await message.edit(content=":x: Took too long to respond. Please try again!")


async def setup(bot):
    await bot.add_cog(Entertainment(bot))
