# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Course, Step

# Create your tests here.

class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regualr Expressions",
            description="Learn to write regex in Python"
        )
        now = timezone.now()
        self.assertLess(course.created_at, now)

class StepModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Basics",
            description="all things basic"
        )

    def test_step_title(self):
        step = Step.objects.create(
            title="Python Basics",
            description="This is a test step for a example course",
            order="1",
            course=self.course,
            content="step 1, step 2, step 3",
        )
        self.assertIn(step, self.course.step_set.all())


class CourseViewTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Testing",
            description="Learn to write a test in Django"
        )

        self.course2 = Course.objects.create(
            title="New Course",
            description="A New course"
        )

        self.step = Step.objects.create(
            title="Introduction to Testing",
            description="Learn to test in your docstrings",
            course=self.course
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:courses_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:course', args=(self.course.pk,)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])
        self.assertTemplateUsed(resp, 'courses/course_detail.html')
        self.assertContains(resp, self.course.title)


    def test_step_detail_view(self):
        resp = self.client.get(reverse('courses:step', args=(self.course.pk, self.step.course.pk,)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context['step'])
        self.assertTemplateUsed(resp, 'courses/step_detail.html')
        self.assertContains(resp, self.step.description)


