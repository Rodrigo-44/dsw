import pytest
from pytest_django.asserts import assertContains, assertNotContains

from appointments.models import Appointment
from factories import AppointmentFactory
from tests import conftest

# ==============================================================================
# APPOINTMENT LIST
# ==============================================================================


@pytest.mark.django_db
def test_appointment_list_requires_authentication(client):
    response = client.get(conftest.APPOINTMENT_LIST_URL)
    assert response.status_code == 302
    assert response.url.startswith(conftest.LOGIN_URL)


@pytest.mark.django_db
def test_appointment_list_page_contains_expected_appointments(client, user, another_user):
    appointments = AppointmentFactory.create_batch(5, user=user)
    another_appointments = AppointmentFactory.create_batch(5, user=another_user)

    client.force_login(user)

    response = client.get(conftest.APPOINTMENT_LIST_URL)
    assert response.status_code == 200

    for appointment in appointments:
        assertContains(response, conftest.str(appointment))
        assertContains(
            response, conftest.APPOINTMENT_DETAIL_URL.format(appointment_pk=appointment.pk)
        )

    for appointment in another_appointments:
        assertNotContains(response, conftest.str(appointment))
        assertNotContains(
            response, conftest.APPOINTMENT_DETAIL_URL.format(appointment_pk=appointment.pk)
        )


@pytest.mark.django_db
def test_appointment_list_page_shows_appointments_in_order_with_same_slot(client, user, slot):
    appointment_earlier = AppointmentFactory(user=user, date='2024-09-04', slot=slot)
    appointment_later = AppointmentFactory(user=user, date='2024-09-05', slot=slot)

    client.force_login(user)

    response = client.get(conftest.APPOINTMENT_LIST_URL)
    assert response.status_code == 200

    content = response.content.decode()

    pos_earlier = content.index(conftest.str(appointment_earlier))
    pos_later = content.index(conftest.str(appointment_later))

    assert pos_earlier < pos_later


@pytest.mark.django_db
def test_appointment_list_page_shows_appointments_in_order_with_different_slots(
    client, user, slot, another_slot
):
    appointment_earlier = AppointmentFactory(user=user, date='2024-09-04', slot=slot)
    appointment_later = AppointmentFactory(user=user, date='2024-09-04', slot=another_slot)

    client.force_login(user)

    response = client.get(conftest.APPOINTMENT_LIST_URL)
    assert response.status_code == 200

    content = response.content.decode()

    pos_earlier = content.index(conftest.str(appointment_earlier))
    pos_later = content.index(conftest.str(appointment_later))

    assert pos_earlier < pos_later


@pytest.mark.django_db
def test_appointment_list_page_shows_no_appointments_message(client, user):
    client.force_login(user)

    response = client.get(conftest.APPOINTMENT_LIST_URL)
    assert response.status_code == 200
    assertContains(response, 'No appointments found')


@pytest.mark.django_db
def test_appointment_list_page_contains_add_appointment_link(client, user):
    client.force_login(user)

    response = client.get(conftest.APPOINTMENT_LIST_URL)
    assert response.status_code == 200
    assertContains(response, conftest.APPOINTMENT_ADD_URL)


# ==============================================================================
# APPOINTMENT DETAIL
# ==============================================================================


@pytest.mark.django_db
def test_appointment_detail_requires_authentication(client, appointment):
    url = conftest.APPOINTMENT_DETAIL_URL.format(appointment_pk=appointment.pk)
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == f'/login/?next={url}'


@pytest.mark.django_db
def test_appointment_detail_page_shows_appointment_details(client, appointment):
    client.force_login(appointment.user)

    url = conftest.APPOINTMENT_DETAIL_URL.format(appointment_pk=appointment.pk)
    response = client.get(url)
    assert response.status_code == 200
    assertContains(response, f'Date: {appointment.date}')
    assertContains(response, f'Slot: {conftest.str_slot(appointment.slot)}')


@pytest.mark.django_db
def test_appointment_detail_page_forbids_access_to_other_users(client, appointment, another_user):
    client.force_login(another_user)

    url = conftest.APPOINTMENT_DETAIL_URL.format(appointment_pk=appointment.pk)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_appointment_detail_page_contains_link_back_to_appointment_list(client, appointment):
    client.force_login(appointment.user)

    url = conftest.APPOINTMENT_DETAIL_URL.format(appointment_pk=appointment.pk)
    response = client.get(url)
    assert response.status_code == 200
    assertContains(response, conftest.APPOINTMENT_LIST_URL)


# ==============================================================================
# ADD APPOINTMENT
# ==============================================================================


@pytest.mark.django_db
def test_add_appointment_requires_authentication(client):
    url = conftest.APPOINTMENT_ADD_URL
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == f'/login/?next={url}'


@pytest.mark.django_db
def test_add_appointment_page_contains_form(client, user):
    client.force_login(user)

    url = conftest.APPOINTMENT_ADD_URL
    response = client.get(url)
    assert response.status_code == 200
    assertContains(response, '<form')
    assertContains(response, 'novalidate')
    assertContains(response, 'name="date"')
    assertContains(response, 'name="slot"')


@pytest.mark.django_db
def test_add_appointment_page_submits_form_and_creates_appointment(client, user, slot):
    client.force_login(user)

    url = conftest.APPOINTMENT_ADD_URL
    form_data = {
        'date': '2024-12-25',
        'slot': slot.pk,
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 302

    appointment = Appointment.objects.get(user=user, date='2024-12-25', slot=slot)
    assert response.url == conftest.APPOINTMENT_DETAIL_URL.format(appointment_pk=appointment.pk)


@pytest.mark.django_db
def test_add_appointment_page_contains_link_back_to_appointment_list(client, user):
    client.force_login(user)

    url = conftest.APPOINTMENT_ADD_URL
    response = client.get(url)
    assert response.status_code == 200
    assertContains(response, conftest.APPOINTMENT_LIST_URL)


@pytest.mark.django_db
def test_add_appointment_page_shows_errors_for_invalid_form_submission_empty_date(
    client, user, slot
):
    client.force_login(user)

    url = conftest.APPOINTMENT_ADD_URL
    form_data = {
        'date': '',
        'slot': slot.pk,
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 200
    assertContains(response, 'This field is required.')


@pytest.mark.django_db
def test_add_appointment_page_shows_errors_for_invalid_form_submission_empty_slot(client, user):
    client.force_login(user)

    url = conftest.APPOINTMENT_ADD_URL
    form_data = {
        'date': '2024-12-25',
        'slot': '',
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 200
    assertContains(response, 'This field is required.')
