import roadmap.private_storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('roadmap', '0013_reapply_build_lab_briefs')]

    operations = [
        migrations.CreateModel(
            name='ProjectSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.FileField(blank=True, storage=roadmap.private_storage.PrivateSubmissionStorage(), upload_to='reports/%Y/%m/%d/')),
                ('video', models.FileField(blank=True, storage=roadmap.private_storage.PrivateSubmissionStorage(), upload_to='videos/%Y/%m/%d/')),
                ('github_url', models.URLField(blank=True, default='')),
                ('live_url', models.URLField(blank=True, default='')),
                ('status', models.CharField(choices=[('received', 'Received'), ('evaluated', 'Evaluated'), ('evaluation_failed', 'Evaluation Failed'), ('rejected', 'Rejected')], default='received', max_length=30)),
                ('evaluation_json', models.JSONField(blank=True, default=dict)),
                ('score', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='roadmap.project')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
