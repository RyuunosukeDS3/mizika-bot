from discord import Embed, Color
from discord.ext import commands
from api.orbital import Orbital
from decorators import requires_role, log_command_usage


class OpenServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.orbital_api = Orbital()

    @commands.command(name="open_server")
    @log_command_usage
    @requires_role("server_keeper")
    async def upsert_replica_count_command(self, ctx, app_name=""):
        await ctx.message.delete()

        response = self.orbital_api.increase_argo_app_replica_count(app_name)

        embed = Embed()

        if response.status_code != 200:
            embed.title = f"Falha ao subir servidor {app_name}"
            embed.color = Color.red()
            embed.add_field(
                name="Motivo:", value=response.content, inline=False)
            
        else:
            embed.title = "Servidor de  subindo"
            embed.color = Color.green()
            embed.add_field(
                name="Servidor:", value=f"{app_name} subindo! Aguarde alguns minutos.")
        
        return await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OpenServer(bot))
