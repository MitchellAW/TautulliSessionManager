from typing import List

import requests
from requests.exceptions import ConnectionError


class TautulliSessionManager:

    def __init__(self, tautulli_url: str, api_key: str, message: str) -> None:
        """Manage active tautulli sessions/streams

        Args:
            tautulli_url (str): The url to access the Tautulli instance
            api_key (str): The api key to access the Tautulli instance
            message (str): The message to display to the end user
                           after terminating a session
        """

        self.url = f"{tautulli_url}/api/v2?apikey={api_key}&cmd={{}}"
        self.message = message

    def get_session_keys(self) -> List[int]:
        """Gets a list of active session keys

        Returns:
            List[int]: A list of the active session keys
        """
        try:
            response = requests.get(self.url.format("get_activity"))
            if response.status_code == 200:
                activity = response.json()

                # Unpack session data
                activity_response = activity.get("response", {})
                activity_data = activity_response.get("data", {})
                sessions = activity_data.get("sessions", [])

                session_keys = [session.get("session_key", -1) for session in sessions]
                return [session_key for session_key in session_keys if session_key != -1]

            else:
                return []

        except ConnectionError:
            return []

    def terminate_session(self, session_key: str) -> int:
        """Terminates any active Tautulli session with the given session key

        Args:
            session_key (str): The key of the session

        Returns:
            int: The status code returned from the termination request
        """

        print(f"Terminating plex session {session_key}.")

        url_keys = f"&session_key={session_key}&message={self.message}"

        try:
            response = requests.get(self.url.format("terminate_session") + url_keys)

            return response.status_code

        except ConnectionError:
            return 500

    def terminate_all_sessions(self) -> None:
        """Terminate all active Tautulli sessions."""

        print("Terminating all active Plex sessions.")
        sessions = self.get_session_keys()

        for session_key in self.get_session_keys():
            if self.terminate_session(session_key) == 200:
                print(f"Successfully terminated session {session_key}.")

            else:
                print(f"Failed to terminate session {session_key}.")
