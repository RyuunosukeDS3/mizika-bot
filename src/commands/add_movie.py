from discord import Embed, Color
from discord.ext import commands
from api.transmission import Transmission
from api.radarr import Radarr
from decorators import requires_role, log_command_usage


class DownloadMovie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.transmission_api = Transmission()
        self.radarr_api = Radarr()

    @commands.command(name="add_movie")
    @log_command_usage
    @requires_role("trusted_downloader")
    async def add_movie_command(self, ctx, magnet_link=""):
        torrent = magnet_link
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment.filename.endswith(".torrent"):
                torrent = await attachment.read()

        await ctx.message.delete()

        torrent_data = self.transmission_api.add_torrent(torrent, "radarr")
        embed = Embed()

        if not torrent_data:
            embed.title = "Falha ao adicionar Torrent"
            embed.color = Color.red()
            embed.add_field(
                name="Motivo:",
                value="Arquivo torrent ou link magnético inválido.",
                inline=False,
            )
            return await ctx.send(embed=embed)

        self.radarr_api.refresh_monitored_downloads_command()
        movie_data = self.radarr_api.get_radarr_queue_by_torrent_id(
            torrent_data.hash_string
        )

        if movie_data:
            embed.title = f"Adicionado {movie_data['movie']['title']} ({movie_data['movie']['originalTitle']})"
            embed.color = Color.green()
            embed.add_field(
                name="Qualidade:",
                value=movie_data["quality"]["quality"]["name"],
                inline=False,
            )
            embed.set_thumbnail(url=movie_data["movie"]["images"][0]["remoteUrl"])
            embed.set_footer(text=f"ID do torrent {torrent_data.hash_string}")
        else:
            embed.title = "Falha ao adicionar Torrent"
            embed.color = Color.red()
            embed.add_field(
                name="Motivo:",
                value="Filme precisa primeiro ser solicitado via [Overseerr](https://overseerr.mizika.duckdns.org/)",
                inline=False,
            )
            self.transmission_api.remove_torrent(torrent_data.id)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(DownloadMovie(bot))
