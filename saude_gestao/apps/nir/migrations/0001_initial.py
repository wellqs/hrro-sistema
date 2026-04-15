from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('setores', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitacaoNIR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('transferencia', 'Transferência para outra unidade'), ('leito_uti', 'Vaga em UTI'), ('leito_enferma', 'Vaga em Enfermaria'), ('procedimento', 'Procedimento Externo'), ('exame', 'Exame Externo'), ('cirurgia', 'Cirurgia Eletiva/Urgência'), ('ambulatorio', 'Consulta Ambulatorial'), ('outro', 'Outro')], max_length=20)),
                ('prioridade', models.CharField(choices=[('eletivo', 'Eletivo'), ('urgencia', 'Urgência'), ('emergencia', 'Emergência')], default='eletivo', max_length=15)),
                ('status', models.CharField(choices=[('solicitado', 'Solicitado'), ('em_regulacao', 'Em Regulação'), ('autorizado', 'Autorizado'), ('negado', 'Negado'), ('cancelado', 'Cancelado'), ('concluido', 'Concluído')], default='solicitado', max_length=15)),
                ('paciente_nome', models.CharField(max_length=200)),
                ('paciente_prontuario', models.CharField(blank=True, max_length=50)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('descricao_clinica', models.TextField(help_text='Resumo clínico do paciente')),
                ('justificativa', models.TextField(help_text='Justificativa da solicitação')),
                ('cid_principal', models.CharField(blank=True, max_length=10, verbose_name='CID Principal')),
                ('destino_solicitado', models.CharField(blank=True, help_text='Hospital, unidade ou serviço solicitado (quando aplicável)', max_length=200)),
                ('data_solicitacao', models.DateField()),
                ('data_regulacao', models.DateField(blank=True, null=True)),
                ('observacoes', models.TextField(blank=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes_nir', to='setores.setor')),
                ('solicitado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitacoes_nir_enviadas', to=settings.AUTH_USER_MODEL)),
                ('regulado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitacoes_nir_reguladas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Solicitação NIR',
                'verbose_name_plural': 'Solicitações NIR',
                'ordering': ['-data_solicitacao', '-criado_em'],
            },
        ),
    ]
