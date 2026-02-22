from django.test import TestCase, Client
from django.urls import reverse
from .models import Course

class CourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            name="Test Course",
            instructor="Test Instructor",
            provider="Test Provider",
            url="http://test.com",
            description="Test Description",
            keywords="test",
            status="Active"
        )

    def test_course_list_view(self):
        response = self.client.get(reverse('course:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Course")
        self.assertContains(response, "Test Instructor")
        self.assertTemplateUsed(response, 'course.html')
        self.assertTemplateUsed(response, 'course/course_list.html')
