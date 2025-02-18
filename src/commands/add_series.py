from discord import Embed, Color
from discord.ext import commands
from api.transmission import Transmission
from api.sonarr import Sonarr
from decorators import requires_role, log_command_usage


class DownloadSeries(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.transmission_api = Transmission()
        self.sonarr_api = Sonarr()

    @commands.command(name="add_series")
    @log_command_usage
    @requires_role("trusted_downloader")
    async def add_series_command(self, ctx, magnet_link=""):
        torrent = magnet_link
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment.filename.endswith(".torrent"):
                torrent = await attachment.read()

        await ctx.message.delete()

        torrent_data = self.transmission_api.add_torrent(torrent, "sonarr")
        embed = Embed()

        if not torrent_data:
            embed.title = "Falha ao adicionar Torrent"
            embed.color = Color.red()
            embed.add_field(
                name="Motivo:", value="Arquivo torrent ou link magnético inválido.", inline=False)
            return await ctx.send(embed=embed)

        self.sonarr_api.refresh_monitored_downloads_command()
        series_data = self.sonarr_api.get_sonarr_series(
            torrent_data.hash_string)

        if series_data:
            embed.title = f"Adicionado {series_data['title']}"
            embed.color = Color.green()
            embed.add_field(
                name="Status:", value="Monitorado", inline=False)
            embed.set_thumbnail(url=series_data['images'][0]['remoteUrl'])
            embed.set_footer(text=f"ID do torrent {torrent_data.hash_string}")
        else:
            embed.title = "Falha ao adicionar Torrent"
            embed.color = Color.red()
            embed.add_field(
                name="Motivo:", value="Série precisa primeiro ser solicitada via [Overseerr](https://overseerr.mizika.duckdns.org/)", inline=False)
            self.transmission_api.remove_torrent(torrent_data.id)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(DownloadSeries(bot))
