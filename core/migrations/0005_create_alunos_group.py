from django.db import migrations


def create_alunos_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    group, created = Group.objects.get_or_create(name='Alunos')
    
    # Permissões relacionadas a uniformes
    # Formato: (codename, model_name)
    perms_to_add = [
        ('view_uniformitem', 'uniformitem'),
        ('add_uniformorder', 'uniformorder'),
        ('view_uniformorder', 'uniformorder'),
        ('add_uniformorderitem', 'uniformorderitem'),
        ('view_uniformorderitem', 'uniformorderitem'),
    ]
    
    for codename, model in perms_to_add:
        try:
            content_type = ContentType.objects.get(app_label='core', model=model)
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            group.permissions.add(permission)
        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Caso a migração seja rodada em um ambiente onde os modelos ainda não foram registrados no ContentType
            continue


def remove_alunos_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Alunos').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_uniformitem_uniformorder_uniformorderitem'),
    ]

    operations = [
        migrations.RunPython(create_alunos_group, remove_alunos_group),
    ]
