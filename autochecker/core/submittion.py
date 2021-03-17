import uuid
from dataclasses import dataclass


@dataclass
class StudentSubmission:
    submit_id: str
    student_name: str
    service_url: str
    accuracy: float

    @staticmethod
    def gen_id():
        return str(uuid.uuid4())
