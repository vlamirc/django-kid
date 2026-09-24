from apps.accounts.tests.factories import UserFactory


def test_display_name_prefers_full_name():
    user = UserFactory.build(username="ana", first_name="Ana", last_name="Silva")
    assert user.display_name == "Ana Silva"


def test_display_name_falls_back_to_username():
    assert UserFactory.build(username="ana").display_name == "ana"
