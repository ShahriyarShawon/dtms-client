import json
from typing import Optional

import requests
from attrs import define
from cattrs import structure
from yarl import URL


@define
class DrexelClass:
    subject: str
    name: str
    high_credits: float
    writing_intensive: bool
    desc: str
    college: str
    number: str
    prereqs: str


@define
class DrexelTMSClass:
    term: str
    subject: str
    course_number: str
    instruction_type: str
    instruction_method: str
    section: str
    crn: str
    days_time: str
    instructors: str


class DTMSClient:
    def __init__(self, base_url: str):
        self.base = URL(base_url)
        self.session = requests.Session()

    def get_class(self, course_number: str) -> DrexelClass:
        url = self.base / "class" / course_number
        response = self.session.get(url)
        content = json.loads(response.content)
        if "status_code" in content:
            return None 
        return structure(content, DrexelClass)

    def get_prereqs_for_class(self, course_number: str) -> list[str]:
        url = self.base / "prereqs" / course_number
        response = self.session.get(url)
        content = json.loads(response.content)
        return content

    def get_postreqs_for_class(
        self, course_number: str, subject_filter: Optional[str] = None
    ) -> list[DrexelClass]:
        url = self.base / "postreqs" / course_number
        if subject_filter:
            url = url.with_query({"subject_filter": subject_filter})
        response = self.session.get(url)
        content = json.loads(response.content)
        return structure(content, list[DrexelClass])

    def get_classes_for_term(
        self,
        term: str,
        course_number: Optional[str] = None,
        college: Optional[str] = None,
        subject: Optional[str] = None,
        credit_hours: Optional[int] = None,
        prereq: Optional[str] = None,
        instructor: Optional[str] = None,
        writing_intensive: Optional[bool] = False,
    ) -> list[DrexelTMSClass]:
        url = self.base / "classes" / "term" / ""
        url = url % {"term": term}
        if course_number:
            url = url % {"course_number": course_number.upper()}
        if college:
            url = url % {"college": college.upper()}
        if subject:
            url = url % {"subject": subject.upper()}
        if credit_hours:
            url = url % {"credit_hours": credit_hours}
        if prereq:
            url = url % {"prereq": prereq}
        if instructor:
            url = url % {"instructor": instructor}
        if not writing_intensive:
            url = url % {"writing_intensive": "false"}
        response = self.session.get(url)
        content = json.loads(response.content)

        return structure(content, list[DrexelTMSClass])
