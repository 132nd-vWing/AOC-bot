import datetime
from dataclasses import dataclass


@dataclass
class ScheduledMessage:
    datetime: datetime.datetime
    role_name: str
    role_mention: str
    content: str
    message: str = ''

    def __post_init__(self):
        self.message = f'{self.role_mention}\n{self.content}'
