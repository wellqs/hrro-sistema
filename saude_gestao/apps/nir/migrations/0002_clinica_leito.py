from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def populate_clinicas_leitos(apps, schema_editor):
    Clinica = apps.get_model('nir', 'Clinica')
    Leito   = apps.get_model('nir', 'Leito')

    clinicas = [
        {'nome': 'Clínica A', 'capacidade': 38, 'cor': '#185FA5', 'ordem': 1, 'prefixo': 'A'},
        {'nome': 'Clínica B', 'capacidade': 40, 'cor': '#0F6E56', 'ordem': 2, 'prefixo': 'B'},
        {'nome': 'Clínica C', 'capacidade': 47, 'cor': '#534AB7', 'ordem': 3, 'prefixo': 'C'},
        {'nome': 'Extra',     'capacidade':  1, 'cor': '#854F0B', 'ordem': 4, 'prefixo': 'E'},
    ]

    for dados in clinicas:
        prefixo = dados.pop('prefixo')
        clinica = Clinica.objects.create(**dados)
        for i in range(1, clinica.capacidade + 1):
            Leito.objects.create(
                clinica=clinica,
                numero=f'{prefixo}-{i:02d}',
                status='livre',
            )


class Migration(migrations.Migration):

    dependencies = [
        ('nir', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('capacidade', models.PositiveSmallIntegerField()),
                ('cor', models.CharField(default='#185FA5', help_text='Hex color', max_length=7)),
                ('ordem', models.PositiveSmallIntegerField(default=0)),
            ],
            options={'verbose_name': 'Clínica', 'verbose_name_plural': 'Clínicas', 'ordering': ['ordem', 'nome']},
        ),
        migrations.CreateModel(
            name='Leito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10)),
                ('status', models.CharField(
                    choices=[('livre','Livre'),('ocupado','Ocupado'),('reservado','Reservado'),('limpeza','Em Limpeza'),('bloqueado','Bloqueado')],
                    default='livre', max_length=10,
                )),
                ('paciente_nome', models.CharField(blank=True, max_length=200)),
                ('observacao', models.CharField(blank=True, max_length=300)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('clinica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leitos', to='nir.clinica')),
                ('atualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leitos_atualizados', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Leito', 'verbose_name_plural': 'Leitos', 'ordering': ['clinica', 'numero'], 'unique_together': {('clinica', 'numero')}},
        ),
        migrations.RunPython(populate_clinicas_leitos, migrations.RunPython.noop),
    ]
