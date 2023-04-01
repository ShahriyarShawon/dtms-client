from dtms_client.DMTSClient import DTMSClient
class TestClass:
    def setup_class(self):
        self.client = DTMSClient("http://localhost:8000")
    def test_get_class(self):
        c = self.client.get_class("cs 383")
        assert c.number == "CS 383"
    
    def test_get_prereqs_for_class(self):
        paths = self.client.get_prereqs_for_class("CS 383")
        assert len(paths) > 0
    
    def test_postreqs_without_subject(self):
        postreqs = self.client.get_postreqs_for_class("MATH 201")
        assert "CS 300" in postreqs
    
    def test_postreqs_with_subject(self):
        postreqs = self.client.get_postreqs_for_class("MATH 201", "ECE")
        assert "ECE 211" in postreqs
    
    def test_get_classes_for_term_raw(self):
        all_classes_for_term = self.client.get_classes_for_term(term="202245", subject="CS")
        assert len(all_classes_for_term) > 0
    