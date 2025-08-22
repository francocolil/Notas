from sqlmodel import SQLModel, Field

class NoteBase(SQLModel):
    name_note: str
    description: str | None = None


class Note(NoteBase, table=True):
    id: int | None = Field(primary_key=True, default=None, index=True, unique=True)
    id_user: int = Field(foreign_key= "user.id")

class NoteCreate(NoteBase):
    pass

class NotePublic(NoteBase):
    pass
