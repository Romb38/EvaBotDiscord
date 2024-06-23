import discord

async def add_role_to_member(guild: discord.Guild, member_name: str, role_name: str):
    member = discord.utils.get(guild.members, name=member_name)
    role = discord.utils.get(guild.roles, name=role_name)
    if member and role:
        await member.add_roles(role)
        return f"Le rôle {role_name} a été ajouté à {member.display_name}."
    elif not member:
        return f"Le membre {member_name} n'existe pas."
    else:
        return f"Le rôle {role_name} n'existe pas."

async def remove_role_from_member(guild: discord.Guild, member_name: str, role_name: str):
    member = discord.utils.get(guild.members, name=member_name)
    role = discord.utils.get(guild.roles, name=role_name)
    if member and role:
        await member.remove_roles(role)
        return f"Le rôle {role_name} a été retiré à {member.display_name}."
    elif not member:
        return f"Le membre {member_name} n'existe pas."
    else:
        return f"Le rôle {role_name} n'existe pas."