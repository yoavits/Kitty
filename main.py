#discord
import discord
from discord.ext import commands, tasks
from discord import app_commands, ButtonStyle, SelectOption, ui, Component, components, ActionRow
from discord.app_commands import Choice
from discord.ui import Button, View, Select, Modal


#features
import random
import datetime
import time
import asyncio
from bs4 import BeautifulSoup
import aiohttp
import json
import functools
import re



# - - - - - - - - - - - - - - - - - - - - - - - - - 

# Bot Data 📟

#Inroduction: The Kitty 😺
# Set up the bot bot


#bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(command_prefix='.', intents=intents)

    async def setup_hook(self):
        self.add_view(Verification())
        self.add_view(InfoButtons())
        self.add_view(Community_Feedback())
        self.add_view(Staff_Feedback())
        self.add_view(TicketView())

        ticket_args = load_ticket_args()

        if ticket_args is not None:
            await self.wait_until_ready()  # Wait until the bot is ready and the cache is filled

            username = self.get_user(ticket_args["username"])
            support_channel = self.get_channel(ticket_args["support_channel"])
            staff_role = self.get_guild(1069000601318457415).get_role(ticket_args["staff_role"])
            channel_name = ticket_args["channel_name"]
            issue = ticket_args["issue"]
            notes = ticket_args["notes"]

            await self.add_ticket_handler(username, support_channel, staff_role, channel_name, issue, notes)




def save_ticket_args(username, support_channel, staff_role, channel_name, issue, notes):
    ticket_args = {
        "username": username.id,
        "support_channel": support_channel.id,
        "staff_role": staff_role.id,
        "channel_name": channel_name,
        "issue": issue.value,  # Extract the text value from TextInput
        "notes": notes.value   # Extract the text value from TextInput
    }

    with open("ticket_args.json", "w") as f:
        json.dump(ticket_args, f)


#bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


# Bot Token
Token = "MTA3NDQ2MDQxNzQ1NzM4OTU3OA.GtM3oO.nNS3AjjOxfozrv-nnrAokQ3mdfM_5Z733p-ykI"


# - - - - - - - - - - - - - - - - - - - - - - - - - 

# Bot Startup
#@bot.event
async def on_ready(self):

     # - - - - - - - - - - - -
    # UTILITIES 🪶

    update_status.start()
    update_category.start()

    #bot.add_view(InfoButtons())
    await self.setup_hook()

 
     # - - - - - - - - - - - -
    # LOGS 📂
 
    #1. entrance_logging_channel_id - members entrance: joining/leaving the server
    #2. role_logging_channel_id - roles actions: removed/edited/created, and assign roles to users (added/removed)
    #3. history_logging_channel_id - messages that have been deleted or edited
    #4. moderation_logging_channel_id - moderations actions that have been made towards a user in the server

    global entrance_logging_channel_id, role_logging_channel_id, history_logging_channel_id, moderation_logging_channel_id, feedback_logging_channel_id, support_logging_channel_id
     
    # Load channel IDs from JSON file
    with open("channel_ids.json", "r") as f:
        data = json.load(f)
        entrance_logging_channel_id = data.get("entrance_logging_channel_id", None)
        role_logging_channel_id = data.get("role_logging_channel_id", None)
        history_logging_channel_id = data.get("history_logging_channel_id", None)
        moderation_logging_channel_id = data.get("moderation_logging_channel_id", None)
        feedback_logging_channel_id = data.get("feedback_logging_channel_id", None)
        support_logging_channel_id = data.get("support_logging_channel_id", None)


    # - - - - - - - - - - - -
    # BOT READY 🟢

    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


    # - - - - - - - - - - - -
bot = PersistentViewBot()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#Defining Public Variables

SUCCESS_EMOJI = "<:success:1092430169324671076>"
ERROR_EMOJI = "<:error:1092430391387885711>"
PROCESSING_EMOJI = "<:processing:1092430887376920757>"
SEARCH_EMOJI = "<:search:1092430885267181619>"
COOLDOWN_EMOJI = "<:cooldown:1092429966882385950>"
SETTINGS_EMOJI = "<:settings:1092430881840435281>"
WARNING_EMOJI = "<:warning:1092431273806528602>"
ID_EMOJI = "<:id:1092431281658286100>"
CONNECTION_EMOJI = "<:connection:1092431275660423249>"
FILES_EMOJI = "<:files:1092431278814527530>"
MEMBERS_EMOJI = "<:members:1092431268966301748>"
SENDING_EMOJI = "<:sending:1092429291939168336>"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Bot Utilies  🪶

# Utilites Storage

EMOJIS = (':cat:', ':dog:', ':hamster:', ':bird:', ':rabbit:', ':mouse:') # 😺, 🐶, 🐹, 🐦, 🐰, 🐭

# Storage
category_id = 1069053476971216946 # 🏡 LOBBY Category Id



statuses = [
    {"type": discord.ActivityType.listening, "name": ""},
    {"type": discord.ActivityType.playing, "name": "with kindle toys 🧸"},
]

@tasks.loop(minutes=1)
async def update_status():
    status = statuses.pop(0)
    statuses.append(status)
    if status["type"] == discord.ActivityType.listening:
        for guild in bot.guilds:
         member_count = guild.member_count
        status["name"] = f"{member_count} members 🐇"
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=status["type"], name=status["name"]))


@tasks.loop(minutes=1)
async def update_category():
    guild = bot.get_guild(1069000601318457415)  # Replace with your server ID
    category = guild.get_channel(category_id)

    if category:
        member_count = guild.member_count
        category_name = f"🏡 LOBBY | {member_count}"
        if category.name != category_name:
            await category.edit(name=category_name)
            print(f"✅ Successfully Updated category name to {category_name}")
    else:
        print("❌ Category not found")

          
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# ==========================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Bot Logs Embeds 💬

intents = discord.Intents.all()
intents.members = True

logging_channels = {}  # initialize the logging_channels dictionary


