# Generated by Django 4.1.6 on 2023-02-12 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechnicalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='technical_image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='technical_image', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='SpecificationImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='specification_image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spec_image', to='product.product')),
            ],
        ),
    ]
