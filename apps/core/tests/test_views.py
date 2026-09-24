import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_healthz_checks_the_database(client):
    response = client.get(reverse("healthz"))
    assert response.json() == {"status": "ok"}
