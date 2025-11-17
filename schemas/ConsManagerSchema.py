from pydantic import BaseModel

class ConsultingManagerBase(BaseModel):
    name: str
    email: str
    department_name: str


class ConsultingManagerCreate(ConsultingManagerBase):
    pass


class ConsultingManagerResponse(ConsultingManagerBase):
    id: int

    class Config:
        orm_mode = True
