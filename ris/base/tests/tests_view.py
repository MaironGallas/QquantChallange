import json

import pytest
from django.test import Client
from pytest import fixture
from django.urls import reverse

client = Client()


@pytest.mark.django_db
def test_status_code_get_articles_fields_list():
    """Checks if the endpoint responds 200 Ok"""
    response = client.get(reverse('article_list'))
    assert response.status_code == 200
