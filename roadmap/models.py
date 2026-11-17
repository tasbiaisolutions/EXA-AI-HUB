from django.db import models
from django.urls import reverse
from .private_storage import PrivateSubmissionStorage


class DatabaseConnectionStatus(models.Model):
    """Tracks whether the cloud database is reachable."""

    SOURCE_CLOUD = 'cloud'
    SOURCE_CHOICES = [
        (SOURCE_CLOUD, 'Cloud Database'),
    ]

    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, unique=True)
    database_name = models.CharField(max_length=255, blank=True, default='')
    host = models.CharField(max_length=255, blank=True, default='')
    is_connected = models.BooleanField(default=False)
    details = models.TextField(blank=True, default='')
    checked_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['source']

    def __str__(self):
        return f"{self.get_source_display()} ({'connected' if self.is_connected else 'offline'})"


class UserGoal(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Not sure', 'Not sure'),
    ]

    goal = models.CharField(max_length=300, help_text="What do you want to become? (e.g., Robotics Engineer)")
    domain = models.CharField(max_length=200, help_text="e.g. Technology, Robotics, Business")
    current_level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Beginner')
    chosen_tier = models.CharField(
        max_length=20,
        choices=[choice for choice in LEVEL_CHOICES if choice[0] != 'Not sure'],
        default='Beginner',
    )
    existing_skills = models.TextField(blank=True, default='', help_text="Skills the user already has")
    user_name = models.CharField(max_length=100, blank=True, default='Learner')
    
    # AI generated roadmap/skill graph metadata
    roadmap_metadata = models.TextField(blank=True, default='', help_text="JSON representation of the EXA generated roadmap")
    expert_agent_name = models.CharField(max_length=100, blank=True, default='EXA Expert', help_text="The dynamically generated complete expert agent (e.g., Technology Expert)")
    expert_agent_intro = models.TextField(blank=True, default='')

    # Course Enrollment & Paid Experience
    enrollment_status = models.CharField(max_length=30, default='enrolled', choices=[('free_preview', 'Free Preview (Level 1)'), ('enrolled', 'Full Course Enrolled')])
    payment_status = models.CharField(max_length=30, default='active', choices=[('pending', 'Pending Verification'), ('active', 'Paid & Active'), ('free_preview', 'Preview Mode')])
    course_price = models.DecimalField(max_digits=8, decimal_places=2, default=49.00)
    certificate_issued = models.BooleanField(default=False)
    certificate_id = models.CharField(max_length=100, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name}'s Goal: {self.goal} ({self.domain})"

    def get_absolute_url(self):
        return reverse('dashboard', kwargs={'pk': self.pk})

    @property
    def progress_percentage(self):
        skills = self.skills_in_chosen_tier()
        total = len(skills)
        if total == 0:
            return 0
        completed = sum(node.status == 'completed' for node in skills)
        return int((completed / total) * 100)
    
    @property
    def current_skill(self):
        """Return the next skill in the selected tier."""
        tier_skills = self.skills_in_chosen_tier()
        for node in tier_skills:
            if node.status == 'in_progress':
                return node
        return next(
            (node for node in tier_skills if node.status == 'not_started'),
            None,
        )

    def skills_in_chosen_tier(self):
        ranges = {
            'Beginner': (1, 4),
            'Intermediate': (5, 8),
            'Advanced': (9, 12),
        }
        first_level, last_level = ranges.get(self.chosen_tier, (1, 4))
        return [
            node for node in self.skill_nodes.all()
            if first_level <= (node.coach_level or node.order) <= last_level
        ]


