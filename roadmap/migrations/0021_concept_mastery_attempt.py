from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0020_refresh_electronics_typo_goals'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConceptMasteryAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concept_index', models.PositiveIntegerField()),
                ('response', models.TextField()),
                ('score', models.PositiveIntegerField(default=0, help_text='Application rubric score out of 100')),
                ('is_mastered', models.BooleanField(default=False)),
                ('feedback', models.TextField(blank=True, default='')),
                ('evidence_json', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('skill_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mastery_attempts', to='roadmap.skillnode')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.AddIndex(
            model_name='conceptmasteryattempt',
            index=models.Index(fields=['skill_node', 'concept_index', 'created_at'], name='roadmap_con_skill_n_7be43c_idx'),
        ),
    ]
