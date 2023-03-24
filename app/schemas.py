from pydantic import BaseModel


class Statistics(BaseModel):
    user_id: int
    total_created_notes: int
    total_done_notes: int
    done_notes_ratio: int