class SkillNode(models.Model):
    TIER_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, null=True, blank=True, help_text="Learning tier for this skill/module")
    coach_level = models.PositiveIntegerField(null=True, blank=True, help_text="Numeric level 1-12 for the coaching roadmap")
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PHASE_CHOICES = [
        ('assessment', 'Initial Assessment'),
        ('learning', 'Learning Concept'),
        ('quiz', 'Taking Quiz'),
        ('review', 'Review & Improvement'),
        ('completed', 'Concept Mastered'),
    ]

    goal = models.ForeignKey(UserGoal, on_delete=models.CASCADE, related_name='skill_nodes')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    importance = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    phase = models.CharField(max_length=20, choices=PHASE_CHOICES, default='assessment')
    order = models.PositiveIntegerField(default=1)

    @property
    def is_locked(self):
        """Lock levels only behind incomplete projects in the selected tier."""
        if not self.is_in_chosen_tier:
            return True
        level = self.coach_level or self.order
        return any(
            node.status != 'completed' and (node.coach_level or node.order) < level
            for node in self.goal.skills_in_chosen_tier()
        )

    @property
    def is_in_chosen_tier(self):
        level = self.coach_level or self.order
        ranges = {
            'Beginner': (1, 4),
            'Intermediate': (5, 8),
            'Advanced': (9, 12),
        }
        first_level, last_level = ranges.get(self.goal.chosen_tier, (1, 4))
        return first_level <= level <= last_level

    @property
    def level_number(self):
        return self.order
    
    # Expert agent data
    theory_json = models.JSONField(default=dict, blank=True, help_text="Concept, 1-2 line explanation, Example, Practice prompt")
    resources_json = models.JSONField(default=list, blank=True, help_text="Relevant prioritized resources")
    project_json = models.JSONField(default=dict, blank=True, help_text="Mini project definition")

    # Skill map generated from assessment
    skill_map_json = models.JSONField(default=list, blank=True, help_text="List of sub-concepts to master in this skill")
    current_concept_index = models.PositiveIntegerField(default=0, help_text="Which concept in skill_map_json the user is currently on")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.goal.goal})"

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def current_concept(self):
        """Returns the current sub-concept dict from the skill map, or None."""
        if self.skill_map_json and self.current_concept_index < len(self.skill_map_json):
            return self.skill_map_json[self.current_concept_index]
        return None

    @property
    def total_concepts(self):
        return len(self.skill_map_json) if self.skill_map_json else 0

    @property
    def concepts_completed(self):
        return self.current_concept_index

    @property
    def phase_display(self):
        icons = {
            'assessment': '📋 Assessment',
            'learning': '📖 Learning',
            'quiz': '❓ Quiz',
            'review': '🔄 Review',
            'completed': '✅ Mastered',
        }
        return icons.get(self.phase, self.phase)


class LearningUnit(models.Model):
    UNIT_TYPES = [
        ('theory', 'Theory & Concept'),
        ('practice', 'Immediate Practice'),
        ('project', 'Project / Build'),
        ('evaluation', 'Evaluation'),
    ]

    skill_node = models.ForeignKey(SkillNode, on_delete=models.CASCADE, related_name='units')
    title = models.CharField(max_length=255)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES, default='theory')
    
    # LESS CONTENT. MORE PROGRESS. fields
    concept = models.TextField(blank=True, default='')
    why_it_matters = models.TextField(blank=True, default='')
    example = models.TextField(blank=True, default='')
    quick_tip = models.TextField(blank=True, default='')
    practice_prompt = models.TextField(blank=True, default='')
    
    completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        return f"{status} ({self.unit_type}) {self.title}"

