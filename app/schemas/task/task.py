from pydantic import BaseModel, ConfigDict

class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)