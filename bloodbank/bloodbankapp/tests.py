from django.test import TestCase
from django.contrib.auth.models import User
from .models import BloodDonor

class DonorTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john', password='test123')
        BloodDonor.objects.create(

            name="John Doe",
            age=30,
            gender="M",
            blood_group="O+",
            contact_number="9876543210",
            address="Lucknow"
            # Add other required fields here if needed
        )

    def test_donor_created(self):
        donor = BloodDonor.objects.get(name="John Doe")
        self.assertEqual(donor.blood_group, "O+")



from .models import BloodRequest, Hospital


class BloodRequestTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='requester', password='testpass')
        BloodRequest.objects.create(
            requester=user,
            blood_type="A+",
            units=2,
            urgency="medium",
            contact_number="+911234567890",
            hospital="City Hospital",
            status="pending"
        )

    def test_blood_request_created(self):
        request = BloodRequest.objects.get(blood_type="A+")
        self.assertEqual(request.units, 2)


from .models import BloodDonor, BloodCamp, CampRegistration
import datetime


from .models import Hospital

class HospitalTestCase(TestCase):
    def setUp(self):
        Hospital.objects.create(
            name="City Hospital",
            hospital_type="general",
            phone="1234567890",
            address="Delhi"
        )

    def test_hospital_created(self):
        hospital = Hospital.objects.get(name="City Hospital")
        self.assertEqual(hospital.hospital_type, "general")


from .models import BloodDonor, BloodCamp, CampRegistration
import datetime

class CampRegistrationTestCase(TestCase):
    def setUp(self):
        donor = BloodDonor.objects.create(
            name="Ankit",
            age=28,
            gender="M",
            blood_group="B+",
            contact_number="+919876543210",
            address="Kanpur",
            donor_city="Kanpur"
        )
        camp = BloodCamp.objects.create(
            name="Summer Blood Camp",
            organizer="Red Cross",
            start_date=datetime.date.today(),
            city=None
        )
        CampRegistration.objects.create(
            donor=donor,
            camp=camp,
            attended=False,
            donation_made=False
        )

    def test_camp_registration(self):
        registration = CampRegistration.objects.first()
        self.assertEqual(registration.donor.name, "Ankit")
        self.assertEqual(registration.camp.name, "Summer Blood Camp")


from django.contrib.auth.models import User
from django.test import Client


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='admin123')

    def test_user_login(self):
        login_success = self.client.login(username='admin', password='admin123')
        self.assertTrue(login_success)
