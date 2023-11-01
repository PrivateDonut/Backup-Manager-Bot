import nextcord
from nextcord.ext import commands
import os
import asyncio

class BackupRestore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guild_id = 995986682228768799

    @nextcord.slash_command(
    name="database_restore",
    description="Restore a database from a specified backup",
    guild_ids=[guild_id]
    )   
    
    async def restore_backup(self, interaction, database:str, backup_name:str):
        BACKUP_LOCATION = os.getenv('BACKUP_LOCATION')
        backup_file_path = os.path.join(BACKUP_LOCATION, database, backup_name)

        if not os.path.exists(backup_file_path):
            await interaction.send(f"Backup file `{backup_name}` not found for database `{database}`.")
            return

        command = f'"{os.getenv("MYSQL_LOCATION")}\\mysql" --user={os.getenv("MYSQL_USER")} --password={os.getenv("MYSQL_PASS")} --host={os.getenv("MYSQL_HOST")} -e "source {backup_file_path}" {database}'

        await interaction.send(f"Restoring `{database}` from `{backup_name}`. This might take a while...")
        print(f"Backup file path: {backup_file_path}")
        print(f"MySQL executable path: {os.getenv('MYSQL_LOCATION')}\\mysql")

        try:
            proc = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()

            if proc.returncode == 0:
                await interaction.followup.send(f"Database `{database}` successfully restored from `{backup_name}`!")
            else:
                error_message = stderr.decode('utf-8') if stderr else "Unknown error"
                await interaction.followup.send(f"Error while restoring the database backup: {error_message}")

        except Exception as e:
            await interaction.followup.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(BackupRestore(bot))
