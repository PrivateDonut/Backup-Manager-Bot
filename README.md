# Backup Management Discord Bot

The Database Management Discord Bot, developed in Python, offers a robust solution for managing MySQL database backups directly within Discord. Users can initiate manual backups, set up automated routines, and handle both export and import of backups through an intuitive interface. This seamless integration ensures efficient database management and enhances data portability, all from the convenience of your Discord server.

## Installation

Coming soon....

How to install on Windows
How to install on Debian

## Commands

**Manual Commands:**

1. database_list {database name}

- List the last two backups available for the selected database
- Example: /database_list website

2. database_backup {database name}

- Select the database you wish to backup.
- Example: /database_backup website

3. database_restore {databasename} {backup_name}

- Restore a local backed up database.
- The backup name has to include the full name from the backup folder + the .sql extension
- Example: /database_restore website website_20231020112604.sql

**Automated Commands**

1. backup_auto_start

- Enable automated backups for your MySQL Databases.

2. backup_auto_stop

- Disable automated backups for your MySQL Databases.

3. backup_auto_list_db

- Lists all databases that are setup that backs up automatically.

4. backup_auto_add_db {database name}

- Add a database you wish to be backed up automatically(default every 12 hours)
  - Example: /backup_auto_add_db website

5. backup_auto_remove_db {database name}

- Remove a database you wish to no longer take automatic backups from.
- Example: /backup_auto_remove_db website

## Screenshots

## Authors

- [@PrivateDonut](https://github.com/PrivateDonut?)
