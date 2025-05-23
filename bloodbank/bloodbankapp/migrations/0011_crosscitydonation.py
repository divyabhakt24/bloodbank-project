# Generated by Django 4.2.20 on 2025-05-07 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bloodbankapp", "0010_bloodinventory"),
    ]

    operations = [
        migrations.CreateModel(
            name="CrossCityDonation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "blood_type",
                    models.CharField(
                        choices=[
                            ("A+", "A+"),
                            ("A-", "A-"),
                            ("B+", "B+"),
                            ("B-", "B-"),
                            ("O+", "O+"),
                            ("O-", "O-"),
                            ("AB+", "AB+"),
                            ("AB-", "AB-"),
                        ],
                        max_length=3,
                    ),
                ),
                ("units", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("initiated", "Initiated"),
                            ("donated", "Donated"),
                            ("transferred", "Transferred"),
                            ("received", "Received"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="initiated",
                        max_length=15,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("donation_date", models.DateField(blank=True, null=True)),
                ("received_date", models.DateField(blank=True, null=True)),
                (
                    "donor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cross_city_donations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "donor_blood_bank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="donor_blood_bank",
                        to="bloodbankapp.bloodbank",
                    ),
                ),
                (
                    "donor_city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="donor_city",
                        to="bloodbankapp.city",
                    ),
                ),
                (
                    "patient_blood_bank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_blood_bank",
                        to="bloodbankapp.bloodbank",
                    ),
                ),
                (
                    "patient_city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_city",
                        to="bloodbankapp.city",
                    ),
                ),
            ],
        ),
    ]
