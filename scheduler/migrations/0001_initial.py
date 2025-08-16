from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="SchedulerControl",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("is_paused", models.BooleanField(default=False)),
            ],
            options={"db_table": "ai_scheduler_control"},
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=120, unique=True)),
                ("handler", models.CharField(max_length=255)),
                ("args", models.JSONField(default=dict, blank=True)),
                ("tenant_schema", models.CharField(max_length=63, null=True, blank=True)),
                ("interval_seconds", models.PositiveIntegerField(default=5)),
                ("enabled", models.BooleanField(default=True)),
                ("next_run_at", models.DateTimeField(null=True, blank=True)),
                ("last_run_at", models.DateTimeField(null=True, blank=True)),
                ("lock_until", models.DateTimeField(null=True, blank=True)),
                ("max_runtime_seconds", models.PositiveIntegerField(default=55)),
                ("consecutive_failures", models.PositiveIntegerField(default=0)),
            ],
            options={"db_table": "ai_job"},
        ),
    ]
