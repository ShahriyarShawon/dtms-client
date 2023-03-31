import requests
from yarl import URL
from cattrs import structure
import json
from attrs import define

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
    pass

class DTMSClient:
    def __init__(self, base_url: str):
        self.base = URL(base_url)
        self.session = requests.Session()
    
    def get_class(self, course_number: str) -> DrexelClass:
        url = self.base / "class" / course_number
        response = self.session.get(url)
        content = json.loads(response.content)
        return structure(content, DrexelClass)
    
    def get_prereqs_for_class(self, class_number: str) -> list[str]:
        pass 

    def get_postreqs_for_class(self, class_number: str, subject_filter: str) -> list[str]:
        pass 

    def get_classes_for_term(
        self, 
        term: str,
        college: str = None,
        subject: str = None,
        credit_hours: int = None,
        prereq: str = None,
        instructor: str = None,
        writing_intensive: bool = False,  
    ) -> list[DrexelClass]:

        pass