class Project(models.Model):
    goal = models.ForeignKey(UserGoal, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    objective = models.TextField(blank=True, default='')
    requirements = models.TextField(blank=True, default='')
    level = models.CharField(max_length=50, default='Mini Project')
    status = models.CharField(max_length=50, default='Not Started')
    evaluation_criteria = models.TextField(blank=True, default='')
    submission_text = models.TextField(blank=True, default='', help_text="User's submitted code, queries, or link")
    feedback = models.TextField(blank=True, default='', help_text="AI mentor evaluation and rubric feedback")
    score = models.IntegerField(default=0, help_text="Score out of 100")

    def __str__(self):
        return f"Project: {self.title} ({self.status})"


class ProjectSubmission(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('evaluated', 'Evaluated'),
        ('evaluation_failed', 'Evaluation Failed'),
        ('rejected', 'Rejected'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='submissions')
    report = models.FileField(storage=PrivateSubmissionStorage(), upload_to='reports/%Y/%m/%d/', blank=True)
    video = models.FileField(storage=PrivateSubmissionStorage(), upload_to='videos/%Y/%m/%d/', blank=True)
    github_url = models.URLField(blank=True, default='')
    live_url = models.URLField(blank=True, default='')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='received')
    evaluation_json = models.JSONField(default=dict, blank=True)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Submission {self.pk} for {self.project_id} ({self.status})"


class ChatMessage(models.Model):
    PANEL_CHOICES = [('teacher', 'Teacher'), ('expert', 'Expert')]
    ROLE_CHOICES = [('user', 'User'), ('assistant', 'Assistant')]

    user = models.ForeignKey(UserGoal, on_delete=models.CASCADE, related_name='chat_messages')
    domain = models.CharField(max_length=100)
    level = models.PositiveIntegerField(null=True, blank=True)
    panel = models.CharField(max_length=20, choices=PANEL_CHOICES)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'pk']
        indexes = [models.Index(fields=['user', 'panel', 'created_at'])]

    def __str__(self):
        return f"{self.panel} {self.role} message for goal {self.user_id}"


class SystemAdminLog(models.Model):
    category = models.CharField(max_length=60)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category}: {self.message[:80]}"

class Assessment(models.Model):
    goal = models.ForeignKey(UserGoal, on_delete=models.CASCADE, related_name='assessments')
    skill_node = models.ForeignKey(SkillNode, on_delete=models.CASCADE, null=True, blank=True)
    feedback = models.TextField(blank=True, default='')
    weakness_detected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Assessment for {self.goal.user_name} ({'Weakness' if self.weakness_detected else 'Pass'})"


class SkillAssessment(models.Model):
    """Initial assessment when user starts a skill — captures what they already know."""
    skill_node = models.ForeignKey(SkillNode, on_delete=models.CASCADE, related_name='skill_assessments')
    questions_json = models.JSONField(default=list, help_text="Assessment questions generated by AI")
    answers_json = models.JSONField(default=list, help_text="User's answers to assessment questions")
    result_summary = models.TextField(blank=True, default='', help_text="AI summary of user's current knowledge")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Skill Assessment: {self.skill_node.name}"


class QuizQuestion(models.Model):
    """Individual MCQ question for a concept quiz (5 per concept)."""
    skill_node = models.ForeignKey(SkillNode, on_delete=models.CASCADE, related_name='quiz_questions')
    concept_index = models.PositiveIntegerField(default=0, help_text="Which concept this question is for")
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, help_text="A, B, C, or D")
    explanation = models.TextField(blank=True, default='', help_text="Why this answer is correct")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."


class QuizAttempt(models.Model):
    """Tracks each quiz attempt for a concept."""
    skill_node = models.ForeignKey(SkillNode, on_delete=models.CASCADE, related_name='quiz_attempts')
    concept_index = models.PositiveIntegerField(default=0)
    answers_json = models.JSONField(default=list, help_text="List of user's selected answers")
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=5)
    is_passed = models.BooleanField(default=False)
    feedback_json = models.JSONField(default=list, help_text="Per-question feedback")
    mentor_message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = "PASSED" if self.is_passed else "NEEDS REVIEW"
        return f"Quiz {status}: {self.score}/{self.total} for {self.skill_node.name}"

    @property
    def is_perfect(self):
        return self.score == self.total


class ConceptMasteryAttempt(models.Model):
    """Evidence that a learner can apply one concept, beyond selecting an MCQ answer."""
    skill_node = models.ForeignKey(SkillNode, on_delete=models.CASCADE, related_name='mastery_attempts')
    concept_index = models.PositiveIntegerField()
    response = models.TextField()
    score = models.PositiveIntegerField(default=0, help_text='Application rubric score out of 100')
    is_mastered = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, default='')
    evidence_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['skill_node', 'concept_index', 'created_at'])]

    def __str__(self):
        return f"Mastery {'passed' if self.is_mastered else 'needs work'}: {self.skill_node.name}"
