from django.db import migrations

# Nomes copiados de apps.accounts.roles.Role. Migrações não importam código da
# aplicação, porque ele muda com o tempo e a migração precisa continuar igual.
ROLE_NAMES = ["Autores", "Editores"]


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    for name in ROLE_NAMES:
        Group.objects.get_or_create(name=name)


def delete_groups(apps, schema_editor):
    apps.get_model("auth", "Group").objects.filter(name__in=ROLE_NAMES).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [migrations.RunPython(create_groups, delete_groups)]
