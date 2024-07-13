import json

from tautulli.sessions.manager import TautulliSessionManager

if __name__ == "__main__":

    # Load the configuration file
    with open("config/config.json", "r") as config_file:
        config = json.load(config_file)

    # Create the session manager
    power_monitor = TautulliSessionManager(
        tautulli_url=config.get("tautulli_url"),
        api_key=config.get("api_key"),
        message=config.get("message"),
    )

    # Close all active plex sessions with the given error message
    print("Closing all active Plex sessions.")
    power_monitor.terminate_all_sessions()
