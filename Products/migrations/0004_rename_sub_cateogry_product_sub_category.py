# Generated by Django 5.0 on 2024-09-08 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0003_brand_discount_variantion_product_image_variantvalue_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sub_cateogry',
            new_name='sub_category',
        ),
    ]
