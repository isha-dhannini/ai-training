import subprocess
import time
from pyngrok import ngrok


def main():
    process = subprocess.Popen(
        ["autogenstudio", "ui", "--port", "8081", "--host", "0.0.0.0"]
    )

    print("Starting AutoGen Studio...")
    time.sleep(8)

    public_url = ngrok.connect(8081)
    print("AutoGen Studio URL:", public_url)

    print("\nStudio is running.")
    print("Press Ctrl+C in this terminal to stop it.")

    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nStopping Studio...")
        process.terminate()


if __name__ == "__main__":
    main()