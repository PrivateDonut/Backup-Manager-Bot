import nextcord
from nextcord.ext import commands
import os
import datetime

guild_id = int(os.getenv('GUILD_ID'))
class ListBackups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
    name="database_list",
    description="List the last 10 backups for a database",
    guild_ids=[guild_id]
    )
    async def list_backups(self, interaction, database:str):
        BACKUP_LOCATION = os.getenv('BACKUP_LOCATION')
        db_folder_path = os.path.join(BACKUP_LOCATION, database)

        if not os.path.exists(db_folder_path):
            await interaction.send(f"No backups found for database `{database}`.")
            return

        backups = sorted(os.listdir(db_folder_path), key=lambda x: os.path.getmtime(os.path.join(db_folder_path, x)), reverse=True)[:10]

        if not backups:
            await interaction.send(f"No backups found for database `{database}`.")
            return

        formatted_backups = []
        for backup in backups:
            date_str = backup.split("_")[1].split(".")[0]
            date_obj = datetime.datetime.strptime(date_str, "%Y%m%d%H%M%S")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            formatted_time = date_obj.strftime("%H:%M:%S")
            formatted_backups.append(f"{backup} (Date: {formatted_date}, Time: {formatted_time})")

        backups_str = "\n".join(formatted_backups)
        await interaction.send(f"Last 10 backups for `{database}`:\n```\n{backups_str}\n```")

def setup(bot):
    bot.add_cog(ListBackups(bot))