import nextcord
from nextcord.ext import commands
import time
import os
import asyncio

class DatabaseBackup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guild_id = int(os.getenv('GUILD_ID'))

    @nextcord.slash_command(
        name="database_backup",
        description="Choose a database to backup!",
        guild_ids=[guild_id]
    )
    async def database_backup(self, interaction, database:str):
        BACKUP_LOCATION = os.getenv('BACKUP_LOCATION')
        if BACKUP_LOCATION is None:
            raise ValueError("BACKUP_LOCATION variable is not set.")

        # Create the backup folder for the specified database name
        db_folder_path = os.path.join(BACKUP_LOCATION, database)
        os.makedirs(db_folder_path, exist_ok=True)

        timestamp = time.strftime('%Y%m%d%H%M%S')
        backup_file = os.path.join(db_folder_path, f"{database}_{timestamp}.sql")
        
        command = f'"{os.getenv("MYSQL_LOCATION")}\\mysqldump" --user={os.getenv("MYSQL_USER")} --password={os.getenv("MYSQL_PASS")} --host={os.getenv("MYSQL_HOST")} {database} > {backup_file}'

        # Inform the user that the backup process has started
        await interaction.send(f"Backup for `{database}` is in progress...")  

        try:
            # Use asynchronous subprocess
            proc = await asyncio.create_subprocess_shell(command)
            await proc.communicate()

            if proc.returncode == 0:
                await interaction.followup.send(f"Backup successful! Saved to `{backup_file}`")
            else:
                await interaction.followup.send("Error while taking database backup")
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(DatabaseBackup(bot))
