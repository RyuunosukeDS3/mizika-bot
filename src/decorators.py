from functools import wraps
from discord import Embed, Color
import logging


def requires_role(role_name):
    def decorator(func):
        @wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            has_role = any(
                role.name == role_name for role in args[0].author.roles)

            if not has_role:
                embed = Embed(color=Color.red()).add_field(
                    name="", value="Você não tem permissão para usar esse comando!")
                await args[0].send(embed=embed)
                return

            return await func(ctx, *args, **kwargs)
        return wrapper
    return decorator


def log_command_usage(func):
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        command_name = func.__name__
        user_name = args[0].author.name
        logger.info(
            f"'{command_name}' used by user {user_name} ({args[0].author.id})")

        result = await func(ctx, *args, **kwargs)
        return result

    return wrapper
