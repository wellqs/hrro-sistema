from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setor',
            name='tipo',
            field=models.CharField(
                choices=[
                    ('direcao', 'Direção'),
                    ('diretoria', 'Diretoria'),
                    ('gerencia', 'Gerência'),
                    ('assistencial', 'Assistencial'),
                    ('administrativo', 'Administrativo'),
                    ('unidade', 'Unidade'),
                    ('comissao', 'Comissão'),
                    ('nucleo', 'Núcleo'),
                ],
                max_length=20,
            ),
        ),
    ]
