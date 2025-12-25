import logging
from datetime import datetime, timedelta
from typing import List, Optional


class EitaaSession:
    def __init__(self, session_id: str, client_instance):
        self.session_id = session_id
        self.client = client_instance
        self.is_active = True
        self.last_used = datetime.now()
        self.cool_donw_until = None

    def mark_rate_limited(self, minutes: int = 15):
        "Make the limited session unavailable for a while"
        self.is_active = False
        self.cool_down_until = datetime.now() + timedelta(minutes=minutes)
        id = self.session_id
        logging.info(
            f"session {id} is rate limited until {self.cool_down_until}"
            )

    def check_health(self):
        "Make the formerly limited session active again if it's the time"
        if not self.is_active and (self.cool_donw_until < datetime.now()):
            self.is_active = True
            logging.info(f"session {self.session_id} is activated again")


class SessionManager:
    def __init__(self):
        self.sessions: List[EitaaSession] = []
        self._current_index = 0

    def add_session(self, session_id: str, client_instance):
        new_session = EitaaSession(session_id, client_instance)
        self.sessions.append(new_session)

    def get_next_available_session(self) -> Optional[EitaaSession]:
        "Choose the next active session in a random way"
        if not self.sessions:
            return None

        # return the sessions that are cooled and ready
        for s in self.sessions:
            s.check_health()

        active_sessions = [s for s in self.sessions if s.is_active]
        if not active_sessions:
            logging.info("Currently no session is active")
            return None

        # choose a session (round-robin)
        session = active_sessions[self._current_index % len(self.sessions)]
        self._current_index += 1
        session.last_used = datetime.now()
        return session

    def get_total_active_count(self) -> int:
        return len([s for s in self.sessions if s.is_active])
