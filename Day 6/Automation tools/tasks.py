import subprocess

def backup_files():
    print("Running backup...")
    print("Backing up files...")


def cleanup():
    print("Cleaning up temp files...")
    print("Cleanup done")


def system_info():
    subprocess.run(["uname", "-a"])