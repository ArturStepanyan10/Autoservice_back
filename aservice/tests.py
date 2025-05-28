import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from aservice.models import (
    User, Car, Service, Worker, Appointment,
    Reviews, Specialization, Post
)


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', password='1234', role='Клиент', first_name='Иван', last_name='Иванов', username='test')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'Клиент')


class CarModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='owner@example.com', password='1234', role='Клиент')

    def test_create_car(self):
        car = Car.objects.create(
            brand='Toyota',
            model='Camry',
            year='2018',
            color='Белый',
            vin='JTDBE32K530068472',
            license_plate='A123BC77',
            user=self.user
        )
        self.assertEqual(car.vin, 'JTDBE32K530068472')
        self.assertEqual(car.user, self.user)


class ServiceModelTest(TestCase):
    def test_create_service(self):
        service = Service.objects.create(
            title='Замена масла',
            description='Полная замена масла в двигателе',
            labor_time=datetime.timedelta(minutes=45),
            difficulty_level=2
        )
        self.assertEqual(service.title, 'Замена масла')
        self.assertEqual(service.difficulty_level, 2)


class WorkerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='worker@example.com', password='1234', role='Механик')
        self.specialization = Specialization.objects.create(title='Автоэлектрик')
        self.position = Post.objects.create(title='Главный механик')

    def test_create_worker(self):
        worker = Worker.objects.create(
            user=self.user,
            specialization=self.specialization,
            position=self.position,
            experience=5
        )
        self.assertEqual(worker.user.email, 'worker@example.com')
        self.assertEqual(worker.experience, 5)


class AppointmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='client@example.com', password='1234', role='Клиент', username='test')
        self.worker_user = User.objects.create_user(email='worker2@example.com', password='1234', role='Механик')
        self.worker = Worker.objects.create(user=self.worker_user, specialization=None, position=None, experience=3)
        self.car = Car.objects.create(
            brand='Ford', model='Focus', year='2020', vin='1HGCM82633A004352', license_plate='X111XX99', user=self.user
        )
        self.service = Service.objects.create(title='Шиномонтаж', description='Замена резины', labor_time=datetime.timedelta(minutes=60))

    def test_create_appointment_valid(self):
        appointment = Appointment.objects.create(
            date=timezone.now().date() + datetime.timedelta(days=1),
            time=datetime.time(hour=10, minute=30),
            car=self.car,
            user=self.user,
            worker=self.worker,
            email='client@example.com',
            phone_number='+79991234567',
            first_name='Иван',
            last_name='Петров'
        )
        appointment.service.set([self.service])
        appointment.full_clean()  # не должно вызвать исключение
        self.assertEqual(appointment.worker, self.worker)

    def test_create_appointment_past_date(self):
        appointment = Appointment(
            date=timezone.now().date() - datetime.timedelta(days=1),
            time=datetime.time(hour=10, minute=30),
            car=self.car,
            user=self.user,
            worker=self.worker,
            email='client@example.com',
            phone_number='+79991234567'
        )
        with self.assertRaises(ValidationError):
            appointment.clean()


class ReviewsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='rev@example.com', password='1234', role='Клиент', username='test')
        self.service = Service.objects.create(title='Мойка', description='Мойка кузова', labor_time=datetime.timedelta(minutes=30))

    def test_create_review(self):
        review = Reviews.objects.create(
            user=self.user,
            service=self.service,
            rating=5,
            content='Отлично всё сделали!'
        )
        self.assertEqual(review.rating, 5)
        self.assertTrue(review.is_published)


class SpecializationPostModelTest(TestCase):
    def test_create_specialization(self):
        spec = Specialization.objects.create(title='Диагност')
        self.assertEqual(str(spec), 'Диагност')

    def test_create_post(self):
        post = Post.objects.create(title='Стажер')
        self.assertEqual(str(post), 'Стажер')
