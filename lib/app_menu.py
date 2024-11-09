import pyinputplus as pyip
from lib.database_manager import DatabaseManager


class AppMenu:
    def __init__(self, rds_manager):
        self.rds_manager = rds_manager
        self.db_manager = DatabaseManager(rds_manager)

    @staticmethod
    def divider():
        print("-" * 45)

    def option_menu(self):
        print("Default region: us-east-1")
        self.divider()

        choice = ""
        while choice != "Quit":
            choice = pyip.inputMenu(
                [
                    "Change region",
                    "List databases",
                    "Create database from snapshot",
                    "Quit",
                ],
                lettered=False,
                numbered=True,
            )
            if choice == "Change region":
                self.rds_manager.change_region()
            elif choice == "List databases":
                databases = self.rds_manager.get_databases()
                for db in databases:
                    print(f"    {db['DBInstanceIdentifier']}")
            elif choice == "Create database from snapshot":
                self.db_manager.create_database_from_snapshot()
            elif choice == "Quit":
                print("Bye")
