import json

from django.test import Client, TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from courses.models import Course
from quizzes.models import Quiz


class EditSolutionsTests(TestCase):

    def setUp(self):
        User.objects.create_user('0', password='0')
        User.objects.create_user('1', password='0')
        instructor = Profile.objects.get(user__username='0')
        student = Profile.objects.get(user__username='1')

        course = Course()
        course.name = '0'
        course.owner = instructor
        course.save()
        course.instructors.add(instructor)
        course.students.add(student)

        instructor_client = Client()
        instructor_client.post('/login/', data={
            'login': '0',
            'password': '0'
        })

        instructor_client.post('/quizzes/create/', data={
            'course': '1',
        })
        instructor_client.post('/quiz/1/article/edit/', data={
            'title': '0',
            'content': '0'
        })
        instructor_client.post('/quiz/1/questions/edit/', data={
            'questions': '["1", "2", "3", "4"]'
        })

        student_client = Client()
        student_client.post('/login/', data={
            'login': '1',
            'password': '0'
        })

        self.instructor_client = instructor_client
        self.student_client = student_client

    def test_instructor_can_edit_solutions(self):
        resp = self.instructor_client.get('/quiz/1/solutions/edit/')
        self.assertEqual(resp.status_code, 200)

    def test_student_cant_edit_solutions(self):
        resp = self.student_client.get('/quiz/1/solutions/edit/')
        self.assertEqual(resp.status_code, 403)

    def test_field_solution_available(self):
        quiz = Quiz.objects.get(pk=1)
        self.assertEqual(quiz.solution_available, False)

        data = {'solutions': [
            {'question_id': 1, 'solution': '1'},
            {'question_id': 2, 'solution': '2'},
            {'question_id': 3, 'solution': '3'},
            {'question_id': 4, 'solution': '4'},
        ]}
        self.instructor_client.post('/quiz/1/solutions/edit/', data=json.dumps(data), content_type='application/json')

        quiz = Quiz.objects.get(pk=1)
        self.assertEqual(quiz.solution_available, True)
