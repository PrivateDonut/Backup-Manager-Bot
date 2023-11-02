import nextcord
from nextcord.ext import commands, tasks
import os
import time
import asyncio
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

class AutomatedDatabaseBackup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = self.create_connection()
        backup_interval = os.getenv('BACKUP_INTERVAL')
        if backup_interval:
            backup_interval = float(backup_interval)
        else:
            backup_interval = 60.0  # Default to 60 minutes if not set
        self.backup_task = tasks.loop(minutes=backup_interval)(self._backup_task)
        self.backup_task.start()  # Start the loop when the bot starts

    guild_id = int(os.getenv('GUILD_ID'))

    def create_connection(self):
        return mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASS'),
            database=os.getenv('MYSQL_BOT_DB')  # Ensure this is the name of your database
        )

    async def _backup_task(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT database_name FROM auto_backup_preferences")
        databases = cursor.fetchall()
        for db in databases:
            await self.database_backup(db[0])

    async def database_backup(self, database: str):
        BACKUP_LOCATION = os.getenv('BACKUP_LOCATION')
        if BACKUP_LOCATION is None:
            raise ValueError("BACKUP_LOCATION variable is not set.")

        db_folder_path = os.path.join(BACKUP_LOCATION, database)
        os.makedirs(db_folder_path, exist_ok=True)

        timestamp = time.strftime('%Y%m%d%H%M%S')
        backup_file = os.path.join(db_folder_path, f"{database}_{timestamp}.sql")
        
        command = f'"{os.getenv("MYSQL_LOCATION")}\\mysqldump" --user={os.getenv("MYSQL_USER")} --password={os.getenv("MYSQL_PASS")} --host={os.getenv("MYSQL_HOST")} {database} > {backup_file}'

        channel_id = os.getenv("AUTO_BACKUP_CHANNEL_ID")
        if channel_id is None:
            print("AUTO_BACKUP_CHANNEL_ID environment variable is not set!")
            return

        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            print(f"Couldn't find the channel with ID {channel_id}!")
            return
        await channel.send(f"Taking backup for database `{database}`...")
        print(f"Taking backup for database {database}...")

        try:
            proc = await asyncio.create_subprocess_shell(command)
            await proc.communicate()
            await channel.send(f"Backup for database `{database}` completed!")
            print(f"Backup for database `{database}` completed!")

            if proc.returncode != 0:
                print(f"Error while taking backup for database {database}")
                await channel.send(f"Error while taking backup for database `{database}`")
        except Exception as e:
            print(f"Error: {e}")


    @nextcord.slash_command(
        name="backup_auto_add_db",
        description="Add a database to the auto-backup list.",
        guild_ids=[guild_id]
    )
    async def add_auto_backup_db(self, interaction, database:str):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO auto_backup_preferences (user_id, database_name) VALUES (%s, %s)", (interaction.user.id, database))
        self.conn.commit()
        await interaction.send(f"Added `{database}` to the auto-backup list!")

    @nextcord.slash_command(
        name="backup_auto_remove_db",
        description="Remove a database from the auto-backup list.",
        guild_ids=[guild_id]
    )
    async def remove_auto_backup_db(self, interaction, database:str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM auto_backup_preferences WHERE user_id = %s AND database_name = %s", (interaction.user.id, database))
        self.conn.commit()
        await interaction.send(f"Removed `{database}` from the auto-backup list!")

    @nextcord.slash_command(
        name="backup_auto_list_db",
        description="List all databases in the auto-backup list.",
        guild_ids=[guild_id]
    )
    async def list_auto_backup_db(self, interaction):
        cursor = self.conn.cursor()
        cursor.execute("SELECT database_name FROM auto_backup_preferences WHERE user_id = %s", (interaction.user.id,))
        dbs = cursor.fetchall()
        if not dbs:
            await interaction.send("No databases are currently set for auto-backup.")
            return

        dbs_str = ", ".join([db[0] for db in dbs])
        await interaction.send(f"Databases set for auto-backup: `{dbs_str}`")

    @nextcord.slash_command(
        name="backup_auto_start",
        description="Start automated backups for databases.",
        guild_ids=[guild_id]
    )
    async def start_auto_backup(self, interaction):
        if not self.backup_task.is_running():
            self.backup_task.start()
            await interaction.send("Started automated backups!")
        else:
            await interaction.send("Automated backups are already running!")

    @nextcord.slash_command(
        name="backup_auto_stop",
        description="Stop automated backups for databases.",
        guild_ids=[guild_id]
    )
    async def stop_auto_backup(self, interaction):
        if self.backup_task.is_running():
            self.backup_task.cancel()
            await interaction.send("Stopped automated backups!")
        else:
            await interaction.send("Automated backups are not currently running!")

    def cog_unload(self):
        self.conn.close()  # Close the database connection when the cog is unloaded

def setup(bot):
    bot.add_cog(AutomatedDatabaseBackup(bot))
