from lib.app_menu import AppMenu
from lib.rds_manager import RDSManager


def main():
    rds_manager = RDSManager()
    app_menu = AppMenu(rds_manager)
    app_menu.option_menu()


if __name__ == "__main__":
    main()
