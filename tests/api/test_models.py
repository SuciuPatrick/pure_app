import pytest
from api.models import Student, Class
from tests.factories import StudentFactory, ClassFactory


@pytest.mark.django_db
class TestStudentCountSignals:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.class_a = ClassFactory()
        self.class_b = ClassFactory()

    def test_student_creation_updates_count(self):
        """Test that creating a student increases the class student count"""
        student = StudentFactory(class_group=self.class_a)
        self.class_a.refresh_from_db()
        assert self.class_a.student_count == 1

    def test_student_deletion_updates_count(self):
        """Test that deleting a student decreases the class student count"""
        student = StudentFactory(class_group=self.class_a)
        self.class_a.refresh_from_db()
        assert self.class_a.student_count == 1

        student.delete()
        self.class_a.refresh_from_db()
        assert self.class_a.student_count == 0

    def test_student_class_change_updates_both_counts(self):
        """Test that changing a student's class updates both old and new class counts"""
        student = StudentFactory(class_group=self.class_a)
        self.class_a.refresh_from_db()
        assert self.class_a.student_count == 1
        assert self.class_b.student_count == 0

        student.class_group = self.class_b
        student.save()

        self.class_a.refresh_from_db()
        self.class_b.refresh_from_db()
        assert self.class_a.student_count == 0
        assert self.class_b.student_count == 1

    def test_multiple_students_count(self):
        """Test that multiple students in the same class are counted correctly"""
        students = [StudentFactory(class_group=self.class_a) for _ in range(3)]
        self.class_a.refresh_from_db()
        assert self.class_a.student_count == 3
