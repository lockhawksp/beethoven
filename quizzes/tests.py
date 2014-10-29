import json

from django.test import Client, TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from courses.models import Course
from quizzes.models import Quiz


def create_test_profile(username, password):
    User.objects.create_user(username, password=password)
    return Profile.objects.get(user__username=username)


def create_test_course(name, owner, instructors=(), students=()):
    course = Course()
    course.name = name
    course.owner = owner
    course.save()
    course.instructors.add(*instructors)
    course.students.add(*students)


def login_test_user(username, password):
    client = Client()
    client.post('/login/', data={
        'login': username,
        'password': password
    })
    return client


def create_test_quiz(client, course_id, title, content, questions=()):
    resp = client.post('/quizzes/create/', data={
        'course': course_id,
    })

    resp = client.post(resp.url, data={
        'title': title,
        'content': content
    })

    client.post(resp.url, data={
        'questions': json.dumps(list(questions))
    })


def create_test_solutions(client):
    data = {'solutions': [
        {'question_id': 1, 'solution': '1'},
        {'question_id': 2, 'solution': '2'},
        {'question_id': 3, 'solution': '3'},
        {'question_id': 4, 'solution': '4'},
    ]}
    resp = client.post(
        '/quiz/1/solutions/edit/',
        data=json.dumps(data),
        content_type='application/json'
    )
    return resp


class EditSolutionsTests(TestCase):

    def setUp(self):
        instructor = create_test_profile('0', '0')
        student = create_test_profile('1', '0')
        instructor_client = login_test_user('0', '0')
        student_client = login_test_user('1', '0')
        create_test_course(
            '0',
            instructor,
            instructors=(instructor,),
            students=(student,)
        )
        create_test_quiz(instructor_client, 1, '0', '0',
                         questions=('1', '2', '3', '4'))

        self.instructor_client = instructor_client
        self.student_client = student_client

    def test_instructor_can_edit_solutions(self):
        resp = self.instructor_client.get('/quiz/1/solutions/edit/')
        self.assertEqual(resp.status_code, 200)

        resp = create_test_solutions(self.instructor_client)
        self.assertEqual(resp.status_code, 200)

    def test_student_cant_edit_solutions(self):
        resp = self.student_client.get('/quiz/1/solutions/edit/')
        self.assertEqual(resp.status_code, 403)

        resp = create_test_solutions(self.student_client)
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
        self.instructor_client.post(
            '/quiz/1/solutions/edit/',
            data=json.dumps(data),
            content_type='application/json'
        )

        quiz = Quiz.objects.get(pk=1)
        self.assertEqual(quiz.solution_available, True)

    def test_student_cant_change_answers_after_viewing_solutions(self):
        url = '/quiz/1/attempt/'
        resp = self.student_client.get(url)
        self.assertEqual(resp.status_code, 200)

        data = {'answers': [
            {'id': 1, 'answer': '1'},
            {'id': 2, 'answer': '2'},
            {'id': 3, 'answer': '3'},
            {'id': 4, 'answer': '4'},
        ]}
        resp = self.student_client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)

        self.student_client.get('/quiz/1/solutions/view/')
        resp = self.student_client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 403)

    def test_student_can_only_view_solutions_after_submitting_answers(self):
        resp = self.student_client.get('/quiz/1/solutions/view/')
        self.assertEqual(resp.status_code, 403)
