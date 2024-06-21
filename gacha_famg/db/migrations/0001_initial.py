# Generated by Django 5.0.6 on 2024-06-21 18:18

import db.util
import db.validate
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hid', models.CharField(default=db.util.generate_hid, editable=False, max_length=10, unique=True, verbose_name='Home ID')),
                ('name', models.CharField(max_length=150, verbose_name='名前')),
            ],
            options={
                'verbose_name': 'ホーム',
                'verbose_name_plural': 'ホーム',
                'db_table': 'homes',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='カテゴリ名')),
                ('priority', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(32767)], verbose_name='表示優先度')),
                ('text_color', models.CharField(default='#0D0D0D', max_length=7, verbose_name='テキストカラー')),
                ('bg_color', models.CharField(default='#DAD5D2', max_length=7, verbose_name='背景カラー')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.home')),
            ],
            options={
                'verbose_name': 'カテゴリー',
                'verbose_name_plural': 'カテゴリー',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='HomeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.home')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ホームに所属するユーザー',
                'verbose_name_plural': 'ホームに所属するユーザー',
                'db_table': 'home_users',
            },
        ),
        migrations.AddField(
            model_name='home',
            name='users',
            field=models.ManyToManyField(through='db.HomeUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PurchaseRecordMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_month', models.CharField(default=db.util.default_year_month, max_length=7, validators=[db.validate.validate_year_month_format], verbose_name='年月')),
                ('date', models.DateField(default=db.util.defualt_year_month_start_date, verbose_name='月初の日付')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.home')),
            ],
            options={
                'verbose_name': '購入記録の月管理',
                'verbose_name_plural': '購入記録の月管理',
                'db_table': 'purchase_record_months',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='日付')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.home')),
            ],
            options={
                'verbose_name': 'レシート',
                'verbose_name_plural': 'レシート',
                'db_table': 'receipts',
            },
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField(verbose_name='詳細')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='金額')),
                ('discount', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='割引額')),
                ('note', models.TextField(blank=True, null=True, verbose_name='備考')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.category')),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.receipt')),
            ],
            options={
                'verbose_name': '購入品記録',
                'verbose_name_plural': '購入品記録',
                'db_table': 'purchase_items',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='ショップ名')),
                ('priority', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(32767)], verbose_name='表示優先度')),
                ('text_color', models.CharField(default='#0D0D0D', max_length=7, verbose_name='テキストカラー')),
                ('bg_color', models.CharField(default='#DAD5D2', max_length=7, verbose_name='背景カラー')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.home')),
            ],
            options={
                'verbose_name': 'ショップ',
                'verbose_name_plural': 'ショップ',
                'db_table': 'shops',
            },
        ),
        migrations.AddField(
            model_name='receipt',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.shop'),
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('home', 'name'), name='unique_home_category_name'),
        ),
        migrations.AddConstraint(
            model_name='homeuser',
            constraint=models.UniqueConstraint(fields=('home', 'user'), name='unique_home_user'),
        ),
        migrations.AddConstraint(
            model_name='shop',
            constraint=models.UniqueConstraint(fields=('home', 'name'), name='unique_home_shop'),
        ),
    ]
