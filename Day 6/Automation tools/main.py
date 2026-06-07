import argparse
from tasks import backup_files, cleanup, system_info
from scheduler import start_scheduler

def main():

    parser = argparse.ArgumentParser(description="Automation Tool")

    parser.add_argument("--task", choices=["backup", "cleanup", "info"])
    parser.add_argument("--mode", choices=["run", "schedule"])

    args = parser.parse_args()

    # RUN ONCE MODE
    if args.mode == "run":
        if args.task == "backup":
            backup_files()
        elif args.task == "cleanup":
            cleanup()
        elif args.task == "info":
            system_info()

    # PYTHON SCHEDULER MODE
    elif args.mode == "schedule":
        start_scheduler()


if __name__ == "__main__":
    main()


# Use this command
# To run once        : python main.py --task backup --mode run
# To start schedular : python main.py --mode schedule
