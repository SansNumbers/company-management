from celery import shared_task

from apps.audit.models import Audit
from apps.company.models import Company
from apps.office.models import Office
from apps.vehicle.models import Vehicle
from apps.worker.api.utils import send_email


@shared_task
def calculate_vehicles_number():
    for office in Office.objects.all():
        vehicle_count = Vehicle.objects.filter(office_id=office.pk).count()
        office.vehicle_count = vehicle_count
        office.save()


@shared_task
def send_vehicle_report():
    for company in Company.objects.all():
        vehicles = Vehicle.objects.filter(company=company).exclude(office=True).values_list('name', flat=True)
        vehicle_string_names = f'{", ".join(list(vehicles))}.'
        if not vehicles:
            email_body = f"Hi, {company.owner.first_name}! \nYou have no unused vehicles in your company."
            send_email_data = {
                'email_body': email_body,
                'email_subject': 'Unused vehicles in your company',
                'to_email': company.owner.email,
            }
            send_email(send_email_data)

        email_body = f"Hi, {company.owner.first_name}! \nYou have vehicles that is on the company balance " \
                     f"but not belongs to any office: \n{vehicle_string_names}"
        send_email_data = {
            'email_body': email_body,
            'email_subject': 'Unused vehicles in your company',
            'to_email': company.owner.email,
        }
        send_email(send_email_data)


@shared_task
def create_vehicle_audit(vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    audit = Audit.objects.create(
        vehicle=vehicle,
        office=vehicle.office,
        company=vehicle.company
    )
    audit.drivers.set(vehicle.drivers.all())
