from app.models import UserAction, ActionEnum


class StatisticsServices:
    model = UserAction

    @classmethod
    async def create_user_action(cls, action_schema: model):
        user_action = await action_schema.create()
        return user_action

    @classmethod
    async def retrieve_statistics(cls, user_id: int):
        total_created_notes = await cls.model.find(
            cls.model.user_id == user_id,
            cls.model.action == ActionEnum.NOTE_CREATE) \
            .count()

        total_done_notes = await cls.model.find(
            cls.model.user_id == user_id,
            cls.model.action == ActionEnum.NOTE_MARKED_DONE) \
            .count()

        done_notes_ratio = total_done_notes / total_created_notes if total_created_notes else 0

        data = {
            'user_id': user_id,
            'total_created_notes': total_created_notes,
            'total_done_notes': total_done_notes,
            'done_notes_ratio': done_notes_ratio
        }
        return data
