import enum
from datetime import datetime

from beanie import Document


class ActionEnum(enum.Enum):
    LIST_CREATE = "list_create"
    LIST_DELETE = "list_delete"
    NOTE_CREATE = "note_create"
    NOTE_DELETE = "note_delete"
    NOTE_MARKED_DONE = "note_marked_done"
    NOTE_MARKED_UNDONE = "note_marked_undone"


class UserAction(Document):
    user_id: int
    action: ActionEnum
    timestamp: datetime
