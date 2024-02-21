from typing import Any
from dataclasses import dataclass


@dataclass
class Profile:
    id: int
    username: str
    firstName: str
    lastName: str
    email: str
    locale: str
    timeZone: str

    @staticmethod
    def from_dict(obj: Any) -> "Profile":
        _id = int(obj.get("id"))
        _username = str(obj.get("username"))
        _firstName = str(obj.get("firstName"))
        _lastName = str(obj.get("lastName"))
        _email = str(obj.get("email"))
        _locale = str(obj.get("locale"))
        _timeZone = str(obj.get("timeZone"))
        return Profile(
            _id, _username, _firstName, _lastName, _email, _locale, _timeZone
        )
