# Generated by Django 5.1.3 on 2024-11-17 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0004_empresa_result_alter_user_first_name_alter_user_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='result',
            field=models.CharField(blank=True, choices=[('APROVADO', 'Aprovado'), ('REPROVADO', 'Reprovado'), ('EM ANALISE', 'Em Analise'), ('EM ABERTO', 'Em Aberto')], max_length=100, null=True),
        ),
    ]