# Join log embed 💬
@bot.event 
async def on_member_join(member):
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    channel = await entrance_get_logging_channel(member.guild)
    role = member.guild.get_role(1091471850095251618)
    if channel is not None:
        embed = discord.Embed(
            title="Member Joined!",
            description=f"{member.mention} joined the server! Here are some details about the user.",
            color=discord.Color.light_gray(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{bot.user.name} 🐈 | Logging", icon_url=bot.user.avatar)
        embed.add_field(name="Username", value=member.name)
        embed.add_field(name="ID", value= f"{member.id}")
        embed.add_field(name="Account Created", value=member.created_at.strftime("%b %d, %Y"))
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=f"Member Joined | {bot.user.name}🐈")
        await channel.send(embed=embed)

        # assign the role to the new member
        await member.add_roles(role)

# Left log embed 💬
@bot.event 
async def on_member_remove(member):
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    channel = await entrance_get_logging_channel(member.guild)
    if channel is not None:
        embed = discord.Embed(
            title="Member Left!",
            description=f"{member.mention} left the server! Here are some details about the user.",
            color=discord.Color.darker_gray(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{bot.user.name} 🐈 | Logging", icon_url=bot.user.avatar)
        embed.add_field(name="Username", value=member.name)
        embed.add_field(name="ID", value=f"{member.id}")
        embed.add_field(name="Account Created", value=member.created_at.strftime("%b %d, %Y"))
        if member.joined_at is not None:
            embed.add_field(name="Membership", value=member.joined_at.strftime("%b %d, %Y"))
        else:
            embed.add_field(name="Membership", value="Unknown")
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        roles_str = ", ".join(roles) if roles else "None"
        embed.add_field(name="Roles", value=roles_str)
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=f"Member Left | {bot.user.name}🐈")
        await channel.send(embed=embed)



# - - - - - - - - - - - - - - - - 


# Role giver/remove log embed 💬

# Define a list to store the role changes for each user
role_changes = {}

@bot.event
async def on_member_update(before, after):
    global role_logging_channel_id
    channel = await role_get_logging_channel(after.guild)
    if channel is None:
        print("Unable to find channel.")
        return
    roles_added = set(after.roles) - set(before.roles)
    roles_removed = set(before.roles) - set(after.roles)
    """"""
    if roles_added and not roles_removed:
        if after.id not in role_changes:
            role_changes[after.id] = {"added": roles_added, "removed": set()}
        else:
            role_changes[after.id]["added"] |= roles_added
    elif roles_removed and not roles_added:
        if after.id not in role_changes:
            role_changes[after.id] = {"added": set(), "removed": roles_removed}
        else:
            role_changes[after.id]["removed"] |= roles_removed
    elif roles_added and roles_removed:
        if after.id not in role_changes:
            role_changes[after.id] = {"added": roles_added, "removed": roles_removed}
        else:
            role_changes[after.id]["added"] |= roles_added
            role_changes[after.id]["removed"] |= roles_removed
    
    # Check if there are any role changes for the user
    if after.id in role_changes:
        # Wait for 10 seconds before sending the embed
        await asyncio.sleep(10)

        changes = role_changes.get(after.id, {"added": set(), "removed": set()})
        """
        roles_added_title = ""
        roles_added_description = ""
        if roles_added > 1:
            roles_added_title = "Roles have been Attached!"
            roles_added_description = f"The following roles have been added to {after.mention}:\n{added_roles_str}\n"
        else:
            roles_added_title = "Role has been Attached"
            roles_added_description = f"The following has been added to {after.mention}:\n{added_roles_str}\n"
        
        roles_removed_title = ""
        roles_removed_description = ""
        if roles_removed > 1:
            roles_added_title = "Roles have been Subtracted!"
            roles_added_description = f"The following roles have been removed from {after.mention}:\n{removed_roles_str}\n"

        else:
            roles_added_title = "Role has been Subtracted"
            roles_added_description = f"The following has been removed from {after.mention}:\n{removed_roles_str}\n"
        """
        #responsible = before.guild.get_member(bot.user.id).display_name
        embed = None
        if changes["added"] and not changes["removed"]:
            added_roles_str = "\n".join([f"`‣` {role.mention}" for role in changes["added"]])
             
            embed = discord.Embed(
                title= "Roles have been Subtracted!",
                description=f"The following roles have been added to {after.mention}:\n{added_roles_str}\n", 
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now(),
            )
     
            embed.set_footer(text=f"Roles Attached | {bot.user.name}🐈")# | Added by {responsible}")
        elif changes["removed"] and not changes["added"]:
            removed_roles_str = "\n".join([f"`‣` {role.mention}" for role in changes["removed"]])
            embed = discord.Embed(
                title="Roles have been Subtracted!",
                description=f"The following roles have been removed from {after.mention}:\n{removed_roles_str}\n",
                color=discord.Color.dark_blue(),
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text=f"Roles Subtracted | {bot.user.name}🐈")# | Removed by {responsible}")
        elif changes["added"] and changes["removed"]:
            added_roles_str = "\n".join([f">  {role.mention}" for role in changes["added"]])
            removed_roles_str = "\n".join([f">  {role.mention}" for role in changes["removed"]])
            embed = discord.Embed(
                title="Roles have been Replaced!",
                description=f"The following roles have been added and removed from {after.mention}:",
                color=discord.Color.purple(),
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text=f"Roles Replaced | {bot.user.name}🐈")# | Replaced by {responsible}")
            embed.add_field(name="Removed", value=removed_roles_str, inline=True)
            embed.add_field(name="Added", value=added_roles_str, inline=True)

        if embed is not None:
        # Send the embed to the logging channel
            embed.set_author(name=f"{bot.user.name} | Logging", icon_url=bot.user.avatar)
            await channel.send(embed=embed)

        # Clear the role changes for the user
        role_changes.pop(after.id, None)
        

# Role created log embed 💬
@bot.event
async def on_guild_role_create(role):
    channel = await role_get_logging_channel(role.guild)
    if channel is None:
        print("Unable to find channel.")
        return

    embed = discord.Embed(
        title="Role Created!",
        description=f"The role **{role.name}** has sucessfully been created.",
        color=discord.Color.green(),
        timestamp=datetime.datetime.now()
    )

    embed.set_author(name=f"{bot.user.name} | Logging", icon_url=bot.user.avatar)
    embed.set_footer(text=f"Role Create | {bot.user.name}🐈")

    await channel.send(embed=embed)

# Role deleted log embed 💬
@bot.event
async def on_guild_role_delete(role):
    channel = await role_get_logging_channel(role.guild)
    if channel is None:
        print("Unable to find channel.")
        return

    embed = discord.Embed(
        title="Role Deleted!",
        description=f"The role **{role.name}** has sucessfully been deleted.",
        color=discord.Color.red(),
        timestamp=datetime.datetime.now()
    )

    embed.set_author(name=f"{bot.user.name} | Logging", icon_url=bot.user.avatar)
    embed.set_footer(text=f"Role Deleted | {bot.user.name}🐈")

    await channel.send(embed=embed)


# Role updated log embed 💬
@bot.event
async def on_guild_role_update(before, after):
    channel = await role_get_logging_channel(before.guild)
    if channel is None:
        print("Unable to find channel.")
        return

    embed = discord.Embed(
        title="Role Updated!",
        description=f"The role **{before.name}** has successfully been updated.",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )

    # Check if there are any differences between the before and after roles
    if before.name != after.name or before.color != after.color or before.hoist != after.hoist or before.mentionable != after.mentionable:
        before_value = ""
        after_value = ""

        # Collecting Before/After Values
        if before.name != after.name:
            before_value += f"> Name: **{before.name}**"
            after_value += f"> Name: **{after.name}**"

        if before.color != after.color:
            before_value += "\n"f"> Color: **{before.color}**"
            after_value += "\n"f"> Color: **{after.color}**"

        if before.hoist != after.hoist:
            before_value += "\n"f"> Is Hoist: **{before.hoist}**"
            after_value += "\n"f"> Is Hoist: **{after.hoist}**"

        if before.mentionable != after.mentionable:
            before_value += "\n"f"> Is Mentionable: **{before.mentionable}**"
            after_value += "\n"f"> Is Mentionable: **{after.mentionable}**"

        embed.add_field(name="Before", value=before_value, inline=False)
        embed.add_field(name="After", value=after_value, inline=False)

        embed.set_author(name=f"{bot.user.name} | Logging", icon_url=bot.user.avatar)
        embed.set_footer(text=f"Role Update | {bot.user.name}🐈")

        await channel.send(embed=embed)


# - - - - - - - - - - - - - - - - 

# Message edit log embed 💬
@bot.event
async def on_message_edit(before, after):
    if before.content != after.content:
        channel = await history_get_logging_channel(before.guild)
        if channel is not None:
            embed = discord.Embed(
                title="Message Edited!",
                description=f"{before.author.mention}'s message was edited in {before.channel.mention}. \n Here are some details about the message.",
                color=discord.Color.dark_magenta(),
                timestamp=datetime.datetime.now()
            )
            embed.set_author(name=f"{bot.user.name} 🐈 | Logging", icon_url=bot.user.avatar)
            embed.add_field(name="Original Content", value=str(before.content), inline=True)
            embed.add_field(name="Edited Content", value=str(after.content), inline=True)
            for attachment in before.attachments:
                embed.add_field(name="Attachment", value=attachment.url, inline=False)
            embed.set_footer(text=f"Message Edited | {bot.user.name}🐈")
            await channel.send(embed=embed)

# message delete log embed 💬
@bot.event
async def on_message_delete(message):
    if message.guild is None:
        return
    channel = await history_get_logging_channel(message.guild)
    if channel is not None:
        embed = discord.Embed(
            title="Message Deleted!",
            description=f"{message.author.mention}'s message was deleted in {message.channel.mention}. \n Here is some information about the message.",
            color=discord.Color.dark_red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{bot.user.name} 🐈 | Logging", icon_url=bot.user.avatar)
        embed.add_field(name="Deleted Content", value=message.content, inline=False)
        embed.set_footer(text=f"Message Deleted | {bot.user.name}🐈")
        await channel.send(embed=embed)

# - - - - - - - - - - - - - - - - 





# - - - - - - - - - - - 

# Define a helper function to get the entrance logging channel object 🔗
async def entrance_get_logging_channel(guild):
    channel = guild.get_channel(entrance_logging_channel_id)
    return channel


# Define a helper function to get the role logging channel object 🔗
async def role_get_logging_channel(guild):
    channel = guild.get_channel(role_logging_channel_id)
    print(channel)
    return channel

# Define a helper function to get the history logging channel object 🔗
async def history_get_logging_channel(guild):
    channel = guild.get_channel(history_logging_channel_id)
    return channel

async def moderation_get_logging_channel(guild):
    channel = guild.get_channel(moderation_logging_channel_id)
    return channel

# Define a helper function to get the feedback logging channel object 🔗
async def feedback_get_logging_channel(guild):
    channel = guild.get_channel(feedback_logging_channel_id)
    return channel


async def support_get_logging_channel(interaction: discord.Interaction, bot):

    if interaction.guild:
        channel = discord.utils.get(interaction.guild._channels, id=support_logging_channel_id)
    else:
        channel = await bot.fetch_channel(support_logging_channel_id)

    return channel



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# ==========================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



# Bot Commands Permissions Access 🔑

# Define access ids for each role
OWNERSHIP_ACCESS_ID = 4
ADMIN_ACCESS_ID = 3
MODERATION_ACCESS_ID = 2
MEMBERSHIP_ACCESS_ID = 1
GLOBAL_ACCESS_ID = 0

OWNERSHIP_ACCESS_ROLE = "<@&1069003717417902210>"
ADMIN_ACCESS_ROLE = "<@&1074620244699648030>"
MODERATION_ACCESS_ROLE = "<@&1078373457366102128>"
MEMBERSHIP_ACCESS_ROLE = "<@&1069003932363391016>"
GLOBAL_ACCESS_ROLE = "<@&1069000601318457415>"


# Define a sample list of user roles and their associated access ids
role_access_map = [
    {"role_id": 1069003717417902210, "access_id": OWNERSHIP_ACCESS_ID},
    {"role_id": 1074620244699648030, "access_id": ADMIN_ACCESS_ID},
    {"role_id": 1078373457366102128, "access_id": MODERATION_ACCESS_ID},
    {"role_id": 1069003932363391016, "access_id": MEMBERSHIP_ACCESS_ID},
    {"role_id": 1069000601318457415, "access_id": GLOBAL_ACCESS_ID}
]

# Define a dictionary that maps command names to their required access ids 📕
command_access = {
    "hello": MEMBERSHIP_ACCESS_ID,
    "ping": MEMBERSHIP_ACCESS_ID,
    "commands": MEMBERSHIP_ACCESS_ID,
    "info": MEMBERSHIP_ACCESS_ID,
    "product": MEMBERSHIP_ACCESS_ID,
    "purge": ADMIN_ACCESS_ID,
}

# Define a function that checks if a user has the required access id to execute a command 🔓
def has_access(user_roles, required_access: int) -> bool:
    max_access = max([role["access_id"] for role in user_roles], default=0)
    return max_access >= required_access


# Require Access for Application Commands
def requires_access(required_access):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(interaction: discord.Interaction, *args, **kwargs):
            
            user_roles = [{"role_id": role.id, "access_id": next((item["access_id"] for item in role_access_map if item["role_id"] == role.id), 0)} for role in interaction.user.roles]

            if has_access(user_roles, required_access):
                await func(interaction, *args, **kwargs)
            else:
                for role in role_access_map:
                    if role["access_id"] == required_access:
                        REQUIRED_ROLE = f"<@&{role['role_id']}>"
                        break
                error_embed = creating_error_embed()
                error_embed.title = f"Access Denied! {ERROR_EMOJI}"
                error_embed.description = f"You are not eligible to use this command. \n You need the role of {REQUIRED_ROLE} to access to this command."
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
               
        return wrapper
    return decorator


# Require Access for Context Commands
def requires_access2(required_access):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs):
            global REQUIRED_ROLE
            
            user_roles = [{"role_id": role.id, "access_id": next((item["access_id"] for item in role_access_map if item["role_id"] == role.id), 0)} for role in ctx.author.roles]

            if has_access(user_roles, required_access):
                await func(ctx, *args, **kwargs)
            else:
                for role in role_access_map:
                    if role["access_id"] == required_access:
                        REQUIRED_ROLE = f"<@&{role['role_id']}>"
                        break
                error_embed = creating_error_embed()
                error_embed.title = f"Access Denied! {ERROR_EMOJI}"
                error_embed.description = f"You are not eligible to use this command. \n You need the role of {REQUIRED_ROLE} to access to this command."
                await ctx.reply(embed=error_embed, mention_author=False)
               
        return wrapper
    return decorator

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# ==========================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Defualt Embeds 💬

# Creating a defualt loading embed 🔃
def creating_loading_embed():
    # Create the loading message embed
    loading_embed = discord.Embed(
    title=f"Processing {PROCESSING_EMOJI}",
    color=0x99958E,
    description="Please wait a few more moments...",
    timestamp=datetime.datetime.now(),
    )
    loading_embed.set_author(name=bot.user.name + '🐕 | Processing', icon_url=bot.user.avatar)
    loading_embed.set_footer(text=f"Processing | {bot.user.name}🐕")
    return loading_embed


# Creating a defualt  error embed ❌
def creating_error_embed():
    error_embed = discord.Embed(
    title=f"Error has occurred! {ERROR_EMOJI}",
    color=0x99958E,
    description="You are not eligible to use this command.",
    timestamp=datetime.datetime.now(),
    )
    error_embed.set_author(name=bot.user.name + '🐈 | Error', icon_url=bot.user.avatar)
    error_embed.set_footer(text=f"Error | {bot.user.name}🐈")
    return error_embed

# Creatying a defulat sucess embed ✅
def creating_sucess_embed():
    sucess_embed = discord.Embed(
        title=f"Sucess! {SUCCESS_EMOJI}",
        color=0x99958E,
        description="The action has successfully been made!",
        timestamp=datetime.datetime.now(),
    )
    sucess_embed.set_author(name=bot.user.name + '🐈 | Sucess' , icon_url=bot.user.avatar)
    sucess_embed.set_footer(text=f"Sucess | {bot.user.name}🐈")
    return sucess_embed



# Commands Errors Embed - Application Commands ⚠️
@bot.tree.error
async def on_slash_command_error(interaction: discord.Interaction, error: commands.CommandError):
    error_embed = creating_error_embed()

    if isinstance(error, app_commands.CommandOnCooldown):
        # Command Cooldown
        retry_after = int(error.retry_after)
        cooldown_timestamp = datetime.datetime.now() + datetime.timedelta(seconds=retry_after)
        epoch_time = int(cooldown_timestamp.timestamp())
        command_name = interaction.data["name"]
        user_id = interaction.user.id

        error_embed.title = f"Too fast! {COOLDOWN_EMOJI} "
        error_embed.description = f"This command is on cooldown. \n Please try again <t:{epoch_time}:R>"

        # Send the initial embed message
        message = await interaction.response.send_message(embed=error_embed, ephemeral=True)

        # Create a task to delete the message after the cooldown
        async def delete_message():
            await asyncio.sleep(retry_after - 1) # Remove 1 second before the cooldown finished
            await interaction.delete_original_response()

        # Schedule the task
        asyncio.create_task(delete_message())

    else:
        error_embed.title = f"Error has occured! {ERROR_EMOJI} "
        error_embed.description = f"An error occurred while executing the command. \n Please report to <@497810250175348746> about the case."
        error_embed.add_field(name="Error", value=f"`{error}`", inline=False)
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
        print(f"{error}")


# Bot Commands Errors Embed - Context Commands ⚠️
@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    error_embed = creating_error_embed()

    if isinstance(error, commands.CommandOnCooldown):
        # Command Cooldown
        retry_after = int(error.retry_after)
        cooldown_timestamp = datetime.datetime.now() + datetime.timedelta(seconds=retry_after)
        epoch_time = int(cooldown_timestamp.timestamp())
        command_name = ctx.command.name
        user_id = ctx.author.id

        error_embed.title = f"Too fast! {COOLDOWN_EMOJI} "
        error_embed.description = f"This command is on cooldown. \n Please try again <t:{epoch_time}:R>"

        # Send the initial embed message
        message = await ctx.reply(embed=error_embed, mention_author=False)

        # Create a task to delete the message after the cooldown
        async def delete_message():
            await asyncio.sleep(retry_after - 1) # Remove 1 second before the cooldown finished
            await message.delete()

        # Schedule the task
        asyncio.create_task(delete_message())

    elif isinstance(error, commands.CommandNotFound):
        error_embed.title = f"Command Error! {ERROR_EMOJI} "
        error_embed.description = f"The command you entered does not exist. \n Please use the correct command name or check for spelling mistakes."
        await ctx.reply(embed=error_embed, mention_author=False)

    else:
        error_embed.title = f"Error has occured! {ERROR_EMOJI} "
        error_embed.description = f"An error occurred while executing the command. \n Please report to <@497810250175348746> about the case."
        error_embed.add_field(name="Error", value=f"`{error}`", inline=False)
        await ctx.reply(embed=error_embed, mention_author=False)
        print(f"{error}")



"""
class PersistentView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Green', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('This is green.', ephemeral=True)


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def setup_hook(self) -> None:
        # Register the persistent view for listening here.
        # Note that this does not send the view to any message.
        # In order to do this you need to first send a message with the View, which is shown below.
        # If you have the message_id you can also pass it as a keyword argument, but for this example
        # we don't have one.
        self.add_view(PersistentView())
"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# ==========================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Application Commands ⚙️
tree = bot.tree.command
arguments = app_commands.describe
access = requires_access
choices = app_commands.choices
cooldown = app_commands.checks.cooldown

#  Applications Menu 🍴
tree_menu = bot.tree.context_menu


# Context Commands 💬
context_command = bot.command
access2 = requires_access2


 #1. hello world 👋🏼
@tree(name="hello", description=f"Hello World! 👋🏼")
@cooldown(1, 60.0, key=lambda i: (i.guild_id, i.user.id))
@access(MEMBERSHIP_ACCESS_ID)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey there! Welcome to Kindle Pets! {random.choice(EMOJIS)}", ephemeral=True)



#2. Command for checking the bot's speed ping 🔨
@tree(name="ping", description="Test your network connection latency 🔨")
@cooldown(2, 60.0, key=lambda i: str(i.user.id))
@access(MEMBERSHIP_ACCESS_ID)
async def ping(interaction: discord.Interaction): 
    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title=f"Success! {random.choice(EMOJIS)}",
        color=0x99958E,
        timestamp=datetime.datetime.utcnow(),
    )
    embed.set_author(name=f"{bot.user.name} 🐈", icon_url=bot.user.avatar)
    embed.add_field(name="Time", value=f"{latency} ms", inline=False)
    embed.set_footer(text=f"Success | {bot.user.name} 🐈")

    await interaction.response.send_message(embed=embed, ephemeral=True)
 
#3. Command for info for all the commands of the bot 📄
@tree(name="commands", description="Displays a list of all the available commands of the bot 📄")
@cooldown(1, 60.0, key=lambda i: str(i.user.id))
@access(GLOBAL_ACCESS_ID)
async def command(interaction: discord.Interaction):

    # Send the loading message
    await interaction.response.defer(ephemeral=True)
    #loading_embed = creating_loading_embed()
    #loading_embed = await interaction.response.send_message(embed=loading_embed, ephemeral=True)
    

    #Embed 1
     # Create an embed with the specified information
    first_commands_embed = discord.Embed(color=0x99958E, title = "Information Commands", description=f"Commands for helpful information and tools \n Access Required: {MEMBERSHIP_ACCESS_ROLE}", timestamp=datetime.datetime.now())
    first_commands_embed.set_author(name=f"{bot.user.name}🐈 | Commands", icon_url=bot.user.avatar)
    first_commands_embed.set_footer(text=f"Information Commands | {bot.user.name}🐈")
    

    # List of available commands in the bot
    first_commands = {
   "Information": {
            "</hello:1078443078416871526>": f"{hello.description}",
            "</commands:1074485566730686644>": f"{command.description}",
            "</info:1088814510569181304>": f"{info.description}"
       },
        "Utility": {
            "</ping:1074474588265787443>": f"{ping.description}",
            #"</verify:1091887102221889580>" : f"{verify.description}",
            "</product:1078085606120366280>" : f"{product.description}",
            "</purge:1078066999994896416>": f"{purge_command.description}",
            "</feedback:1091496743675367474>": f"{feedback.description}",
            "</ticket:1092482493309005894>": f"{ticket.description}",
        },
    }


    #Embed 2
     # Create an embed with the specified information
    second_commands_embed = discord.Embed(color=0x99958E, title = "Database Commands", description=f"Commands for configuration data within the server \n Access Required: {ADMIN_ACCESS_ROLE}", timestamp=datetime.datetime.now())
    second_commands_embed.set_author(name=f"{bot.user.name}🐈 | Commands", icon_url=bot.user.avatar)
    second_commands_embed.set_footer(text=f"Database Commands | {bot.user.name}🐈")

        # List of available commands in the bot
    second_commands = {
        "Configuration": {
        "</set_entrance:1087179706375340104>": f"{set_entrance_logging_channel.description}",
        "</set_roleupdate:1087179706375340105>": f"{set_role_logging_channel.description}",
        "</set_history:1087179706375340106>": f"{set_history_logging_channel.description}",
        "</set_moderation:1087361205301166110>": f"{set_moderation_logging_channel.description}",
        "</set_feedback:1091492088861966388>": f"{set_feedback_logging_channel.description}",
       },

    }
    
    # Add fields to first_commands_embed
    for category, cmds in first_commands.items():
        cmd_list = "\n".join([f"{cmd} - {desc}" for cmd, desc in cmds.items()])
        first_commands_embed.add_field(name=category, value=cmd_list, inline=False)

    # Add fields to second_commands_embed
    for category, cmds in second_commands.items():
        cmd_list = "\n".join([f"{cmd} - {desc}" for cmd, desc in cmds.items()])
        second_commands_embed.add_field(name=category, value=cmd_list, inline=False)


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Saving all the embeds in a variable
    embeds = [first_commands_embed,second_commands_embed]

    # Set the initial page to the first embed
    current_page = 0

    view = View()

    # Create the buttons
    first_button = discord.ui.Button(label="First", custom_id="first", style=discord.ButtonStyle.blurple, emoji=f"{ID_EMOJI}", disabled=True)
    back_button = discord.ui.Button(label="Back", custom_id="back", style=discord.ButtonStyle.red, disabled=True)
    forward_button = discord.ui.Button(label="Forward", custom_id="forward", style=discord.ButtonStyle.green)
    last_button = discord.ui.Button(label="Last", custom_id="last", style=discord.ButtonStyle.blurple)

    view.add_item(first_button)
    view.add_item(back_button)
    view.add_item(forward_button)
    view.add_item(last_button)
    

    # Create the message with the initial embed and buttons
    message = await interaction.followup.send(embed=embeds[current_page], view=view)

    # Define the button callback function
    async def button_callback(interaction: discord.Interaction):
        nonlocal current_page

        if interaction.data["custom_id"] == "first":
            current_page = 0
        elif interaction.data["custom_id"] == "back":
            current_page -= 1
        elif interaction.data["custom_id"] == "forward":
            current_page += 1
        elif interaction.data["custom_id"] == "last":
            current_page = len(embeds) - 1

        # Disable/enable buttons as needed
        first_button.disabled = (current_page == 0)
        back_button.disabled = (current_page == 0)
        forward_button.disabled = (current_page == len(embeds) - 1)
        last_button.disabled = (current_page == len(embeds) - 1)

        # Update the message with the new embed and buttons
        await interaction.response.edit_message(embed=embeds[current_page], view=view)



    # Add the button callback to the buttons
    for button in [first_button, back_button, forward_button, last_button]:
        button.callback = button_callback


""""
# Help Command ❔
@tree(name="help", description="Helping you with any question you may have")
async def help(interaction: discord.Interaction):
    # Create a list of embeds for the pages
    embeds = [
        discord.Embed(title="Bot Help #1", description="Use the buttons below to navigate between help pages"),
        discord.Embed(title="Bot Help #2", description="This is the second page of help"),
        discord.Embed(title="Bot Help #3", description="This is the third page of help"),
        discord.Embed(title="Bot Help #4", description="This is the fourth and final page of help"),
    ]
    # Set the initial page to the first embed
    current_page = 0

    view = View()

    # Create the buttons
    first_button = discord.ui.Button(label="First", custom_id="first", style=discord.ButtonStyle.blurple, emoji=f"{ID_EMOJI}", disabled=True)
    back_button = discord.ui.Button(label="Back", custom_id="back", style=discord.ButtonStyle.red, disabled=True)
    forward_button = discord.ui.Button(label="Forward", custom_id="forward", style=discord.ButtonStyle.green)
    last_button = discord.ui.Button(label="Last", custom_id="last", style=discord.ButtonStyle.blurple)

    view.add_item(first_button)
    view.add_item(back_button)
    view.add_item(forward_button)
    view.add_item(last_button)

    # Create the message with the initial embed and buttons
    message = await interaction.response.send_message(embed=embeds[current_page], view=view)

    # Define the button callback function
    async def button_callback(interaction: discord.Interaction):
        nonlocal current_page

        if interaction.data["custom_id"] == "first":
            current_page = 0
        elif interaction.data["custom_id"] == "back":
            current_page -= 1
        elif interaction.data["custom_id"] == "forward":
            current_page += 1
        elif interaction.data["custom_id"] == "last":
            current_page = len(embeds) - 1

        # Disable/enable buttons as needed
        first_button.disabled = (current_page == 0)
        back_button.disabled = (current_page == 0)
        forward_button.disabled = (current_page == len(embeds) - 1)
        last_button.disabled = (current_page == len(embeds) - 1)

        # Update the message with the new embed and buttons
        await interaction.response.edit_message(embed=embeds[current_page], view=view)



    # Add the button callback to the buttons
    for button in [first_button, back_button, forward_button, last_button]:
        button.callback = button_callback

"""


#4. Command for info for all the important info within the server 🪪
@tree(name="info", description=f"Displays a technical information regarding the server 🪪")
@cooldown(1, 60.0, key=lambda i: str(i.user.id))
@access(MEMBERSHIP_ACCESS_ID)
async def info(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.edit_original_response("This command can only be used in a server context.")

    server = interaction.guild
    if not server:
            return await interaction.edit_original_response("Unable to retrieve server information.")


    # Send the loading message
    loading_embed = creating_loading_embed()
    loading_embed = await interaction.response.send_message(embed=loading_embed, ephemeral=True)

    icon_url = server.icon.url if server.icon else None


    # Fetch server information
    owner = server.owner.mention
    admins = sum(member.guild_permissions.administrator for member in server.members)
    roles = len(server.roles)
    icon_url = server.icon.url if server.icon else None

    # Calculate server age
    server_age = (datetime.datetime.now(datetime.timezone.utc) - server.created_at).days
    server_age_str = f"{server_age} days" if server_age else "Unknown"


    # Create the main embed with server information
    main_embed = discord.Embed(title="Server Information", color=0x99958E, timestamp=datetime.datetime.now())
    main_embed.set_thumbnail(url=icon_url)
    main_embed.set_author(name=bot.user.name + '🐈 | Information', icon_url=bot.user.avatar)
    main_embed.set_footer(text=f"{main_embed.title} | {bot.user.name}🐈")

    #  Add fields to the main embed
    main_embed.add_field(name="Owner", value=owner, inline=True)
    main_embed.add_field(name="Admins", value=admins, inline=True)
    main_embed.add_field(name="Roles", value=roles, inline=True)
    main_embed.add_field(name="Server Age", value=server_age_str, inline=True)
    main_embed.add_field(name="Prefix", value=f"`{bot.command_prefix}`", inline=True)


    # Adding Channel Count field to the embed
    text_channels_count = len(server.text_channels)
    voice_channels_count = len(server.voice_channels)
    fourm_channels_count = len(server.forums)

    locked_text_channels_count = 0
    locked_voice_channels_count = 0
    locked_fourm_channels_count = 0

    for channel in server.text_channels:
     if not channel.permissions_for(interaction.user).read_messages:
        locked_text_channels_count += 1

    for channel in server.voice_channels:
     if not channel.permissions_for(interaction.user).connect:
        locked_voice_channels_count += 1

    for channel in server.forums:
     if not channel.permissions_for(interaction.user).connect:
        locked_fourm_channels_count += 1

    text_channels_info = f"Text: {text_channels_count} ({locked_text_channels_count} locked for you)" if locked_text_channels_count > 0 else f"Text: {text_channels_count} (full access)"
    voice_channels_info = f"Voice: {voice_channels_count} ({locked_voice_channels_count} locked for you)" if locked_voice_channels_count > 0 else f"Voice: {voice_channels_count} (full access)"
    fourm_channels_info = f"Fourm: {fourm_channels_count} ({locked_fourm_channels_count} locked for you)" if locked_fourm_channels_count > 0 else f"Fourm: {fourm_channels_count} (full access)"
    main_embed.add_field(name="Channels", value=f"{text_channels_info}\n{voice_channels_info}\n{fourm_channels_info}", inline=True)

    # Adding Member Count and Bot Count field to the embed
    total_count = server.member_count

    human_count = 0
    bot_count = 0

    for member in server.members:
        if not member.bot:
            human_count += 1
        else:
            bot_count += 1

    main_embed.add_field(name="Members", value=f"Total: {total_count}\nHumans: {human_count}\nBots: {bot_count}", inline=True)

    if server.text_channels:
    # Finding the most active text channel
        most_active_channel = None
        most_messages = 0
        for channel in server.text_channels:
            count = 0
            async for message in channel.history(limit=None):
                if not message.author.bot:
                    count += 1
            if count > most_messages:
                most_messages = count
                most_active_channel = channel
        if most_active_channel:
            main_embed.add_field(name="Most Active", value=most_active_channel.mention, inline=True)
  



    if server.text_channels:
    # Get the list of members and their message counts
        top_members = []
    cache = {}
    for channel in server.text_channels:
        async for message in channel.history(limit=None):
            if message.author.id not in cache:
                cache[message.author.id] = 0
            cache[message.author.id] += 1

    for member_id, count in cache.items():
        member = server.get_member(member_id)
        if member and not member.bot and count > 0:
            top_members.append((member, count))

    # Sort the list of top members
    top_members.sort(key=lambda x: x[1], reverse=True)
    top_members = top_members[:3]

    # Create the top members string
    top_members_str = "\n".join([f"{i+1}. {member.mention} ({count})" for i, (member, count) in enumerate(top_members)])

    # Adding the most active members within the server
    main_embed.add_field(name="Top Members", value=top_members_str, inline=True)

    await interaction.edit_original_response(embed=main_embed)




    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


#5. Command for getting product information 📦
@tree(name="product", description="Select the current avilable products within the online Shop 📦")
@cooldown(2, 60.0, key=lambda i: str(i.user.id))
@arguments(category ="Type of category")
@choices(category = [
    Choice(name= "Cats", value="cats"),
    Choice(name= "Dogs", value="dogs")
])
@access(MEMBERSHIP_ACCESS_ID)
async def product(interaction: discord.Interaction, category: str):

    # Send the loading message
    await interaction.response.defer(ephemeral=True)
    #loading_embed = creating_loading_embed()
    #loading_message = await interaction.response.send_message(embed=loading_embed, ephemeral=False)


    if category.lower() == "cats":
        category_url = "https://kindlepets-online.myshopify.com/collections/cats"
        category_name = "Cats"
        category_icon = "https://i.imgur.com/HbI73VC.png"
        category_emoji = "🐱"
    elif category.lower() == "dogs":
        category_url = "https://kindlepets-online.myshopify.com/collections/dogs"
        category_name = "Dogs"
        category_icon = "https://i.imgur.com/hYNlW1A.png"
        category_emoji = "🐶"
    else:
        error_embed = creating_error_embed()
        error_embed.description("Invalid category. \n Please choose either ` cats ` or ` dogs `")
        await interaction.followup.send(embed=error_embed, ephemeral=True)
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(category_url) as resp:
            soup = BeautifulSoup(await resp.text(), 'html.parser')
            product_list = soup.find_all('div', class_='grid-product__content')
            products = []
            for product in product_list:
                name = product.find('a', class_='grid-product__title').text.strip()
                link = "https://kindlepets-online.myshopify.com" + product.find('a', class_='grid-product__title')['href']
                description = product.find('div', class_='grid-product__description').text.strip()
                products.append((name, link, description))

    # Create embed
    embed = discord.Embed(title=f"Success! {category_emoji}", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
    embed.set_author(name=f"{bot.user.name} 🐈 | Product", icon_url=bot.user.avatar)
    embed.description = f"Here are the products in the {category_name} category:"
    for name, link, description in products:
        embed.add_field(name=name, value=f"{description}\n[Product link]({link})")

    # Add thumbnail and timestamp to embed
    embed.set_thumbnail(url=category_icon)
    embed.set_footer(text=f"Success | {bot.user.name} 🐈")

    # Send the embed as a response to the interaction
    await interaction.followup.send(embed=embed)


#6. Command for purging messages 🚚
@tree(name="purge", description="Delete a specified number of messages from a user 🚚")
@cooldown(2, 60.0, key=lambda i: str(i.user.id))
@arguments(target="Which person do you want to make the purge?", messages="Amount of messages to be deleted")
@access(MODERATION_ACCESS_ID)
async def purge_command(interaction: discord.Interaction, target: discord.Member, messages: int):
    await interaction.response.defer(ephemeral=True)

    success_embed = creating_sucess_embed()
    error_embed = creating_error_embed()

    if messages >= 101:
        error_embed.description = "Purge action cannot be more than 100 messages"
        await interaction.followup.send(embed=error_embed, ephemeral=True)
        return

    channel = interaction.channel

    def check(message):
        return message.author == target

    if messages <= 100:
        deleted_messages = await channel.purge(limit=messages, check=check)
    else:
        deleted_messages = await channel.purge(limit=messages)

    if not deleted_messages:
        error_embed.description = f"No messages were purged. {target.mention} didn't send any messages on {channel.mention}."
        await send_response(interaction, error_embed)
        return

    success_embed.description = f"Successfully removed {len(deleted_messages)} messages from {target.mention}."
    success_embed.set_author(name=bot.user.name + '🐈 | Processing', icon_url=bot.user.avatar)
    await send_response(interaction, success_embed)

async def send_response(interaction, embed):
    await interaction.followup.send(embed=embed, ephemeral=True)


#7. Command for sending a feedback modal 🌟
@tree(name="feedback", description="Give us a feedback! 🌟")
@cooldown(1, 120.0, key=lambda i: str(i.user.id))
@access(MEMBERSHIP_ACCESS_ID)
async def feedback(interaction: discord.Interaction):
    await interaction.response.send_modal(Community_Feedback())


# Step 1: Picking the type of ticket
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="How may I help you?",
        options=[
            SelectOption(label="Support", emoji=f"{SEARCH_EMOJI}", description="Create a Support Ticket", value="support", ),
            SelectOption(label="Report", emoji=f"{WARNING_EMOJI}", description="Create a Report Ticket", value="report"),
        ], custom_id="view selection"
         
    )

    async def support_callback(self, interaction: discord.Interaction, select: ui.select):
        if select.values[0] == "support":
            await interaction.response.send_modal(SupportSystem(bot))
        elif select.values[0] == "report":
            await interaction.response.send_message(f"**{PROCESSING_EMOJI} This modal is currently under construction.**", ephemeral=True)
            await asyncio.sleep(5)
            await interaction.delete_original_response()

    #async def on_timeout(self, interaction):
       #self.children[0].disabled = True
       #await interaction.delete_original_response()      

"""
# Step 2: Creating a modal to support ticket and a channel
class SupportSystem(Modal, title="Support Form"):
    def __init__(self):
        super().__init__(timeout=None)

  
    text = ui.TextInput
    
    issue = text(label="Please describe your issue", style=discord.TextStyle.paragraph, placeholder="Explain your issue", required=True, max_length=200, custom_id="issue")
    notes = text(label="Notes", style=discord.TextStyle.long, placeholder="Notes to add", required=False ,max_length=100, custom_id="notes")

    async def on_submit(self, interaction: discord.Interaction):
        modal_sent = datetime.datetime.utcnow()
        modal_unix = int((modal_sent - datetime.datetime(1970, 1, 1)).total_seconds())
        
        # Create new support channel
        support_category = bot.get_channel(1092255747368308776)
        support_channels = [channel.name for channel in support_category.text_channels if "support" in channel.name.lower()]
        channel_count = len(support_channels) + 1
        channel_name = f"support・{channel_count}"
        channel_description = f"**{SEARCH_EMOJI} Support Ticket \n • Created by: {interaction.user.mention}  \n  • Issue: '{self.issue.value}**'"
        support_channel = await interaction.guild.create_text_channel(channel_name, category=support_category, topic=channel_description)

        # Add permissions to user who submitted the form
        await support_channel.set_permissions(interaction.user, read_messages=True, send_messages=True, read_message_history=True)

        # Create embed message
        ticket_embed = discord.Embed(
            title=f"New Ticket Created! 🎫",
            description=f"The user {interaction.user.mention} has an issue need to be handeled! \n The form has been sent <t:{modal_unix}:R>.",
            color=discord.Color.light_gray(),
            timestamp=datetime.datetime.now()
        )
        ticket_embed.add_field(name=f"{self.issue.label}", value=f"```{self.issue.value}```", inline=False)
        if self.notes.value == "":
            ticket_embed.add_field(name=f"{self.notes.label}", value=f"```No Data```", inline=False)
        else:
            ticket_embed.add_field(name=f"{self.notes.label}", value=f"```{self.notes.value}```", inline=False)
        ticket_embed.set_author(name=f"{bot.user.name} 🐈 | Support Ticket", icon_url=bot.user.avatar)
        ticket_embed.set_footer(text=f"Sent by {interaction.user.name} | {bot.user.name}🐈")

        # Get the user who submitted the form
        user = interaction.user

        # Get the staff team role by ID
        staff_role = interaction.guild.get_role(1074620244699648030)

        bot = PersistentViewBot(user, interaction, support_channel, channel_name, staff_role, self.issue, self.notes, None)

        # Creating a new view with the custom view "TicketHandler"
        view = TicketHandler(bot.user, bot.interaction, bot.support_channel, bot.channel_name, bot.staff_role, bot.issue, bot.notes, None)

        # Send the embed form to the new support channel 
        await support_channel.send(f"{user.mention}, {staff_role.mention}, a new ticket has been opened!",embed=ticket_embed, view=view)

        # Send response to user
        await interaction.response.send_message(f"**{SUCCESS_EMOJI} You have successfully submitted the form! \n Please go to: <#{support_channel.id}>**", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.delete_original_response()
"""

class SupportSystem(Modal, title="Support Form"):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

  
    text = ui.TextInput
    
    issue = text(label="Please describe your issue", style=discord.TextStyle.paragraph, placeholder="Explain your issue", required=True, max_length=200, custom_id="issue")
    notes = text(label="Notes", style=discord.TextStyle.long, placeholder="Notes to add", required=False ,max_length=100, custom_id="notes")

    async def on_submit(self, interaction: discord.Interaction):
        modal_sent = datetime.datetime.utcnow()
        modal_unix = int((modal_sent - datetime.datetime(1970, 1, 1)).total_seconds())
        
        # Create new support channel
        support_category = self.bot.get_channel(1092255747368308776)
        support_channels = [channel.name for channel in support_category.text_channels if "support" in channel.name.lower()]
        channel_count = len(support_channels) + 1
        channel_name = f"support・{channel_count}"
        channel_description = f"**{SEARCH_EMOJI} Support Ticket \n • Created by: {interaction.user.mention}  \n  • Issue: '{self.issue.value}**'"
        support_channel = await interaction.guild.create_text_channel(channel_name, category=support_category, topic=channel_description)

        # Add permissions to user who submitted the form
        await support_channel.set_permissions(interaction.user, read_messages=True, send_messages=True, read_message_history=True)

        # Create embed message
        ticket_embed = discord.Embed(
            title=f"New Ticket Created! 🎫",
            description=f"The user {interaction.user.mention} has an issue need to be handeled! \n The form has been sent <t:{modal_unix}:R>.",
            color=discord.Color.light_gray(),
            timestamp=datetime.datetime.now()
        )
        
        ticket_embed.add_field(name=f"{self.issue.label}", value=f"```{self.issue.value}```", inline=False)
        if self.notes.value == "":
            ticket_embed.add_field(name=f"{self.notes.label}", value=f"```No Data```", inline=False)
        else:
            ticket_embed.add_field(name=f"{self.notes.label}", value=f"```{self.notes.value}```", inline=False)
        ticket_embed.set_author(name=f"{self.bot.user.name} 🐈 | Support Ticket", icon_url=self.bot.user.avatar)
        ticket_embed.set_footer(text=f"Sent by {interaction.user.name} | {self.bot.user.name}🐈")

        # Get the user who submitted the form
        username = interaction.user

        # Get the staff team role by ID
        staff_role = interaction.guild.get_role(1074620244699648030)

        print("-------------------------------------")

        print(username)

        save_ticket_args(username, support_channel, staff_role, channel_name, self.issue, self.notes)

        view = TicketHandler(username, support_channel, staff_role, channel_name, self.issue, self.notes)

        await self.bot.add_ticket_handler(username, support_channel, staff_role, channel_name, self.issue, self.notes)

        await support_channel.send(f"{username.mention}, {staff_role.mention}, a new ticket has been opened!", embed=ticket_embed, view=view)

        # Send response to user
        await interaction.response.send_message(f"**{SUCCESS_EMOJI} You have successfully submitted the form! \n Please go to: <#{support_channel.id}>**", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.delete_original_response()



class TicketHandler(View):
    def __init__(self, username, support_channel, staff_role, channel_name, issue, notes):
        super().__init__(timeout=None)
        self.support_channel = support_channel
        self.username = username
        self.staff = staff_role
        self.channel_name = channel_name
        self.issue = issue
        self.notes = notes
        
        print(f"inside TicketHandler {username}")
    

    @discord.ui.button(label="Close Ticket", style=ButtonStyle.grey, custom_id="close ticket")
    async def closeticket_callback(self, interaction:discord.Interaction, button):

        full_access = interaction.guild.get_role(1069003717417902210)
        user_roles = interaction.user.roles
        print()
        if self.staff in user_roles or full_access in user_roles: #If one of the members have the 'Staff Roles' or if the owner has the owner role.
            await interaction.response.send_modal(ClosingTicket(self.username, self.support_channel, self.channel_name, self.issue, self.notes))
        else:
            await interaction.response.send_message(f"**{ERROR_EMOJI} You don't have permission to use this button!**", ephemeral=True)
            await asyncio.sleep(5)
            await interaction.delete_original_response()

"""
class TicketHandler(View):
    def __init__(self, username, support_channel, staff_role, channel_name, issue, notes):
        super().__init__(timeout=None)
        self.support_channel = support_channel
        self.username = username
        self.staff = staff_role
        self.channel_name = channel_name
        self.issue = issue
        self.notes = notes
        

    @discord.ui.button(label="Close Ticket", style=ButtonStyle.grey, custom_id="close ticket")
    async def closeticket_callback(self, interaction:discord.Interaction, button):

        full_access = interaction.guild.get_role(1069003717417902210)
        user_roles = interaction.user.roles
        if self.staff in user_roles or full_access in user_roles: #If one of the members have the 'Staff Roles' or if the owner has the owner role.
            await interaction.response.send_modal(ClosingTicket(self.username, self.support_channel, self.channel_name, self.issue, self.notes))

        else:
            await interaction.response.send_message(f"**{ERROR_EMOJI} You don't have permission to use this button!**", ephemeral=True)
 


"""

# Step 4: Sending a Modal to provide a reason for closign ticket
def load_ticket_args():
    try:
        with open("ticket_args.json", "r") as f:
            ticket_args = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    return ticket_args

class ClosingTicket(Modal, title=f"Closing Ticket"):
    def __init__(self, username, support_channel, channel_name, issue, notes):
        super().__init__(timeout=None)

        # Load the stored ticket arguments
        ticket_args = load_ticket_args()

        if ticket_args is not None:
            self.support_channel = support_channel
            self.username = username
            self.channel_name = ticket_args["channel_name"]
            self.issue = ticket_args["issue"]
            self.notes = ticket_args["notes"]
        else:
            self.support_channel = support_channel
            self.username = username
            self.channel_name = channel_name
            self.issue = issue
            self.notes = notes

    text = ui.TextInput
    reason = text(label=f"Reason for closing the ticket", style=discord.TextStyle.long, placeholder="Provide Reason", required=True, max_length=200, custom_id="reason")


    async def on_submit(self, interaction: discord.Interaction):
        print(f"channel: {self.channel_name}")
        await interaction.response.defer()

        # Get the support channel from the view's associated message
        self.support_channel = interaction.channel
            
            # Get the conversation happened in the channel before deleting it
        conversation = ""
        async for message in self.support_channel.history():
            if message.author != interaction.guild.me:
                conversation += f"{message.author.name}: {message.content}\n"
        
        rate_button = RateButton(self.username, self.support_channel, self.channel_name, self.issue, self.notes, self.reason)
            # Delete the support channel
        await interaction.channel.delete()
        
        channel = await support_get_logging_channel(interaction, self.bot)

        
        ticket_counts["support_ticket_count"] += 1

        # Update the feedback counts in the JSON file
        with open("ticket_counts.json", "w") as f:
            json.dump(ticket_counts, f)

        
        ticket_sent = datetime.datetime.utcnow()
        ticket_unix = int((ticket_sent - datetime.datetime(1970, 1, 1)).total_seconds())

        if channel is not None:
                        # Create embed message
                ticket_logging_embed = discord.Embed(
                    title=f"New Support Case! {FILES_EMOJI}",
                    description=f"The user {self.user.mention} created a support ticket handles by {interaction.user.mention} \n The ticket has been closed <t:{ticket_unix}:R>.",
                    color=discord.Color.light_gray(),
                    timestamp=datetime.datetime.now()
                )
                ticket_logging_embed.add_field(name=f"{self.issue.label}", value=f"```{self.issue.value}```", inline=False)
                if self.notes.value == "":
                     ticket_logging_embed.add_field(name=f"{self.notes.label}", value=f"```No Data```", inline=False)
                else:
                     ticket_logging_embed.add_field(name=f"{self.notes.label}", value=f"```{self.notes.value}```", inline=False)
                     
                ticket_logging_embed.add_field(name=f"{self.reason.label}", value=f"```{self.reason}```", inline=True)    

                ticket_logging_embed.set_author(name=f"{bot.user.name} 🐈 | Logging", icon_url=bot.user.avatar)
                ticket_logging_embed.set_footer(text=f"Support Ticket #{ticket_counts['support_ticket_count']} | {bot.user.name}🐈")

                # Sends a new logging message
                await channel.send(embed=ticket_logging_embed)
        

        if interaction.user == self.username:
            if conversation == "": 
                await interaction.user.send(f"**{SUCCESS_EMOJI} You have successfully closed `{self.channel_name}` created by yourself. \n Reason: `{self.reason}`.**")
            else:
                await interaction.user.send(f"**{SUCCESS_EMOJI} You have successfully closed `{self.channel_name}` created by yourself. \n Reason: `{self.reason}` \n\n Here is the conversation in the channel:**\n```{conversation}```")
                
        else:
            if conversation == "":
                await interaction.user.send(f"**{SUCCESS_EMOJI} You have successfully closed `{self.channel_name}` created by {self.username.mention}. \n Reason: `{self.reason}`.**")
                await self.username.send(f"**{SENDING_EMOJI} Your ticket has successfully been closed by {interaction.user.mention}. \n Reason: `{self.reason}`**", view=rate_button)
            else:
                await interaction.user.send(f"**{SUCCESS_EMOJI} You have successfully closed `{self.channel_name}` created by {self.username.mention}. \n Reason: `{self.reason}` \n\n Here is the conversation in the channel:**\n```{conversation}```")
                await self.username.send(f"**{SENDING_EMOJI} Your ticket has successfully been closed by {interaction.user.mention}. \n Reason: `{self.reason}` \n\n Here is the conversation in the channel:**\n```{conversation}```", view=rate_button)   



# Step 5: Creating a raiting button inside username's DMs
class RateButton(View):
    def __init__(self, username, support_channel, channel_name, issue, notes, reason):
        super().__init__(timeout=None)
        self.username = username
        self.support_channel = support_channel
        self.channel_name = channel_name
        self.issue = issue
        self.notes = notes
        self.reason = reason


    @discord.ui.button(label="Rate Service", style=ButtonStyle.grey, custom_id="oke")
    async def close_ticket_callback(self, interaction, button):

        await interaction.response.send_modal(RateService(self.username, self.support_channel, self.channel_name, self.issue, self.notes, self.reason))


# Step 6: Creating a modal for 
class RateService(Modal, title="Rate Service Form"):
    def __init__(self, username, support_channel, channel_name, issue, notes, reason):
        super().__init__(timeout=None)
        self.username = username
        self.support_channel = support_channel
        self.channel_name = channel_name
        self.issue = issue
        self.notes = notes
        self.reason = reason
        self.rate_button = RateButton(username, support_channel, channel_name, issue, notes, reason)


    text = ui.TextInput

    rate = text(label=f"Rate the service from 1/10", style=discord.TextStyle.short, placeholder="1 to 10", required=True)
    addition = text(label=f"Anything else you wish to add?", style=discord.TextStyle.long, placeholder="Type here", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        ticket_sent = datetime.datetime.utcnow()
        ticket_unix = int((ticket_sent - datetime.datetime(1970, 1, 1)).total_seconds())

        channel = await support_get_logging_channel(interaction, bot)

        ticket_counts["support_ticket_count"] += 1

        # Update the feedback counts in the JSON file
        with open("ticket_counts.json", "w") as f:
            json.dump(ticket_counts, f)

        if channel is not None:
            """           # Create embed message
                self.ticket_logging_embed = discord.Embed(
                    title=f"New Support Case! {FILES_EMOJI}",
                    description=f"The user {self.username.mention} created a support ticket handeled by {interaction.user.mention} \n The ticket has been closed <t:{ticket_unix}:R>.",
                    color=discord.Color.light_gray(),
                    timestamp=datetime.datetime.now()
                )
                self.ticket_logging_embed.add_field(name=f"{self.issue.label}", value=f"```{self.issue.value}```", inline=False)
                if self.notes.value == "":
                     self.ticket_logging_embed.add_field(name=f"{self.notes.label}", value=f"```No Data```", inline=False)
                else:
                     self.ticket_logging_embed.add_field(name=f"{self.notes.label}", value=f"```{self.notes.value}```", inline=False)
                     
                self.ticket_logging_embed.add_field(name=f"{self.reason.label}", value=f"```{self.reason}```", inline=True)
                self.ticket_logging_embed.add_field(name=f"{self.rate.label}", value=f"```{self.rate}```", inline=True) 

                if not self.addition.value == "":
                     self.ticket_logging_embed.add_field(name=f"{self.addition.label}", value=f"```{self.addition}```", inline=False)

                self.ticket_logging_embed.set_author(name=f"{bot.user.name} 🐈 | Logging", icon_url=bot.user.avatar)
                self.ticket_logging_embed.set_footer(text=f"Support Ticket #{ticket_counts['support_ticket_count']} | {bot.user.name}🐈")

                # Edits the logging message from "ClosingTicket" with the new value rate
                await channel.send(embed=self.ticket_logging_embed)
            """
        await interaction.response.send_message(f"**{SUCCESS_EMOJI} The form has sucessfully been submitted! Thank you! :) **", ephemeral=True)
        await asyncio.sleep(10)
        await interaction.delete_original_response()

           

# Load the feedback counts from the JSON file 📠
try:
    with open("ticket_counts.json", "r") as f:
        ticket_counts = json.load(f)
except FileNotFoundError:
    ticket_counts = {"report_ticket_count": 0, "support_ticket_count": 0}



#9. Command for creating a ticket to make contact with the staff 🎫  
@tree(name="ticket", description="Create a ticket to make a contact with the Staff Team 🎫")
@cooldown(10, 120.0, key=lambda i: str(i.user.id))
@access(MEMBERSHIP_ACCESS_ID)
async def ticket(interaction: discord.Interaction):
    # Step 1: Ask the user what type of support they need

    view = TicketView()

    await interaction.response.send_message(f"Hello there 👋🏼",view=view, ephemeral=True, allowed_mentions=False)



class ClosingTicketCommand(View):
    def __init__(self, username, support_channel, channel_name, issue, notes):
        super().__init__(timeout=None)
        #10. Command for closing a ticket to make contact with the staff 🎫  
        @tree(name="close ticket", description="Close an exist ticket 🎫")
        @cooldown(10, 120.0, key=lambda i: str(i.user.id))
        @access(ADMIN_ACCESS_ID)
        async def ticket(interaction: discord.Interaction):
        # Step 1: Ask the user what type of support they need

                # Get the support channel from the view's associated message
            self.support_channel = interaction.channel
                
                # Get the conversation happened in the channel before deleting it
            conversation = ""
            async for message in self.support_channel.history():
                if message.author != interaction.guild.me:
                    conversation += f"{message.author.name}: {message.content}\n"
            
            rate_button = RateButton(self.username, self.support_channel, self.channel_name, self.issue, self.notes, self.reason)
                # Delete the support channel
            await interaction.channel.delete()
            
            channel = await support_get_logging_channel(interaction, self.bot)

            
            ticket_counts["support_ticket_count"] += 1

            # Update the feedback counts in the JSON file
            with open("ticket_counts.json", "w") as f:
                json.dump(ticket_counts, f)

            
            ticket_sent = datetime.datetime.utcnow()
            ticket_unix = int((ticket_sent - datetime.datetime(1970, 1, 1)).total_seconds())

            if channel is not None:
                            # Create embed message
                    ticket_logging_embed = discord.Embed(
                        title=f"New Support Case! {FILES_EMOJI}",
                        description=f"The user {self.user.mention} created a support ticket handles by {interaction.user.mention} \n The ticket has been closed <t:{ticket_unix}:R>.",
                        color=discord.Color.light_gray(),
                        timestamp=datetime.datetime.now()
                    )
                    ticket_logging_embed.add_field(name=f"{self.issue.label}", value=f"```{self.issue.value}```", inline=False)
                    if self.notes.value == "":
                        ticket_logging_embed.add_field(name=f"{self.notes.label}", value=f"```No Data```", inline=False)
                    else:
                        ticket_logging_embed.add_field(name=f"{self.notes.label}", value=f"```{self.notes.value}```", inline=False)
                        
                    ticket_logging_embed.add_field(name=f"{self.reason.label}", value=f"```{self.reason}```", inline=True)    

                    ticket_logging_embed.set_author(name=f"{bot.user.name} 🐈 | Logging", icon_url=bot.user.avatar)
                    ticket_logging_embed.set_footer(text=f"Support Ticket #{ticket_counts['support_ticket_count']} | {bot.user.name}🐈")

                    # Sends a new logging message
                    await channel.send(embed=ticket_logging_embed)
            

            if interaction.user == self.username:
                if conversation == "": 
                    await interaction.user.send(f"**{SUCCESS_EMOJI} You have successfully closed `{self.channel_name}` created by yourself. \n Reason: `{self.reason}`.**")
                else:
                    await interaction.user.send(f"**{SUCCESS_EMOJI} You have successfully closed `{self.channel_name}` created by yourself. \n Reason: `{self.reason}` \n\n Here is the conversation in the channel:**\n```{conversation}```")
                    
            else:
                if conversation == "":
                    await interaction.user.send(f"**{SUCCESS_EMOJI} You have successfully closed `{self.channel_name}` created by {self.username.mention}. \n Reason: `{self.reason}`.**")
                    await self.username.send(f"**{SENDING_EMOJI} Your ticket has successfully been closed by {interaction.user.mention}. \n Reason: `{self.reason}`**", view=rate_button)
                else:
                    await interaction.user.send(f"**{SUCCESS_EMOJI} You have successfully closed `{self.channel_name}` created by {self.username.mention}. \n Reason: `{self.reason}` \n\n Here is the conversation in the channel:**\n```{conversation}```")
                    await self.username.send(f"**{SENDING_EMOJI} Your ticket has successfully been closed by {interaction.user.mention}. \n Reason: `{self.reason}` \n\n Here is the conversation in the channel:**\n```{conversation}```", view=rate_button)  

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# ==========================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Context Commands


class Verification(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="verify", style=ButtonStyle.green, emoji=f"{SUCCESS_EMOJI}", custom_id="verifying")


    async def verify(self, interaction: discord.Interaction, user):

        await interaction.response.defer(ephemeral=True)

        role_added = interaction.guild.get_role(1069003932363391016)
        role_removed = interaction.guild.get_role(1091471850095251618)

        user = interaction.user
        
        if role_removed in user.roles:
            await user.remove_roles(role_removed)
            await user.add_roles(role_added)

            await interaction.followup.send(f"{SUCCESS_EMOJI} **You have been successfully verified!**", embed=True)

        elif role_added in user.roles:
            await interaction.followup.send(f"{ERROR_EMOJI} **You have already been verified.**", ephemeral=True)
        
        elif role_removed not in user.roles and role_added not in user.roles:
            await user.add_roles(role_added)
            await interaction.followup.send(f"{SUCCESS_EMOJI} **You have been successfully verified!**", ephemeral=True)

#1. Command for creating verification system with a button ✅
@context_command(name="cv")
@commands.cooldown(10, 60.0, commands.BucketType.user)
@requires_access2(OWNERSHIP_ACCESS_ID)
async def create_verification(ctx):
    await ctx.message.delete()

    verification_embed = discord.Embed(
        title="Verification System",
        description="Please click below to confirm you are not a bot. \n If you clicked and still see this message, please create a ticket",
        color=0x81b29a,
        timestamp=datetime.datetime.now()
    )
    verification_embed.set_author(name=f"{bot.user.name} | Verification" , icon_url=bot.user.avatar)
    verification_embed.set_footer(text=f"Click below | {bot.user.name}")
    await ctx.send(embed=verification_embed, view=Verification())


class InfoButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
        
        self.ticket_button = Button(label="Create Ticket", style=ButtonStyle.red, custom_id="ticket")
        self.ticket_button.callback = self.ticket
    
        self.links_button = Button(label="Links", style=ButtonStyle.link, url="https://linktr.ee/kindlepets")

        self.guide_button = Button(label="Start Guide", style=ButtonStyle.blurple, custom_id="guide")
        self.guide_button.callback = self.guide
        
        self.add_item(self.guide_button)
        self.add_item(self.ticket_button)
        self.add_item(self.links_button)
    
    
    async def ticket(self, interaction):
        await interaction.response.send_message(f"Hello there 👋🏼",view=TicketView(), ephemeral=True)

        
    async def guide(self,  interaction):     
        await interaction.response.send_message(f"**{PROCESSING_EMOJI} Coming Soon...**", ephemeral=True)

        

#2. Command for creating an information page that includes (Start Guide / Ticket / Links)
@context_command(name="in")
@commands.cooldown(10, 60, commands.BucketType.user)
@requires_access2(OWNERSHIP_ACCESS_ID)
async def create_information(ctx):
    await ctx.message.delete()
    
    infromation_embed = discord.Embed(
        description="```                        Kindle Pets 🐇                ``` \n\n Kidle Pets is your pet's ultimate toy and accessory destination. We tirelessly search the internet to bring you the best products, so your furry friend can always play and be comfortable. Trust us to be your go-to source for high-quality, affordable pet toys and accessories \n\n At Kindle Pets, we offer a diverse range of products to cater to the unique needs of different types of pets, including puppies, kitties, and more! \n As we expand, we plan to introduce new product lines for beloved pets like rabbits, birds, and hamsters! \n\n `❔` For more information, please refer to <#1069052179257765970>.",
        color=0x2f3136, timestamp=datetime.datetime.now(),
    )
    infromation_embed.set_author(name="Information 📄")
    infromation_embed.set_footer(text=f"Information | {bot.user.name} 🐈")

    view = InfoButtons()

    await ctx.send(embed=infromation_embed, view=view)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# ==========================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Configuration Commands ⚙️
entrance_logging_channel_id = None
role_logging_channel_id = None
history_logging_channel_id = None
moderation_logging_channel_id = None
feedback_logging_channel_id = None
support_logging_channel_id = None


# Configuring the names of the logging systems 🔩
logging_system_names = {
    "entrance_logging_channel_id": "`entrance`<:entrance:1073758155219140710>",
    "role_logging_channel_id": "`role updates`<:role:1073758738663620768>",
    "history_logging_channel_id": "`history`<:history:1073758795857145886>",
    "moderation_logging_channel_id" : "`moderation`",
    "feedback_logging_channel_id" : "`feedback`",
    "support_logging_channel_id" : "`support`",

}


def load_channel_ids():
    with open("channel_ids.json", "r") as f:
        return json.load(f)


channel_ids = load_channel_ids()


logging_channel_ids = {
    "entrance_logging_channel_id": channel_ids.get("entrance_logging_channel_id"),
    "role_logging_channel_id": channel_ids.get("role_logging_channel_id"),
    "history_logging_channel_id": channel_ids.get("history_logging_channel_id"),
    "moderation_logging_channel_id": channel_ids.get("moderation_logging_channel_id"),
    "feedback_logging_channel_id" : channel_ids.get("feedback_logging_channel_id"),
    "support_logging_channel_id" : channel_ids.get("support_logging_channel_id"),
}


# Check if the channel is in the logging category 📁
def is_channel_in_correct_category(channel):
    logs_category_id = 1073750975057252412
    return channel.category_id == logs_category_id


# Getting the logging systems names 📃
def get_logging_system_name(channel_id):

    for key, value in logging_channel_ids.items():
        if channel_id == value:
            return logging_system_names[key]
    return None


 #Check if the channel is available for the specified logging system ✅


# Checking if the channel is available for setting the logging system ✅
def is_channel_available_for_logging_system(channel, logging_system_key):
    
    # Load channel IDs from JSON file 📤
    with open("channel_ids.json", "r") as f:
        channel_ids = json.load(f)

    # Check if the channel is already being used by another logging system ✅
    for key, value in channel_ids.items():
        if key == logging_system_key:
            if value == channel.id:
                return f"The {logging_system_names[key]} logging system is already using this channel."
        else:
            if value == channel.id:
                return f"This channel is already being used by the {logging_system_names[key]} logging system."
        
    return True


# - - - - - - - - - - - - - - - - - - - -- - - - -  -- - - - - - - - - -


# Join/Leave Logs 📂

# Configure Entrance Logging Command ⚙️
@tree(name="set_entrance", description="Set the role logging channel 📂")
@cooldown(3, 120.0, key=lambda i: str(i.user.id))
@access(ADMIN_ACCESS_ID)
@arguments(channel="Channel to setup the logging system")
async def set_entrance_logging_channel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    """Sets the logging channel for the entrance logging system."""

    await interaction.response.defer(ephemeral=True)

    # Creating Success & Error Embeds 💬
    success_embed = creating_sucess_embed()
    error_embed = creating_error_embed()

    success_embed.color.light_gray
    error_embed.color.dark_gray

    global entrance_logging_channel_id

    # Check if the interaction is valid ✅
    if interaction is None or interaction.token is None:
        return

    # Set the channel to the default channel if none is provided 🪛
    if not channel:
        channel = interaction.channel

    # Check if the channel is in the required category ✅
    if not is_channel_in_correct_category(channel):
        error_embed.title = f"Command Error {ERROR_EMOJI}"
        error_embed.description = "Channel has to be in `LOGS CHANNEL 📂` category"
        await interaction.followup.send(embed=error_embed)
        return

    # Check if the channel is available for the entrance logging system ✅
    logging_system_key = "entrance_logging_channel_id" # for set_entrance_logging_channel()

    is_channel_available = is_channel_available_for_logging_system(channel, logging_system_key)
    if not is_channel_available == True:
        error_embed.description = is_channel_available
        await interaction.followup.send(embed=error_embed)
        return


    # Update the entrance logging channel ID 🔃
    entrance_logging_channel_id = channel.id


    # Save channel IDs to JSON file 📇
    with open("channel_ids.json", "r") as f:
        channel_ids = json.load(f)
        channel_ids["entrance_logging_channel_id"] = channel.id

    with open("channel_ids.json", "w") as f:
        json.dump(channel_ids, f)

    success_embed.description = f"The logging channel for {logging_system_names['entrance_logging_channel_id']} has been successfully set to {channel.mention}"

    await interaction.followup.send(embed=success_embed)
  

# ==================================================================================

# Roles Update Logs 📂

# Configure Role Logging Command ⚙️
@tree(name="set_roleupdate", description="Set the a logging channel for the join/left events 📂")
@cooldown(3, 120.0, key=lambda i: str(i.user.id))
@access(ADMIN_ACCESS_ID)
@arguments(channel="Channel to setup the logging system")
async def set_role_logging_channel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    """Sets the logging channel for the roles logging system."""

    await interaction.response.defer(ephemeral=True)

    # Creating Success & Error Embeds 💬
    success_embed = creating_sucess_embed()
    error_embed = creating_error_embed()

    success_embed.color.light_gray
    error_embed.color.dark_gray

    global role_logging_channel_id

    # Check if the interaction is valid ✅
    if interaction is None or interaction.token is None:
        return

    # Set the channel to the default channel if none is provided 🪛 
    if not channel:
        channel = interaction.channel

    # Check if the channel is in the required category ✅
    if not is_channel_in_correct_category(channel):
        error_embed.title = f"Command Error {ERROR_EMOJI}"
        error_embed.description = "Channel has to be in `LOGS CHANNEL 📂` category"
        await interaction.followup.send(embed=error_embed)
        return

    # Check if the channel is available for the role logging system ✅
    logging_system_key = "role_logging_channel_id" # for set_role_logging_channel()

    is_channel_available = is_channel_available_for_logging_system(channel, logging_system_key)
    if not is_channel_available == True:
        error_embed.description = is_channel_available
        await interaction.followup.send(embed=error_embed)
        return


    # Update the role logging channel ID 🔃
    role_logging_channel_id = channel.id

    # Save channel IDs to JSON file 📇
    with open("channel_ids.json", "r") as f:
        channel_ids = json.load(f)
        channel_ids["role_logging_channel_id"] = channel.id

    with open("channel_ids.json", "w") as f:
        json.dump(channel_ids, f)

    success_embed.description = f"The logging channel for {logging_system_names['role_logging_channel_id']} has been successfully set to {channel.mention}"

    await interaction.followup.send(embed=success_embed)


# ==================================================================================

# History Chat Update Logs 📂


# Configure History Logging Command ⚙️
@tree(name="set_history", description="Set the a logging channel for the roles events 📂")
@cooldown(3, 120.0, key=lambda i: str(i.user.id))
@access(ADMIN_ACCESS_ID)
@arguments(channel="Channel to setup the logging system")
async def set_history_logging_channel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    """Sets the logging channel for the history logging system."""

    await interaction.response.defer(ephemeral=True)

    # Creating Success & Error Embeds 💬
    success_embed = creating_sucess_embed()
    error_embed = creating_error_embed()

    success_embed.color.light_gray
    error_embed.color.dark_gray

    global history_logging_channel_id

    # Check if the interaction is valid ✅
    if interaction is None or interaction.token is None:
        return

    # Set the channel to the default channel if none is provided 🪛 
    if not channel:
        channel = interaction.channel

    # Check if the channel is in the required category ✅
    if not is_channel_in_correct_category(channel):
        error_embed.title = f"Command Error {ERROR_EMOJI}"
        error_embed.description = "Channel has to be in `LOGS CHANNEL 📂` category"
        await interaction.followup.send(embed=error_embed)
        return

    # Check if the channel is available for the history logging system ✅
    logging_system_key = "history_logging_channel_id" # for set_history_logging_channel()

    is_channel_available = is_channel_available_for_logging_system(channel, logging_system_key)
    if not is_channel_available == True:
        error_embed.description = is_channel_available
        await interaction.followup.send(embed=error_embed)
        return


    # Update the history logging channel ID 🔃
    history_logging_channel_id = channel.id

    # Save channel IDs to JSON file 📇
    with open("channel_ids.json", "r") as f:
        channel_ids = json.load(f)
        channel_ids["history_logging_channel_id"] = channel.id

    with open("channel_ids.json", "w") as f:
        json.dump(channel_ids, f)

    success_embed.description = f"The logging channel for {logging_system_names['history_logging_channel_id']} has been successfully set to {channel.mention}"

    await interaction.followup.send(embed=success_embed)


# ===============================================================


# Moderation Actions Logs 📂

# Configure Moderation Logging Command ⚙️
@tree(name="set_moderation", description="Set the a logging channel for the moderation actions 📂")
@cooldown(3, 120.0, key=lambda i: str(i.user.id))
@access(ADMIN_ACCESS_ID)
@arguments(channel="Channel to setup the logging system")
async def set_moderation_logging_channel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    """Sets the logging channel for the moderation logging system."""

    await interaction.response.defer(ephemeral=True)

    # Creating Success & Error Embeds 💬
    success_embed = creating_sucess_embed()
    error_embed = creating_error_embed()

    success_embed.color.light_gray
    error_embed.color.dark_gray

    global moderation_logging_channel_id

    # Check if the interaction is valid ✅
    if interaction is None or interaction.token is None:
        return

    # Set the channel to the default channel if none is provided 🪛
    if not channel:
        channel = interaction.channel

    # Check if the channel is in the required category ✅
    if not is_channel_in_correct_category(channel):
        error_embed.title = f"Command Error {ERROR_EMOJI}"
        error_embed.description = "Channel has to be in `LOGS CHANNEL 📂` category"
        await interaction.followup.send(embed=error_embed)
        return

    # Check if the channel is available for the entrance logging system ✅
    logging_system_key = "moderation_logging_channel_id" # for set_entrance_logging_channel()

    is_channel_available = is_channel_available_for_logging_system(channel, logging_system_key)
    if not is_channel_available == True:
        error_embed.description = is_channel_available
        await interaction.followup.send(embed=error_embed)
        return


    # Update the entrance logging channel ID 🔃
    entrance_logging_channel_id = channel.id


    # Save channel IDs to JSON file 📇
    with open("channel_ids.json", "r") as f:
        channel_ids = json.load(f)
        channel_ids["moderation_logging_channel_id"] = channel.id

    with open("channel_ids.json", "w") as f:
        json.dump(channel_ids, f)

    success_embed.description = f"The logging channel for {logging_system_names['moderation_logging_channel_id']} has been successfully set to {channel.mention}"

    await interaction.followup.send(embed=success_embed)


# ==================================================================================


# Feedback Logs 📂

# Configure Feedback Logging Command ⚙️
@tree(name="set_feedback", description="Set the a logging channel for the feedback forms 📂")
@cooldown(3, 120.0, key=lambda i: str(i.user.id))
@access(ADMIN_ACCESS_ID)
@arguments(channel="Channel to setup the logging system")
async def set_feedback_logging_channel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    """Sets the logging channel for the feedback logging system."""

    await interaction.response.defer(ephemeral=True)

    # Creating Success & Error Embeds 💬
    success_embed = creating_sucess_embed()
    error_embed = creating_error_embed()

    success_embed.color.light_gray
    error_embed.color.dark_gray

    global feedback_logging_channel_id

    # Check if the interaction is valid ✅
    if interaction is None or interaction.token is None:
        return

    # Set the channel to the default channel if none is provided 🪛
    if not channel:
        channel = interaction.channel

    # Check if the channel is in the required category ✅
    if not is_channel_in_correct_category(channel):
        error_embed.title = f"Command Error {ERROR_EMOJI}"
        error_embed.description = "Channel has to be in `LOGS CHANNEL 📂` category"
        await interaction.followup.send(embed=error_embed)
        return

    # Check if the channel is available for the entrance logging system ✅
    logging_system_key = "feedback_logging_channel_id" # for set_entrance_logging_channel()

    is_channel_available = is_channel_available_for_logging_system(channel, logging_system_key)
    if not is_channel_available == True:
        error_embed.description = is_channel_available
        await interaction.followup.send(embed=error_embed)
        return


    # Update the feedback logging channel ID 🔃
    feedback_logging_channel_id = channel.id


    # Save channel IDs to JSON file 📇
    with open("channel_ids.json", "r") as f:
        channel_ids = json.load(f)
        channel_ids["feedback_logging_channel_id"] = channel.id

    with open("channel_ids.json", "w") as f:
        json.dump(channel_ids, f)

    success_embed.description = f"The logging channel for {logging_system_names['feedback_logging_channel_id']} has been successfully set to {channel.mention}"

    await interaction.followup.send(embed=success_embed)


# ==================================================================================


# Support Logs 📂

# Configure Support Logging Command ⚙️
@tree(name="set_support", description="Set the a logging channel for the support tickets 📂")
@cooldown(3, 120.0, key=lambda i: str(i.user.id))
@access(ADMIN_ACCESS_ID)
@arguments(channel="Channel to setup the logging system")
async def set_feedback_logging_channel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    """Sets the logging channel for the support logging system."""

    await interaction.response.defer(ephemeral=True)

    # Creating Success & Error Embeds 💬
    success_embed = creating_sucess_embed()
    error_embed = creating_error_embed()

    success_embed.color.light_gray
    error_embed.color.dark_gray

    global support_logging_channel_id

    # Check if the interaction is valid ✅
    if interaction is None or interaction.token is None:
        return

    # Set the channel to the default channel if none is provided 🪛
    if not channel:
        channel = interaction.channel

    # Check if the channel is in the required category ✅
    if not is_channel_in_correct_category(channel):
        error_embed.title = f"Command Error {ERROR_EMOJI}"
        error_embed.description = "Channel has to be in `LOGS CHANNEL 📂` category"
        await interaction.followup.send(embed=error_embed)
        return

    # Check if the channel is available for the entrance logging system ✅
    logging_system_key = "support_logging_channel_id" # for set_entrance_logging_channel()

    is_channel_available = is_channel_available_for_logging_system(channel, logging_system_key)
    if not is_channel_available == True:
        error_embed.description = is_channel_available
        await interaction.followup.send(embed=error_embed)
        return


    # Update the feedback logging channel ID 🔃
    support_logging_channel_id = channel.id


    # Save channel IDs to JSON file 📇
    with open("channel_ids.json", "r") as f:
        channel_ids = json.load(f)
        channel_ids["support_logging_channel_id"] = channel.id

    with open("channel_ids.json", "w") as f:
        json.dump(channel_ids, f)

    success_embed.description = f"The logging channel for {logging_system_names['support_logging_channel_id']} has been successfully set to {channel.mention}"

    await interaction.followup.send(embed=success_embed)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# ==========================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


#Menu Apps 🍴

@tree_menu(name="User Info")
@cooldown(3, 60.0, key=lambda i: str(i.user.id))
@access(MEMBERSHIP_ACCESS_ID)
async def user_info(interaction: discord.Interaction, user: discord.Member):

    await interaction.response.defer(ephemeral=True)

    # Create embed object
    embed = discord.Embed(title="User Information", color=user.color)
    timestamp=datetime.datetime.now()
    embed.set_author(name=f"{bot.user.name} 🐈 | Menu", icon_url=bot.user.avatar)
    embed.set_footer(text=f"User Information | {bot.user.name}🐈")
    
    # Set user thumbnail
    embed.set_thumbnail(url=user.avatar)
    
    # General field
    created_at = int(user.created_at.timestamp())
    general_field = f"> **User:** {user.name}#{user.discriminator} {'<:bot:1088838380873338890>' if user.bot else '<:human:1088838501124014220>'}\n"\
                    f"> **ID:** `{user.id}`\n"\
                    f"> **Mention:** {user.mention}\n"\
                    f"> **Created:** <t:{created_at}:R>\n"\
                    f"> **Banner:** `{user.color}`"
                    #f"> **[Profile]({user.avatar})**"
    embed.add_field(name="General", value=general_field, inline=False)
    
    # Server field
    joined_at = int(user.joined_at.timestamp())
    server_field = f"> **Joined:** <t:{joined_at}:R>\n"\
                   f"> **Main Role:** {user.top_role.mention}"
    embed.add_field(name="Server", value=server_field, inline=False)
    
    # Roles field
    roles = [f"> {role.mention}\n" for role in user.roles if role.name != '@everyone']
    roles_field = "".join(roles) if roles else "No roles"
    embed.add_field(name="Roles", value=roles_field, inline=False)
    
    # Send embed message
    await interaction.followup.send(embed=embed, ephemeral=True)


@tree_menu(name="Staff Feedback")
async def staff_feedback(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_modal(Staff_Feedback())



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# ==========================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Modals Apps
text = ui.TextInput

# Community Feedback - Giving Feedback to the community's performance and operations
class Community_Feedback(Modal):
    def __init__(self):
        super().__init__(title="Community Feedback", timeout=None, custom_id="community feedback")

    answer1 = text(label="First Impression", style=discord.TextStyle.long, placeholder="Type your answer", required=True, max_length=100, custom_id="answer1")
    answer2 = text(label="Suggestions to improve", style=discord.TextStyle.paragraph, placeholder="Type your answer", required=False, max_length=200, custom_id="answer2")

    async def on_submit(self, interaction: discord.Interaction):
        feedback_counts["community_feedback_count"] += 1

        # Update the feedback counts in the JSON file
        with open("feedback_counts.json", "w") as f:
            json.dump(feedback_counts, f)

        feedback_sent = datetime.datetime.utcnow()
        feedback_unix = int((feedback_sent - datetime.datetime(1970, 1, 1)).total_seconds())
        
        channel = await feedback_get_logging_channel(interaction.guild)
        if channel is not None:
            embed = discord.Embed(
                title=f"New Community Feedback! {FILES_EMOJI}",
                description=f"The user {interaction.user.mention} has sent a new feedback! \n The feedback has been sent <t:{feedback_unix}:R>",
                color=discord.Color.light_gray(),
                timestamp=datetime.datetime.now()
            )
            embed.add_field(name=f"{self.answer1.label}", value=f"```{self.answer1}```", inline=False)
            if self.answer2.value == "":
                embed.add_field(name=f"{self.answer2.label}", value=f"```No Data```", inline=False)
            else:
                embed.add_field(name=f"{self.answer2.label}", value=f"```{self.answer2}```", inline=False)
            embed.set_author(name=f"{bot.user.name} 🐈 | Logging", icon_url=bot.user.avatar)
            embed.set_footer(text=f"Community Feedback #{feedback_counts['community_feedback_count']} | {bot.user.name}🐈")

            await interaction.response.send_message(f"{SUCCESS_EMOJI} You have successfully submitted your form! \n Thanks for your feedback!", ephemeral=True)

            # Send the feedback to the desired channel
            await channel.send(embed=embed)


# Staff Feedback - Giving Feedback to the Staff's performance
class Staff_Feedback(Modal):
    def __init__(self):
        super().__init__(title="Staff feedback", timeout=None, custom_id="staff feedback")
    
    answer1 = text(label="Staff Username", style=discord.TextStyle.short, placeholder="Example: Darner ⛄#1652", required=True, max_length=50, custom_id="answer1")
    answer2 = text(label="Rate him/her", style=discord.TextStyle.short, placeholder="1 out of 10", required=True, max_length=200, custom_id="answer2")
    answer3 = text(label="Do you think he/she does his/her job propely?", style=discord.TextStyle.paragraph, placeholder="Type your answer", required=False, max_length=200, custom_id="answer3")
    answer4 = text(label="How would you describe him/her", style=discord.TextStyle.paragraph, placeholder="Type your answer", required=False, max_length=200, custom_id="answer4")

    async def on_submit(self, interaction: discord.Interaction):
        feedback_counts["staff_feedback_count"] += 1

        # Update the feedback counts in the JSON file
        with open("feedback_counts.json", "w") as f:
            json.dump(feedback_counts, f)

        feedback_sent = datetime.datetime.utcnow()
        feedback_unix = int((feedback_sent - datetime.datetime(1970, 1, 1)).total_seconds())
        
        channel = await feedback_get_logging_channel(interaction.guild)
        if channel is not None:
            embed = discord.Embed(
                title=f"New Staff Feedback! {FILES_EMOJI}",
                description=f"The user {interaction.user.mention} has sent a new feedback! \n The feedback has been sent <t:{feedback_unix}:R>",
                color=discord.Color.light_gray(),
                timestamp=datetime.datetime.now()
            )
            embed.add_field(name=f"{self.answer1.label}", value=f"```{self.answer1}```", inline=True)
            embed.add_field(name=f"{self.answer2.label}", value=f"```{self.answer2}```", inline=True)

            if self.answer3.value == "":
                embed.add_field(name=f"{self.answer3.label}", value=f"```No Data```", inline=False)
            else:
                embed.add_field(name=f"{self.answer3.label}", value=f"```{self.answer3}```", inline=False)

            if self.answer4.value == "":
                embed.add_field(name=f"{self.answer4.label}", value=f"```No Data```", inline=False)
            else:
                embed.add_field(name=f"{self.answer4.label}", value=f"```{self.answer4}```", inline=False)

            embed.set_author(name=f"{bot.user.name} 🐈 | Logging", icon_url=bot.user.avatar)
            embed.set_footer(text=f"Staff Feedback #{feedback_counts['staff_feedback_count']} | {bot.user.name}🐈", icon_url=interaction.user.avatar)

            await interaction.response.send_message(f"{SUCCESS_EMOJI} You have successfully submitted your form! \n Thanks for your feedback!", ephemeral=True)

            # Send the feedback to the desired channel
            await channel.send(embed=embed)



# Load the feedback counts from the JSON file 📠
try:
    with open("feedback_counts.json", "r") as f:
        feedback_counts = json.load(f)
except FileNotFoundError:
    feedback_counts = {"community_feedback_count": 0, "staff_feedback_count": 0}





# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# ==========================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



# Running kitty! 🐈
if __name__ == '__main__':
    bot.run(Token)








# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# ==========================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#Storage 📦


# Working

class ButtonSelectionMenu(View):
    def __init__(self, interaction, message):
        super().__init__(timeout=2)
        self.message = message
        self.interaction = interaction

        options = [
            SelectOption(label="Link Button", value="link_button", description="A button that links to a URL"),
            SelectOption(label="this is the label", value="this is the value", description="this is the description")
        ]
        select = Select(placeholder="Choose a button type", min_values=1, max_values=1, options=options)
        self.add_item(select)
        
    """
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.interaction.user.id

    async def on_select(self, select: Select, interaction):
        if interaction.data['values'][0] == "link_button":
            self.stop()
        else:
            await interaction.response.send_message("Invalid option selected. Please try again.", ephemeral=True)
    
    async def on_timeout2(self):
        await self.interaction.followup.send("Timeout. Please try again.", ephemeral=True)
    """


@tree(name="add_button", description="Add a button to your message")
@arguments(message_link="Paste the message link where you want the button to be added")
async def add_button(interaction: discord.Interaction, message_link: str):

    async def send_button_selection():
        message_id = int(message_link.split("/")[-1])
        message = await interaction.channel.fetch_message(message_id)
        view = ButtonSelectionMenu(interaction, message)
        await interaction.response.send_message("Choose a button type:", view=view)
        await view.wait()

    async def prompt_information(field_name):
        await interaction.channel.send(f"Please enter the {field_name}:")
        response = await bot.wait_for("message", check=lambda m: m.author.id == interaction.user.id, timeout=60)
        return response.content.strip()

    async def add_button_to_message(interaction, label, url, emoji_id, color):
        try:
            message_id = int(message_link.split("/")[-1])
            message = await interaction.channel.fetch_message(message_id)
            if message.channel.id != interaction.channel.id:
                raise ValueError("Message not found in this channel.")
        except (discord.NotFound, ValueError):
            await interaction.followup.send("Message not found. Please make sure the message link is correct.")
            return

        existing_components = message.components

        # Create a new ActionRow with the existing components and the new button
        new_action_row = ActionRow(*existing_components, Button(style=color, label=label, url=url, emoji=emoji_id))

        await message.edit(components=[new_action_row])

        # Send a follow-up message to the user
        await interaction.followup.send("Button has been added successfully.")

    
   
#-------------------------------------------

    await send_button_selection()

    label = await prompt_information("label")
    url = await prompt_information("URL")
    emoji_id_input = await prompt_information("emoji ID (or type 'none' if you don't want an emoji)")
    emoji_id = None if emoji_id_input.lower() == "none" else emoji_id_input
    color_input = await prompt_information("color (green, blue, red, or grey)")

    color = color_input.strip().lower()
    if color == "green":
        color = ButtonStyle.green
    elif color == "blue":
        color = ButtonStyle.blurple
    elif color == "red":
        color = ButtonStyle.red
    elif color == "grey" or color == "gray":
        color = ButtonStyle.grey
    else:
        await interaction.followup.send("Invalid color. Please choose from green, blue, red, or grey.")
        return

    await add_button_to_message(interaction,label, url, emoji_id, color)
