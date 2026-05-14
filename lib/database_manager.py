from string import Template

import questionary


class DatabaseManager:
    def __init__(self, rds_manager):
        self.rds_manager = rds_manager

    def choose_database(self) -> dict:
        databases = self.rds_manager.get_databases()
        if not databases:
            return None

        db_choice = questionary.select(
            "Select a database:",
            choices=[db["DBInstanceIdentifier"] for db in databases],
        ).ask()
        for db in databases:
            if db["DBInstanceIdentifier"] == db_choice:
                return db
        return None

    def choose_snapshot(self, database_name: str) -> str:
        snapshots = self.rds_manager.get_snapshots(database_name)
        if not snapshots:
            return None
        choices = [
            f"{snapshot['id']:<55} {snapshot['create_time']}" for snapshot in snapshots
        ]
        return questionary.select("Select a snapshot:", choices=choices).ask()

    @staticmethod
    def get_template(path: str) -> str:
        with open(path, "r") as tpl_file:
            return tpl_file.read()

    def create_database_from_snapshot(self) -> None:
        source_db = self.choose_database()
        if not source_db:
            return

        snapshot = self.choose_snapshot(source_db["DBInstanceIdentifier"])
        if not snapshot:
            return
        snapshot = snapshot.split()[0]

        target_db = questionary.text("Enter a name for the new database: ").ask()

        template_data = self.get_template("templates/database.tpl")
        template = Template(template_data)
        tpl = template.substitute(
            source=source_db["DBInstanceIdentifier"],
            snapshot=snapshot,
            target=target_db,
        )
        print(tpl)

        confirmed = questionary.confirm("Proceed with restore?").ask()
        if confirmed:
            self.rds_manager.restore_database_from_snapshot(
                snapshot, target_db, source_db
            )
