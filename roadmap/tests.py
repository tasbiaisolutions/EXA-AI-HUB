import json

from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.sessions.backends.base import SessionBase
from django.urls import reverse
from unittest.mock import patch
from .models import UserGoal, SkillNode, QuizQuestion, QuizAttempt, Project, ProjectSubmission
from .models import ChatMessage
from .ai_service import (
    EXAOrchestrator,
    generate_lesson_for_domain,
    generate_quiz_for_domain,
)
from .course_content import RESTRUCTURED_CURRICULA
from .course_teaching import get_course_guide
from .submission_scanner import (
    MAX_REPORT_BYTES, MAX_VIDEO_BYTES, SubmissionScanner, SubmissionValidationError,
    validate_pdf, validate_video, validate_video_duration,
)
from .groq_client import GroqClient


class MentorFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.goal = UserGoal.objects.create(
            user_name="Alex",
            domain="Backend Engineering",
            current_level="beginner",
            goal="Master REST APIs & Databases",
            existing_skills="Python syntax"
        )
        self.skill = SkillNode.objects.create(
            goal=self.goal,
            name="API Fundamentals",
            description="Understand HTTP methods and REST concepts",
            importance="Core foundation for all backend work",
            order=1
        )

    def test_initial_skill_node_phase(self):
        self.assertEqual(self.skill.phase, 'assessment')
        self.assertEqual(self.skill.status, 'not_started')

    def test_skill_assessment_get_and_post(self):
        # 1. GET assessment page
        response = self.client.get(reverse('skill_assessment', kwargs={'pk': self.skill.pk}))
        self.assertContains(response, "Before we start: API Fundamentals")
        self.assertContains(response, "No grades")

        # 2. POST assessment answers
        post_data = {
            'answer_0': 'HTTP is a protocol for web communication',
            'answer_1': 'GET and POST',
            'answer_2': 'JSON formatted data'
        }
        post_response = self.client.post(reverse('skill_assessment', kwargs={'pk': self.skill.pk}), post_data)
        self.assertRedirects(post_response, reverse('concept_overview', kwargs={'pk': self.skill.pk}))

        # Verify SkillNode was updated to learning phase and has concepts
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.phase, 'learning')
        self.assertEqual(self.skill.status, 'in_progress')
        self.assertGreater(len(self.skill.skill_map_json), 0)

    def test_skill_map_view(self):
        self.skill.skill_map_json = [
            {'name': 'HTTP Methods', 'description': 'GET, POST, PUT, DELETE', 'importance': 'Crucial', 'order': 1},
            {'name': 'Status Codes', 'description': '200, 404, 500', 'importance': 'Crucial', 'order': 2}
        ]
        self.skill.save()

        response = self.client.get(reverse('skill_map', kwargs={'pk': self.skill.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HTTP Methods")
        self.assertContains(response, "Status Codes")

    def test_teach_concept_view(self):
        self.skill.skill_map_json = [
            {'name': 'HTTP Methods', 'description': 'GET, POST, PUT, DELETE', 'importance': 'Crucial', 'order': 1}
        ]
        self.skill.save()

        response = self.client.get(reverse('teach_concept', kwargs={'pk': self.skill.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HTTP Methods")
        self.assertContains(response, "Take the 5-Question Quiz")
        self.assertNotContains(response, "Mentor's Pro Tip & Gotchas")

    def test_quiz_generation_and_perfect_score_applause(self):
        self.skill.skill_map_json = [
            {'name': 'HTTP Methods', 'description': 'GET, POST, PUT, DELETE', 'importance': 'Crucial', 'order': 1}
        ]
        self.skill.save()

        # GET quiz page -> generates 5 questions
        response = self.client.get(reverse('quiz', kwargs={'pk': self.skill.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "5-Question Assessment")

        questions = QuizQuestion.objects.filter(skill_node=self.skill, concept_index=0)
        self.assertEqual(questions.count(), 5)

        # POST 5 correct answers
        post_data = {}
        for q in questions:
            post_data[f'question_{q.pk}'] = q.correct_answer

        submit_resp = self.client.post(reverse('quiz_submit', kwargs={'pk': self.skill.pk}), post_data)
        self.assertEqual(submit_resp.status_code, 302)

        attempt = QuizAttempt.objects.filter(skill_node=self.skill).first()
        self.assertIsNotNone(attempt)
        self.assertEqual(attempt.score, 5)
        self.assertTrue(attempt.is_passed)

        # View results page -> should show the score outcome.
        result_resp = self.client.get(reverse('quiz_result', kwargs={'pk': attempt.pk}))
        self.assertEqual(result_resp.status_code, 200)
        self.assertContains(result_resp, "PERFECT SCORE")
        self.assertTrue(attempt.is_passed)

    def test_outliers_lesson_and_quiz_are_topic_specific(self):
        lesson = generate_lesson_for_domain(
            "Outliers", "Level 5: Statistics for analysts", "data_analytics", "Intermediate"
        )
        questions = generate_quiz_for_domain(
            "Outliers", "Level 5: Statistics for analysts", "data_analytics", "Intermediate"
        )

        self.assertIn("iqr", lesson["code_example"].lower())
        self.assertIn("do not delete", lesson["pro_tip"].lower())
        self.assertNotIn("SELECT", lesson["code_example"])
        self.assertEqual(len(questions), 5)
        self.assertTrue(all("outliers" in q["question_text"].lower() for q in questions))
        self.assertEqual(len({q["question_text"] for q in questions}), 5)

    def test_course_lessons_and_quizzes_cover_every_concept_uniquely(self):
        for domain, curriculum in RESTRUCTURED_CURRICULA.items():
            all_questions = set()
            for level in curriculum["levels"]:
                for concept in level["concepts"]:
                    guide = get_course_guide(domain, level["name"], concept)
                    self.assertIsNotNone(guide, f"Missing topic guide: {domain} / {level['name']} / {concept}")

                    lesson = generate_lesson_for_domain(
                        concept, level["name"], domain, level["tier"]
                    )
                    self.assertIn(concept, lesson["core_concept"])
                    self.assertTrue(lesson["code_example"])
                    self.assertTrue(lesson["thinking_exercise"])

                    questions = generate_quiz_for_domain(
                        concept, level["name"], domain, level["tier"]
                    )
                    self.assertGreaterEqual(len(questions), 3)
                    self.assertLessEqual(len(questions), 5)
                    question_texts = {question["question_text"] for question in questions}
                    self.assertEqual(len(question_texts), len(questions))
                    self.assertFalse(all_questions.intersection(question_texts))
                    all_questions.update(question_texts)
                    for question in questions:
                        options = [
                            question[f"option_{letter}"] for letter in "abcd"
                        ]
                        self.assertEqual(len(set(options)), 4)
                        self.assertIn(question["correct_answer"], "ABCD")

    def test_quiz_view_replaces_cached_generic_questions(self):
        self.goal.domain = "Data Analyst"
        self.goal.chosen_tier = "Intermediate"
        self.goal.save()
        self.skill.name = "Level 5: Statistics for analysts"
        self.skill.order = 5
        self.skill.coach_level = 5
        self.skill.tier = "Intermediate"
        self.skill.skill_map_json = [{"name": "Outliers"}]
        self.skill.save()
        for order in range(1, 6):
            QuizQuestion.objects.create(
                skill_node=self.skill,
                concept_index=0,
                question_text=f"What is the purpose of Outliers? Generic question {order}",
                option_a="Generic option A",
                option_b="Generic option B",
                option_c="Generic option C",
                option_d="Generic option D",
                correct_answer="A",
                order=order,
            )

        response = self.client.get(reverse("quiz", kwargs={"pk": self.skill.pk}))
        self.assertEqual(response.status_code, 200)
        refreshed = QuizQuestion.objects.filter(
            skill_node=self.skill, concept_index=0
        )
        self.assertEqual(refreshed.count(), 5)
        refreshed_content = " ".join(
            value
            for question in refreshed
            for value in (
                question.question_text,
                question.option_a,
                question.option_b,
                question.option_c,
                question.option_d,
                question.explanation,
            )
        )
        self.assertIn("iqr", refreshed_content.lower())
        self.assertFalse(any("Generic question" in q for q in refreshed.values_list("question_text", flat=True)))

    def test_quiz_failed_score_mentor_review(self):
        self.skill.skill_map_json = [
            {'name': 'HTTP Methods', 'description': 'GET, POST, PUT, DELETE', 'importance': 'Crucial', 'order': 1}
        ]
        self.skill.save()

        # Trigger quiz generation
        self.client.get(reverse('quiz', kwargs={'pk': self.skill.pk}))
        questions = QuizQuestion.objects.filter(skill_node=self.skill, concept_index=0)

        # Answer with wrong choice
        post_data = {}
        for q in questions:
            wrong_choice = 'B' if q.correct_answer != 'B' else 'C'
            post_data[f'question_{q.pk}'] = wrong_choice

        submit_resp = self.client.post(reverse('quiz_submit', kwargs={'pk': self.skill.pk}), post_data)
        self.assertEqual(submit_resp.status_code, 302)

        attempt = QuizAttempt.objects.filter(skill_node=self.skill).first()
        self.assertFalse(attempt.is_passed)
        self.assertEqual(attempt.score, 0)

        # View results page -> should guide to review and retake
        result_resp = self.client.get(reverse('quiz_result', kwargs={'pk': attempt.pk}))
        self.assertEqual(result_resp.status_code, 200)
        self.assertContains(result_resp, "Mentor Review & Guidance")
        self.assertContains(result_resp, "Review Weak Areas & Re-learn")
        self.assertNotContains(result_resp, 'Correct Answer:')

    def test_review_view(self):
        self.skill.skill_map_json = [
            {'name': 'HTTP Methods', 'description': 'GET, POST, PUT, DELETE', 'importance': 'Crucial', 'order': 1}
        ]
        self.skill.phase = 'review'
        self.skill.save()

        # Create a failed attempt
        QuizAttempt.objects.create(
            skill_node=self.skill,
            concept_index=0,
            answers_json=['B', 'B', 'B', 'B', 'B'],
            score=0,
            total=5,
            is_passed=False,
            feedback_json=[{
                'question_text': 'What method fetches data?',
                'user_answer': 'B',
                'correct_answer': 'A',
                'is_correct': False,
                'explanation': 'GET retrieves representations of resources'
            }],
            mentor_message='Review the core HTTP methods.'
        )

        resp = self.client.get(reverse('review', kwargs={'pk': self.skill.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Targeted Re-Teaching")
        self.assertContains(resp, "Retake Quiz Now")

    def test_strict_learning_gate_blocks_advance_without_passing_quiz(self):
        self.skill.skill_map_json = [
            {'name': 'Concept 1', 'description': 'Intro', 'importance': 'Base', 'order': 1},
            {'name': 'Concept 2', 'description': 'Advanced', 'importance': 'Pro', 'order': 2}
        ]
        self.skill.current_concept_index = 0
        self.skill.save()

        # Advancing without passing quiz is strictly blocked!
        advance_resp = self.client.get(reverse('advance_concept', kwargs={'pk': self.skill.pk}))
        self.assertRedirects(advance_resp, reverse('quiz', kwargs={'pk': self.skill.pk}))
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.current_concept_index, 0)

    def test_advance_concept_and_project_redirect(self):
        self.skill.project_json = {
            'is_active': True, 'title': 'Test project', 'objective': 'Test objective',
            'requirements': 'Test requirements', 'requirements_list': ['one'],
            'requirement_evidence': [{'id': 'R1'}],
        }
        self.skill.save(update_fields=['project_json'])
        self.skill.skill_map_json = [
            {'name': 'Concept 1', 'description': 'Intro', 'importance': 'Base', 'order': 1},
            {'name': 'Concept 2', 'description': 'Advanced', 'importance': 'Pro', 'order': 2}
        ]
        self.skill.current_concept_index = 0
        self.skill.save()

        # Pass concept 0 quiz
        QuizAttempt.objects.create(
            skill_node=self.skill,
            concept_index=0,
            answers_json=['A', 'A', 'A', 'A', 'A'],
            score=5,
            total=5,
            is_passed=True
        )

        # Advance to concept 1
        advance_resp = self.client.get(reverse('advance_concept', kwargs={'pk': self.skill.pk}))
        self.assertRedirects(advance_resp, reverse('teach_concept', kwargs={'pk': self.skill.pk}))
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.current_concept_index, 1)

        # Pass concept 1 quiz
        QuizAttempt.objects.create(
            skill_node=self.skill,
            concept_index=1,
            answers_json=['A', 'A', 'A', 'A', 'A'],
            score=5,
            total=5,
            is_passed=True
        )

        # When all concepts are finished, strictly redirects to Level Project!
        advance_resp2 = self.client.get(reverse('advance_concept', kwargs={'pk': self.skill.pk}))
        self.assertRedirects(advance_resp2, reverse('project', kwargs={'pk': self.goal.pk}))

    def test_level_project_and_strict_level_locks(self):
        # Create Level 2
        level2 = SkillNode.objects.create(
            goal=self.goal,
            name="Level 2: Advanced APIs",
            description="Caching, Auth, Rate Limiting",
            importance="Production grade",
            order=2
        )

        # Level 2 must be strictly locked because Level 1 is not completed
        self.assertTrue(level2.is_locked)
        resp_locked = self.client.get(reverse('teach_concept', kwargs={'pk': level2.pk}))
        self.assertRedirects(resp_locked, reverse('dashboard', kwargs={'pk': self.goal.pk}))

        # Submit and pass Level 1 project
        self.skill.project_json = {
            'is_active': True, 'title': 'Test project', 'objective': 'Test objective',
            'requirements': 'Test requirements', 'requirements_list': ['one'],
            'requirement_evidence': [{'id': 'R1'}],
        }
        self.skill.save(update_fields=['project_json'])
        submit_resp = self.client.post(
            reverse('project', kwargs={'pk': self.goal.pk}), {'submission_text': 'text-only submissions cannot pass'}
        )
        self.assertEqual(submit_resp.status_code, 302)

        # Text-only legacy submission cannot mark a Build Lab project complete.
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.status, 'not_started')
        self.assertTrue(level2.is_locked)

    def test_personal_ai_teacher_chat(self):
        self.goal.domain = 'Data Analyst'
        self.goal.goal = 'Become a Data Analyst'
        self.goal.save(update_fields=['domain', 'goal'])
        reply = 'XLOOKUP searches for a value and returns its matching result. Which two columns are you matching?'
        with patch('roadmap.views.GroqClient.complete', return_value=reply) as complete:
            resp = self.client.post(
                reverse('expert_chat', kwargs={'pk': self.goal.pk}),
                data=json.dumps({'message': 'Can you explain Excel XLOOKUP simply?', 'panel': 'teacher'}),
                content_type='application/json'
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['reply'], reply)
        self.assertEqual(complete.call_args.kwargs['model'], GroqClient.teacher_model())
        prompt = complete.call_args.kwargs['system_prompt']
        request_context = json.loads(complete.call_args.kwargs['messages'][0]['content'])
        self.assertIn('patient senior teacher', prompt)
        self.assertEqual(request_context['domain'], 'Data Analyst')
        self.assertEqual(request_context['learner_question'], 'Can you explain Excel XLOOKUP simply?')
        self.assertEqual(ChatMessage.objects.filter(user=self.goal).count(), 2)

    def test_teacher_and_expert_use_distinct_prompts_and_current_context(self):
        self.goal.domain = 'Data Analyst'
        self.skill.name = 'Level 1: Data Analyst Foundations'
        self.skill.coach_level = 1
        self.skill.skill_map_json = [{'name': 'Spreadsheet formulas'}]
        self.goal.save(update_fields=['domain'])
        self.skill.save()
        prompts = []
        def answer(**kwargs):
            prompts.append(kwargs)
            return 'Start with one small example, then check the result against the source rows.'
        with patch('roadmap.views.GroqClient.complete', side_effect=answer):
            for panel in ('teacher', 'expert'):
                response = self.client.post(
                    reverse('expert_chat', kwargs={'pk': self.goal.pk}),
                    data=json.dumps({'message': 'How should I start?', 'panel': panel}),
                    content_type='application/json'
                )
                self.assertEqual(response.status_code, 200)
        self.assertNotEqual(prompts[0]['system_prompt'], prompts[1]['system_prompt'])
        self.assertEqual(prompts[0]['model'], GroqClient.teacher_model())
        self.assertEqual(prompts[1]['model'], GroqClient.expert_model())
        context = json.loads(prompts[0]['messages'][0]['content'])
        self.assertEqual(context['level_number'], 1)
        self.assertEqual(context['current_topic'], 'Spreadsheet formulas')
        self.assertEqual(ChatMessage.objects.filter(user=self.goal, role='assistant').count(), 2)

    def test_generic_chat_reply_retries_once(self):
        with patch('roadmap.views.GroqClient.complete', side_effect=[
            'Great question! Let me know if you need more help.',
            'Check whether your lookup value appears in the first column of the selected range. What value will you test?'
        ]) as complete:
            response = self.client.post(
                reverse('expert_chat', kwargs={'pk': self.goal.pk}),
                data=json.dumps({'message': 'How do I debug a lookup?', 'panel': 'teacher'}),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(complete.call_count, 2)
        self.assertEqual(ChatMessage.objects.filter(user=self.goal).count(), 2)

    def test_missing_groq_key_uses_course_grounded_local_teacher_reply(self):
        with patch('roadmap.groq_client.GroqClient._api_key', return_value=''):
            response = self.client.post(
                reverse('expert_chat', kwargs={'pk': self.goal.pk}),
                data=json.dumps({'message': 'Can you help?', 'panel': 'teacher'}),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['reply'])
        self.assertEqual(response.json()['panel'], 'teacher')
        self.assertEqual(ChatMessage.objects.filter(user=self.goal).count(), 2)

    def test_missing_groq_key_uses_clear_local_expert_reply(self):
        self.goal.domain = 'Data Analyst'
        self.skill.name = 'Level 1: Data Analyst Foundations'
        self.skill.coach_level = 1
        self.skill.skill_map_json = [{'name': 'Spreadsheet formulas'}]
        self.goal.save(update_fields=['domain'])
        self.skill.save()
        with patch('roadmap.groq_client.GroqClient._api_key', return_value=''):
            response = self.client.post(
                reverse('expert_chat', kwargs={'pk': self.goal.pk}),
                data=json.dumps({'message': 'How should a team use this?', 'panel': 'expert'}),
                content_type='application/json',
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['panel'], 'expert')
        self.assertIn('professional view', response.json()['reply'].lower())
        self.assertEqual(ChatMessage.objects.filter(user=self.goal).count(), 2)

    def test_chat_rate_limit_blocks_twenty_first_message(self):
        from django.utils import timezone
        from datetime import timedelta
        ChatMessage.objects.bulk_create([
            ChatMessage(
                user=self.goal, domain=self.goal.domain, panel='teacher', role='user',
                content=f'Question {number}', created_at=timezone.now() - timedelta(minutes=number),
            )
            for number in range(20)
        ])
        with patch('roadmap.views.GroqClient.complete') as complete:
            response = self.client.post(
                reverse('expert_chat', kwargs={'pk': self.goal.pk}),
                data=json.dumps({'message': 'One more question', 'panel': 'teacher'}),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 429)
        self.assertIn('20 messages per hour', response.json()['error'])
        complete.assert_not_called()

    def test_chat_chips_submit_questions_to_chat_endpoint(self):
        self.goal.domain = 'Data Analyst'
        self.goal.goal = 'Become a Data Analyst'
        self.goal.save(update_fields=['domain', 'goal'])
        self.skill.name = 'Level 1: Data Analyst Foundations'
        self.skill.skill_map_json = [{'name': 'Spreadsheet formulas'}]
        self.skill.save(update_fields=['name', 'skill_map_json'])
        page = self.client.get(reverse('teach_concept', kwargs={'pk': self.skill.pk}))
        self.assertContains(page, 'Milestone structure advice')
        self.assertContains(page, 'Executive summary tips')
        self.assertContains(page, 'SQL query hints')
        self.assertContains(page, 'Best practices for this project')
        self.assertContains(page, 'data-chat-question=')
        self.assertContains(page, 'data-chat-url=')

    def test_payment_state_never_blocks_selected_tier(self):
        self.goal.chosen_tier = 'Intermediate'
        self.goal.enrollment_status = 'free_preview'
        self.goal.payment_status = 'pending'
        self.goal.save()
        levels = [
            SkillNode.objects.create(
                goal=self.goal,
                name=f'Level {number}: Intermediate topic',
                description='Intermediate course level.',
                order=number,
                coach_level=number,
                tier='Intermediate',
                status='in_progress' if number == 5 else 'not_started',
            )
            for number in range(5, 9)
        ]
        for level in levels:
            self.assertFalse(level.is_locked)
            response = self.client.get(reverse('skill_assessment', kwargs={'pk': level.pk}))
            self.assertEqual(response.status_code, 200)
            level.status = 'completed'
            level.save(update_fields=['status'])
        enrollment_response = self.client.get(
            reverse('enroll_course', kwargs={'pk': self.goal.pk})
        )
        self.assertRedirects(
            enrollment_response,
            reverse('dashboard', kwargs={'pk': self.goal.pk}),
        )


class DynamicDomainLearningSystemTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_full_stack_roadmap_generation(self):
        """Verify Full Stack Developer goal generates 12 skills in proper order and never defaults to Robotics."""
        response = self.client.post(reverse('odin_onboarding'), {
            'goal': 'Become a Full Stack Developer',
            'domain': 'Web Development',
            'current_level': 'Beginner',
            'existing_skills': 'None, complete beginner',
            'user_name': 'Karthik'
        })
        self.assertEqual(response.status_code, 302)
        goal = UserGoal.objects.filter(user_name='Karthik').first()
        self.assertIsNotNone(goal)
        self.assertEqual(goal.skill_nodes.count(), 12)

        skill_names = list(goal.skill_nodes.order_by('order').values_list('name', flat=True))
        self.assertIn("Level 1: Web basics", skill_names[0])
        self.assertIn("HTML", skill_names[1])
        self.assertIn("CSS", skill_names[2])
        self.assertIn("JavaScript", skill_names[3])
        self.assertIn("JavaScript intermediate", skill_names[4])
        self.assertIn("Async JavaScript", skill_names[5])
        self.assertIn("Git and GitHub", skill_names[6])
        self.assertIn("Django backend", skill_names[7])
        self.assertIn("Databases", skill_names[8])
        self.assertIn("Auth and security", skill_names[9])
        self.assertIn("React", skill_names[10])
        self.assertIn("Deployment and testing", skill_names[11])
        levels = list(goal.skill_nodes.order_by('order'))
        self.assertEqual([node.coach_level for node in levels], list(range(1, 13)))
        self.assertEqual(
            [node.tier for node in levels],
            ['Beginner'] * 4 + ['Intermediate'] * 4 + ['Advanced'] * 4
        )
        self.assertTrue(levels[3].project_json['is_active'])
        self.assertTrue(levels[4].project_json['is_active'])

        # Verify not Robotics
        for name in skill_names:
            self.assertNotIn("Robotics", name)

        # Check metadata persistence
        self.assertTrue(len(goal.roadmap_metadata) > 0)

    def test_robotics_roadmap_generation(self):
        """Verify Robotics goal generates robotics-specific skills."""
        response = self.client.post(reverse('odin_onboarding'), {
            'goal': 'Become a Robotics Engineer',
            'domain': 'Robotics',
            'current_level': 'Beginner',
            'existing_skills': 'Basic physics',
            'user_name': 'Priya'
        })
        self.assertEqual(response.status_code, 302)
        goal = UserGoal.objects.filter(user_name='Priya').first()
        self.assertIsNotNone(goal)
        self.assertEqual(goal.skill_nodes.count(), 12)

        first_skill = goal.skill_nodes.order_by('order').first()
        self.assertIn("Electronics basics", first_skill.name)
        self.assertIn("Button-controlled LED sequence", goal.skill_nodes.get(order=2).project_json['title'])
        self.assertTrue(goal.skill_nodes.get(order=2).project_json['is_active'])
        self.assertIn("Integrated obstacle-avoiding robot", goal.skill_nodes.get(order=12).project_json['title'])

    def test_custom_domain_roadmap_generation(self):
        """Verify custom arbitrary career goal generates personalized 6-level roadmap."""
        response = self.client.post(reverse('odin_onboarding'), {
            'goal': 'Learn Quantum Computing Algorithms',
            'domain': 'Quantum Physics',
            'current_level': 'Beginner',
            'existing_skills': 'Linear algebra',
            'user_name': 'Suresh'
        })
        self.assertEqual(response.status_code, 302)
        goal = UserGoal.objects.filter(user_name='Suresh').first()
        self.assertIsNotNone(goal)
        self.assertEqual(goal.skill_nodes.count(), 6)

        first_skill = goal.skill_nodes.order_by('order').first()
        self.assertIn("Quantum Computing Algorithms", first_skill.name)

    def test_skill_assessment_and_concepts_rendered_cleanly_without_literal_syntax(self):
        """Verify skill assessment page renders without literal Django syntax like {{ opt }}."""
        goal = UserGoal.objects.create(
            user_name="Anitha",
            domain="Web Development",
            current_level="Beginner",
            goal="Full Stack Developer"
        )
        skill = SkillNode.objects.create(
            goal=goal,
            name="HTML & Semantic Structure",
            description="Core HTML elements and page layout",
            order=1
        )
        response = self.client.get(reverse('skill_assessment', kwargs={'pk': skill.pk}))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # Critical: Ensure no literal template variable output exists
        self.assertNotIn("{{ opt }}", content)
        self.assertNotIn("{{ q.topic", content)
        self.assertNotIn("```html", content)

    def test_assessment_key_skills_follow_the_chosen_tier(self):
        goal = UserGoal.objects.create(
            user_name='Analyst Learner',
            domain='Data Analytics',
            current_level='Intermediate',
            chosen_tier='Intermediate',
            goal='Data Analyst',
        )
        levels = [
            SkillNode.objects.create(
                goal=goal,
                name=f'Level {number}: {title}',
                description=title,
                order=number,
                coach_level=number,
                tier='Intermediate',
                status='in_progress' if number == 5 else 'not_started',
            )
            for number, title in (
                (5, 'Statistics for analysts'),
                (6, 'Pandas intermediate'),
                (7, 'SQL joins, subqueries, and CTEs'),
                (8, 'SQL window functions'),
            )
        ]
        response = self.client.get(
            reverse('skill_assessment', kwargs={'pk': levels[0].pk})
        )
        content = response.content.decode('utf-8')
        self.assertContains(response, 'Your Intermediate focus')
        for title in (
            'Statistics for analysts',
            'Pandas intermediate',
            'SQL joins, subqueries, and CTEs',
            'SQL window functions',
        ):
            self.assertIn(title, content)
        for title in ('Excel basics', 'Python basics', 'Pandas basics', 'SQL basics'):
            self.assertNotIn(title, content)

    def test_all_requested_curricula_have_12_ordered_levels_and_safe_cyber_inactivity(self):
        expected = {
            'web_dev': 'web development',
            'data_analytics': 'data analyst',
            'ai_ml': 'AI Engineer',
            'robotics': 'Robotics Engineer',
            'cybersecurity': 'Cyber Security',
        }
        for domain, goal_text in expected.items():
            curriculum = EXAOrchestrator.analyze_goal_and_skills(goal_text, 'Beginner', domain, '')
            levels = curriculum['skill_nodes']
            self.assertEqual(len(levels), 12, domain)
            self.assertEqual([level['coach_level'] for level in levels], list(range(1, 13)))
            self.assertEqual(
                [level['tier'] for level in levels],
                ['Beginner'] * 4 + ['Intermediate'] * 4 + ['Advanced'] * 4,
                domain,
            )
        cyber_levels = EXAOrchestrator.analyze_goal_and_skills(
            'Cyber Security', 'Beginner', 'cybersecurity', ''
        )['skill_nodes']
        self.assertTrue(all(not level['project_json']['is_active'] for level in cyber_levels))
        self.assertTrue(all('local' in level['project_json']['objective'].lower() or
                            'defensive' in level['project_json']['objective'].lower()
                            for level in cyber_levels))
        cyber_lesson = EXAOrchestrator.generate_concept_lesson(
            'OWASP risks', 'Level 5: OWASP Top 10 part 1', 'Cyber Security', 'Beginner'
        )
        self.assertIn('do not test real third-party systems', cyber_lesson['pro_tip'].lower())
        cyber_project = EXAOrchestrator.generate_project(
            'Cyber Security', 'Beginner', 'Level 5: OWASP Top 10 part 1'
        )
        self.assertIn('local', cyber_project['objective'].lower())
        self.assertNotIn('exploit at least', cyber_project['requirements'].lower())

        data_concepts = EXAOrchestrator.generate_skill_map(
            'Level 8: SQL window functions', 'Data Analyst', 'Beginner', []
        )['concepts']
        self.assertTrue(any('ROW_NUMBER' in concept['name'] for concept in data_concepts))
        self.assertFalse(any('XLOOKUP' in concept['name'] for concept in data_concepts))
        git_concepts = EXAOrchestrator.generate_skill_map(
            'Level 7: Git and GitHub', 'Web Development', 'Beginner', []
        )['concepts']
        self.assertTrue(any('Pull requests' in concept['name'] for concept in git_concepts))

    def test_dashboard_shows_only_the_selected_tier_and_starts_at_its_first_level(self):
        expected = {
            'Beginner': (1, 4),
            'Intermediate': (5, 8),
            'Advanced': (9, 12),
        }
        for tier, (first_level, last_level) in expected.items():
            with self.subTest(tier=tier):
                self.client.post(reverse('odin_onboarding'), {
                    'goal': 'Become a Full Stack Developer',
                    'domain': 'Web Development',
                    'chosen_tier': tier,
                    'existing_skills': '',
                    'user_name': f'{tier} Dashboard Learner',
                })
                goal = UserGoal.objects.get(user_name=f'{tier} Dashboard Learner')
                self.assertEqual(goal.chosen_tier, tier)
                self.assertEqual(goal.current_skill.coach_level, first_level)
                response = self.client.get(reverse('dashboard', kwargs={'pk': goal.pk}))
                content = response.content.decode('utf-8')
                visible_levels = [
                    level for level in range(1, 13)
                    if f'Level {level}:' in content
                ]
                self.assertEqual(visible_levels, list(range(first_level, last_level + 1)))
                self.assertEqual(content.count('class="tier-section"'), 1)
                self.assertIn(f'{tier} Tier', content)

    def test_intermediate_redirects_never_expose_beginner_levels(self):
        self.client.post(reverse('odin_onboarding'), {
            'goal': 'Become a Full Stack Developer',
            'domain': 'Web Development',
            'chosen_tier': 'Intermediate',
            'existing_skills': '',
            'user_name': 'Intermediate Redirect Learner',
        })
        goal = UserGoal.objects.get(user_name='Intermediate Redirect Learner')
        beginner_level = goal.skill_nodes.get(coach_level=1)

        response = self.client.get(
            reverse('skill_assessment', kwargs={'pk': beginner_level.pk})
        )
        self.assertRedirects(response, reverse('dashboard', kwargs={'pk': goal.pk}))
        self.assertNotIn(f'/skill/{beginner_level.pk}/assessment/', response.url)
        dashboard = self.client.get(response.url)
        content = dashboard.content.decode('utf-8')
        for level in range(1, 5):
            self.assertNotIn(f'Level {level}:', content)

    def test_intermediate_out_of_tier_lesson_urls_only_redirect_to_selected_dashboard(self):
        goal = UserGoal.objects.create(
            user_name='Intermediate Route Learner',
            domain='Web Development',
            current_level='Intermediate',
            chosen_tier='Intermediate',
            goal='Become a Full Stack Developer',
        )
        beginner_level = SkillNode.objects.create(
            goal=goal,
            name='Level 1: Web basics',
            description='Beginner content must not be exposed.',
            order=1,
            coach_level=1,
            tier='Beginner',
        )
        level_5 = SkillNode.objects.create(
            goal=goal,
            name='Level 5: JavaScript intermediate',
            description='Selected tier entry.',
            order=5,
            coach_level=5,
            tier='Intermediate',
            status='in_progress',
            skill_map_json=[{'name': 'Scope'}],
        )
        attempt = QuizAttempt.objects.create(
            skill_node=beginner_level,
            answers_json=[],
            feedback_json=[],
        )
        routes = (
            ('skill_assessment', 'get'),
            ('concept_overview', 'get'),
            ('skill_map', 'get'),
            ('learning', 'get'),
            ('teach_concept', 'get'),
            ('quiz', 'get'),
            ('quiz_submit', 'post'),
            ('quiz_result', 'get'),
            ('advance_concept', 'get'),
            ('review', 'get'),
            ('practice_submit', 'post'),
        )
        for route_name, method in routes:
            with self.subTest(route=route_name):
                kwargs = {'pk': attempt.pk if route_name == 'quiz_result' else beginner_level.pk}
                url = reverse(route_name, kwargs=kwargs)
                response = (
                    self.client.post(url, {})
                    if method == 'post'
                    else self.client.get(url)
                )
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, reverse('dashboard', kwargs={'pk': goal.pk}))
                self.assertNotIn(f'/skill/{beginner_level.pk}/', response.url)

        dashboard = self.client.get(reverse('dashboard', kwargs={'pk': goal.pk}))
        dashboard_content = dashboard.content.decode('utf-8')
        self.assertNotIn('Level 1: Web basics', dashboard_content)
        self.assertContains(dashboard, 'Level 5: JavaScript intermediate')
        self.assertEqual(goal.current_skill, level_5)

    def test_advanced_user_never_sees_beginner_or_intermediate_levels(self):
        self.client.post(reverse('odin_onboarding'), {
            'goal': 'Become a Full Stack Developer',
            'domain': 'Web Development',
            'chosen_tier': 'Advanced',
            'existing_skills': '',
            'user_name': 'Advanced Dashboard Learner',
        })
        goal = UserGoal.objects.get(user_name='Advanced Dashboard Learner')
        response = self.client.get(reverse('dashboard', kwargs={'pk': goal.pk}))
        content = response.content.decode('utf-8')
        self.assertEqual(goal.current_skill.coach_level, 9)
        for level in range(1, 9):
            self.assertNotIn(f'Level {level}:', content)

    def test_selected_tier_projects_gate_only_following_levels_inside_that_tier(self):
        self.client.post(reverse('odin_onboarding'), {
            'goal': 'Become a Full Stack Developer',
            'domain': 'Web Development',
            'chosen_tier': 'Intermediate',
            'existing_skills': '',
            'user_name': 'Intermediate Gate Learner',
        })
        goal = UserGoal.objects.get(user_name='Intermediate Gate Learner')
        level_5 = goal.skill_nodes.get(coach_level=5)
        level_6 = goal.skill_nodes.get(coach_level=6)
        self.assertFalse(level_5.is_locked)
        self.assertTrue(level_6.is_locked)

        level_5.status = 'completed'
        level_5.save(update_fields=['status'])
        self.assertFalse(level_6.is_locked)

    def test_each_course_level_has_unique_title_concepts_and_correct_tier(self):
        from .course_content import RESTRUCTURED_CURRICULA

        for domain, curriculum in RESTRUCTURED_CURRICULA.items():
            levels = curriculum['levels']
            titles = [level['name'].strip().casefold() for level in levels]
            concept_lists = [
                tuple(concept.strip().casefold() for concept in level['concepts'])
                for level in levels
            ]
            self.assertEqual(len(titles), len(set(titles)), f'Duplicate title in {domain}')
            self.assertEqual(
                len(concept_lists),
                len(set(concept_lists)),
                f'Duplicate concept list in {domain}',
            )
            for level in levels:
                number = level['coach_level']
                expected_tier = (
                    'Beginner' if 1 <= number <= 4
                    else 'Intermediate' if 5 <= number <= 8
                    else 'Advanced'
                )
                self.assertEqual(level['tier'], expected_tier, f'{domain} level {number}')
                self.assertGreaterEqual(len(level['concepts']), 3)
                expected_max_concepts = 6 if domain == 'robotics' and number == 1 else 5
                self.assertLessEqual(len(level['concepts']), expected_max_concepts)
                mapped_concepts = EXAOrchestrator.generate_skill_map(
                    level['name'], domain, 'Beginner', []
                )['concepts']
                self.assertEqual(
                    [concept['name'] for concept in mapped_concepts],
                    level['concepts'],
                    f'Generated concept map does not match {domain} level {number}',
                )

    def test_intermediate_progression_starts_at_level_5_and_uses_level_5_project_gate(self):
        response = self.client.post(reverse('odin_onboarding'), {
            'goal': 'Become a Full Stack Developer',
            'domain': 'Web Development',
            'chosen_tier': 'Intermediate',
            'existing_skills': '',
            'user_name': 'Intermediate Project Gate Learner',
        })
        self.assertEqual(response.status_code, 302)
        goal = UserGoal.objects.get(user_name='Intermediate Project Gate Learner')
        level_5 = goal.skill_nodes.get(coach_level=5)
        level_6 = goal.skill_nodes.get(coach_level=6)
        self.assertEqual(goal.current_skill, level_5)
        self.assertFalse(level_5.is_locked)
        self.assertTrue(level_6.is_locked)
        self.client.post(
            reverse('project', kwargs={'pk': goal.pk}),
            {'submission_text': 'Text-only submissions cannot pass Build Lab.'},
        )

        level_5.refresh_from_db()
        level_6.refresh_from_db()
        self.assertEqual(level_5.status, 'in_progress')
        self.assertEqual(level_6.status, 'not_started')
        self.assertTrue(level_6.is_locked)


class BuildLabBriefTests(TestCase):
    active_domains = ('data_analytics', 'ai_ml', 'web_dev', 'robotics', 'electronics')

    def test_active_briefs_meet_tier_company_and_submission_quality_gates(self):
        counts = {'Beginner': 3, 'Intermediate': 4, 'Advanced': 5}
        for domain in self.active_domains:
            briefs = [level['project_json'] for level in RESTRUCTURED_CURRICULA[domain]['levels']]
            self.assertTrue(all(brief['is_active'] for brief in briefs))
            self.assertEqual(len({brief['company'] for brief in briefs}), 12, domain)
            self.assertEqual(len({brief['industry'] for brief in briefs}), 12, domain)
            for brief in briefs:
                with self.subTest(domain=domain, company=brief['company']):
                    self.assertEqual(len(brief['requirements_list']), counts[brief['tier']])
                    self.assertTrue(brief['dataset_schema'])
                    self.assertEqual(sum(item['weight'] for item in brief['requirement_evidence']), 100)
                    self.assertEqual(len(brief['scoring']['criteria']), 4)
                    self.assertEqual(sum(item['weight'] for item in brief['scoring']['criteria']), 100)
                    self.assertIn('README', brief['requirements'])
                    self.assertIn('business problem', brief['requirements'].lower())
                    if brief['tier'] == 'Beginner':
                        self.assertFalse(brief['submission']['live_demo_required'])
                    else:
                        self.assertTrue(brief['submission']['live_demo_required'])
                    if brief['tier'] == 'Advanced':
                        self.assertTrue(
                            'monitoring/evaluation' in brief['requirements'].lower()
                            or 'monitoring or evaluation' in brief['requirements'].lower()
                        )

    def test_required_evidence_cap_and_60_point_pass_threshold(self):
        evidence = ' '.join(['analysis result milestone'] * 8)
        missing_pdf = EXAOrchestrator.evaluate_project_submission(
            evidence + ' https://demo.example.com live demo', 'Data Analyst', 'Data Analyst', 'Level 5'
        )
        valid = EXAOrchestrator.evaluate_project_submission(
            evidence + ' PDF report: report.pdf https://demo.example.com live demo',
            'Data Analyst', 'Data Analyst', 'Level 5'
        )
        self.assertEqual(missing_pdf['score'], 40)
        self.assertFalse(missing_pdf['is_passed'])
        self.assertGreaterEqual(valid['score'], 60)
        self.assertTrue(valid['is_passed'])
        self.assertFalse(59 >= 60)
        self.assertTrue(60 >= 60)

    def test_active_briefs_have_no_learner_facing_draft_language_and_match_domain_level(self):
        prohibited = ('draft', 'pending review', 'must be reviewed', 'company-style brief')
        for domain in self.active_domains:
            for number, level in enumerate(RESTRUCTURED_CURRICULA[domain]['levels'], start=1):
                brief = level['project_json']
                with self.subTest(domain=domain, level=number):
                    learner_text = json.dumps(brief).lower()
                    self.assertTrue(all(term not in learner_text for term in prohibited))
                    self.assertEqual(brief['domain'], domain)
                    self.assertEqual(brief['level'], number)
                    self.assertIn(level['name'].split(': ', 1)[1].lower().split()[0], brief['task'].lower())

    def test_invalid_brief_is_blocked_with_preparation_message(self):
        goal = UserGoal.objects.create(
            user_name='Preparing Brief Learner', goal='Become a Data Analyst', domain='Data Analyst'
        )
        SkillNode.objects.create(
            goal=goal, name='Level 1: Excel basics', tier='Beginner', coach_level=1,
            order=1, status='in_progress', project_json={}
        )
        response = self.client.get(reverse('project', kwargs={'pk': goal.pk}), secure=True)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'This project is being prepared. Check back soon.', status_code=403)
        self.assertEqual(Project.objects.filter(goal=goal).count(), 0)

    def test_robotics_level_one_electronics_lesson_snapshot_is_unchanged(self):
        level = RESTRUCTURED_CURRICULA['robotics']['levels'][0]
        self.assertEqual(level['name'], 'Level 1: Electronics basics')
        self.assertEqual(level['description'], "Voltage, current, resistance, Ohm's law, circuits, and breadboarding.")
        self.assertEqual(level['importance'], "Voltage, current, resistance, Ohm's law, circuits, and breadboarding.")
        self.assertEqual(level['concepts'], [
            'Voltage', 'Current', 'Resistance and Ohm\'s law', 'LED circuit', 'Breadboard', 'Multimeter use',
        ])


class ElectronicsAndSubmissionTests(TestCase):
    def test_electronics_is_a_separate_twelve_level_course_with_topic_quizzes(self):
        electronics = RESTRUCTURED_CURRICULA['electronics']['levels']
        self.assertEqual(len(electronics), 12)
        mapped = EXAOrchestrator.generate_skill_map(
            'Level 1: Electronics Foundations & Core Principles', 'EEE', 'Beginner', []
        )
        self.assertEqual([item['name'] for item in mapped['concepts']], electronics[0]['concepts'])
        typo_mapped = EXAOrchestrator.generate_skill_map(
            'Level 1: Electrocics Foundations & Core Principles', 'Electrocics', 'Beginner', []
        )
        self.assertEqual([item['name'] for item in typo_mapped['concepts']], electronics[0]['concepts'])
        for level_number, level in enumerate(electronics[:4], start=1):
            mapped_level = EXAOrchestrator.generate_skill_map(
                level['name'], 'electrical and electroncial', 'Beginner', []
            )
            self.assertEqual(
                [item['name'] for item in mapped_level['concepts']], level['concepts'],
                f'Wrong focus topics for Electronics Level {level_number}',
            )
        self.assertEqual(len(RESTRUCTURED_CURRICULA['robotics']['levels']), 12)
        self.assertEqual(RESTRUCTURED_CURRICULA['robotics']['levels'][0]['concepts'], [
            'Voltage', 'Current', "Resistance and Ohm's law", 'LED circuit', 'Breadboard', 'Multimeter use',
        ])
        self.assertEqual(RESTRUCTURED_CURRICULA['web_dev']['levels'][0]['concepts'], [
            'DNS resolution', 'HTTP and HTTPS', 'Client-server requests and responses', 'Browser developer tools',
        ])

        all_questions = []
        all_concept_points = []
        for level in electronics:
            level_answer_patterns = []
            for concept in level['concepts']:
                guide = get_course_guide('electronics', level['name'], concept)
                self.assertIsNotNone(guide, f'Missing Electronics lesson guide: {level["name"]} / {concept}')
                lesson = EXAOrchestrator.generate_concept_lesson(
                    concept, level['name'], 'EEE', level['tier']
                )
                self.assertIn(concept, lesson['core_concept'])
                self.assertTrue(lesson['concept_points'])
                self.assertTrue(lesson['method_teach'])
                all_concept_points.extend(lesson['concept_points'])
                quiz = EXAOrchestrator.generate_quiz_questions(
                    concept, level['name'], 'EEE', level['tier']
                )
                self.assertGreaterEqual(len(quiz), 4)
                self.assertLessEqual(len(quiz), 5)
                self.assertGreaterEqual(len({item['correct_answer'] for item in quiz}), 3)
                self.assertTrue(all(concept in item['question_text'] for item in quiz))
                level_answer_patterns.append(tuple(item['correct_answer'] for item in quiz))
                all_questions.extend(item['question_text'] for item in quiz)
            self.assertEqual(len(level_answer_patterns), len(set(level_answer_patterns)))
        self.assertEqual(len(all_questions), len(set(all_questions)))
        self.assertEqual(len(all_concept_points), len(set(all_concept_points)))

    def test_electronics_level_one_questions_are_unique_and_concept_specific(self):
        level = RESTRUCTURED_CURRICULA['robotics']['levels'][0]
        questions = []
        for concept in level['concepts']:
            guide = get_course_guide('robotics', level['name'], concept)
            quiz = generate_quiz_for_domain(concept, level['name'], 'robotics', 'Beginner')
            lesson = EXAOrchestrator.generate_concept_lesson(concept, level['name'], 'Robotics Engineer', 'Beginner')
            self.assertIsNotNone(guide)
            self.assertTrue(lesson['concept_points'])
            self.assertTrue(lesson['method_teach'])
            self.assertEqual(lesson['code_example'], guide['example'])
            self.assertEqual(lesson['thinking_exercise'], guide['practice'])
            self.assertEqual(lesson['task'], guide['practice'])
            self.assertGreaterEqual(len(quiz), 3)
            self.assertLessEqual(len(quiz), 5)
            self.assertGreaterEqual(len({item['question_type'] for item in quiz}), 2)
            for item in quiz:
                self.assertEqual(item['answer_key'], item['correct_answer'])
                self.assertIn(concept, item['question_text'])
                questions.append(item['question_text'])
        self.assertEqual(len(questions), len(set(questions)))

    def test_private_upload_validation_and_score_rules(self):
        pdf = SimpleUploadedFile('report.pdf', b'%PDF-1.7\nproof\n%%EOF', content_type='application/pdf')
        validate_pdf(pdf)
        with self.assertRaises(SubmissionValidationError):
            validate_pdf(SimpleUploadedFile('fake.pdf', b'not a pdf'))
        with self.assertRaises(SubmissionValidationError):
            validate_pdf(SimpleUploadedFile('large.pdf', b'%PDF-' + b'x' * MAX_REPORT_BYTES + b'%%EOF'))
        with self.assertRaises(SubmissionValidationError):
            validate_video(SimpleUploadedFile('large.mp4', b'\x00\x00\x00\x18ftypisom' + b'x' * MAX_VIDEO_BYTES))
        with self.assertRaises(SubmissionValidationError):
            with patch('roadmap.submission_scanner._duration_seconds', return_value=301):
                validate_video_duration('video.mp4')

    def test_scanner_retries_invalid_json_and_caps_missing_evidence(self):
        goal = UserGoal.objects.create(user_name='Scanner Owner', goal='Data Analyst', domain='Data Analyst')
        project = Project.objects.create(goal=goal, title='Project', level='Level 1: Excel basics')
        SkillNode.objects.create(
            goal=goal, name=project.level, coach_level=1, order=1,
            project_json={'submission': {'live_demo_required': False}, 'requirements_list': ['one', 'two', 'three']},
        )
        submission = ProjectSubmission.objects.create(project=project)
        with patch.object(SubmissionScanner, '_call_claude', return_value='not-json') as mock_scan:
            with self.assertRaisesRegex(RuntimeError, 'evaluation_failed'):
                SubmissionScanner._scan_with_retry([], submission, {}, 'pdf')
            self.assertEqual(mock_scan.call_count, 2)

        requirements = [{'id': f'R{i}', 'requirement': 'req', 'met': True, 'reason': 'found', 'evidence': 'page 1'} for i in range(3)]
        criteria = [{'name': str(i), 'weight': 25, 'score': score} for i, score in enumerate((25, 25, 9, 0))]
        submission.report = 'report.pdf'
        data = SubmissionScanner._parse_and_score(json.dumps({
            'criteria': criteria, 'requirements': requirements, 'strengths': ['a', 'b', 'c'],
            'improvements': ['a', 'b', 'c'], 'next_step': 'revise', 'rating': 'Needs work',
        }), submission, 'pdf')
        self.assertEqual(data['score'], 59)
        self.assertFalse(data['is_passed'])
        criteria[2]['score'] = 10
        passed = SubmissionScanner._parse_and_score(json.dumps({
            'criteria': criteria, 'requirements': requirements, 'strengths': ['a', 'b', 'c'],
            'improvements': ['a', 'b', 'c'], 'next_step': 'continue', 'rating': 'Pass',
        }), submission, 'pdf')
        self.assertEqual(passed['score'], 60)
        self.assertTrue(passed['is_passed'])
        submission.report = ''
        capped = SubmissionScanner._parse_and_score(json.dumps({
            'criteria': [{'name': str(i), 'weight': 25, 'score': 25} for i in range(4)],
            'requirements': requirements, 'strengths': ['a', 'b', 'c'], 'improvements': ['a', 'b', 'c'],
            'next_step': 'submit PDF', 'rating': 'Incomplete',
        }), submission, 'pdf')
        self.assertEqual(capped['score'], 40)

        live_goal = UserGoal.objects.create(user_name='Live Cap Owner', goal='Data Analyst', domain='Data Analyst')
        live_project = Project.objects.create(goal=live_goal, title='Project', level='Level 5: Statistics for analysts')
        SkillNode.objects.create(
            goal=live_goal, name=live_project.level, coach_level=5, order=5,
            project_json={'submission': {'live_demo_required': True}, 'requirements_list': ['a', 'b', 'c', 'd']},
        )
        live_submission = ProjectSubmission(project=live_project, report='report.pdf')
        live_data = SubmissionScanner._parse_and_score(json.dumps({
            'criteria': [{'name': str(i), 'weight': 25, 'score': 25} for i in range(4)],
            'requirements': [{'id': f'R{i}', 'requirement': 'req', 'met': True, 'reason': 'found', 'evidence': 'page 1'} for i in range(4)],
            'strengths': ['a', 'b', 'c'], 'improvements': ['a', 'b', 'c'],
            'next_step': 'add live link', 'rating': 'Incomplete',
        }), live_submission, 'pdf')
        self.assertEqual(live_data['score'], 40)

    def test_pdf_scan_sends_document_block_and_private_files_have_no_url(self):
        goal = UserGoal.objects.create(user_name='PDF Owner', goal='Data Analyst', domain='Data Analyst')
        project = Project.objects.create(goal=goal, title='Project', level='Level 1: Excel basics')
        SkillNode.objects.create(
            goal=goal, name=project.level, coach_level=1, order=1,
            project_json={'submission': {'live_demo_required': False}, 'requirements_list': ['a', 'b', 'c']},
        )
        submission = ProjectSubmission(project=project, report=SimpleUploadedFile('report.pdf', b'%PDF-1.7\n%%EOF'))
        payload = {
            'criteria': [{'name': str(index), 'weight': 25, 'score': 20} for index in range(4)],
            'requirements': [{'id': f'R{index}', 'requirement': 'req', 'met': True, 'reason': 'found', 'evidence': 'page 1'} for index in range(3)],
            'strengths': ['a', 'b', 'c'], 'improvements': ['a', 'b', 'c'], 'next_step': 'continue', 'rating': 'Good',
        }
        with patch.object(SubmissionScanner, '_call_claude', return_value=json.dumps(payload)) as mock_scan:
            SubmissionScanner.scan_pdf(submission, {})
        document_block = mock_scan.call_args.args[0][0]
        self.assertEqual(document_block['type'], 'document')
        self.assertEqual(document_block['source']['media_type'], 'application/pdf')
        self.assertTrue(document_block['source']['data'])
        with self.assertRaises(ValueError):
            submission.report.storage.url(submission.report.name)

    def test_upload_endpoint_rejects_non_pdf_and_oversize_report(self):
        goal = UserGoal.objects.create(user_name='Upload Owner', goal='Data Analyst', domain='Data Analyst')
        project = Project.objects.create(goal=goal, title='Project', level='Level 1: Excel basics')
        session = self.client.session
        session['current_goal_id'] = goal.pk
        session.save()
        url = reverse('project_submission_upload', kwargs={'pk': project.pk})
        for file in (
            SimpleUploadedFile('fake.pdf', b'plain text'),
            SimpleUploadedFile('huge.pdf', b'%PDF-' + b'x' * MAX_REPORT_BYTES + b'%%EOF'),
        ):
            response = self.client.post(url, {'report': file, 'github_url': 'https://github.com/example/repo'}, secure=True)
            self.assertEqual(response.status_code, 302)
        self.assertEqual(ProjectSubmission.objects.filter(project=project).count(), 0)

    def test_upload_endpoint_rejects_video_over_five_minutes(self):
        goal = UserGoal.objects.create(user_name='Video Owner', goal='Data Analyst', domain='Data Analyst')
        project = Project.objects.create(goal=goal, title='Project', level='Level 1: Excel basics')
        session = self.client.session
        session['current_goal_id'] = goal.pk
        session.save()
        with patch('roadmap.views.validate_video_upload_duration', side_effect=SubmissionValidationError('Video must be five minutes or shorter.')):
            response = self.client.post(
                reverse('project_submission_upload', kwargs={'pk': project.pk}),
                {
                    'report': SimpleUploadedFile('report.pdf', b'%PDF-1.7\n%%EOF'),
                    'video': SimpleUploadedFile('demo.mp4', b'\x00\x00\x00\x18ftypisom'),
                    'github_url': 'https://github.com/example/repo',
                }, secure=True,
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProjectSubmission.objects.filter(project=project).count(), 0)

    def test_another_session_cannot_view_submission(self):
        goal = UserGoal.objects.create(user_name='Owner', goal='Data Analyst', domain='Data Analyst')
        project = Project.objects.create(goal=goal, title='Project', level='Level 1: Excel basics')
        submission = ProjectSubmission.objects.create(project=project)
        session = self.client.session
        session['current_goal_id'] = goal.pk + 1
        session.save()
        response = self.client.get(reverse('submission_result', kwargs={'pk': submission.pk}), secure=True)
        self.assertEqual(response.status_code, 403)
        upload = self.client.post(
            reverse('project_submission_upload', kwargs={'pk': project.pk}),
            {'report': SimpleUploadedFile('report.pdf', b'%PDF-1.7\n%%EOF')}, secure=True,
        )
        self.assertEqual(upload.status_code, 403)



class UniversalSmartLearningEngineUpgradeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.goal = UserGoal.objects.create(
            user_name="Learner_Test",
            domain="Data Analytics",
            goal="Data Analyst",
            chosen_tier="Beginner",
            current_level="Beginner",
        )
        self.skill = SkillNode.objects.create(
            goal=self.goal,
            name="Level 1: Excel basics",
            coach_level=1,
            order=1,
            tier="Beginner",
            status="in_progress",
            phase="learning",
            skill_map_json=[{"name": "Excel formulas"}, {"name": "Filters"}, {"name": "Pivot tables"}, {"name": "XLOOKUP"}],
            current_concept_index=0,
        )

    def test_universal_smart_learning_engine_supports_all_six_domains_and_three_stages(self):
        from .smart_learning_engine import SmartLearningEngine
        from .course_content import RESTRUCTURED_CURRICULA
        from .course_teaching import get_course_guide

        domains = ['web_dev', 'ai_ml', 'robotics', 'data_analytics', 'electronics', 'cybersecurity']
        stages = ['Beginner', 'Intermediate', 'Advanced']

        for domain in domains:
            curriculum = RESTRUCTURED_CURRICULA[domain]
            for stage in stages:
                # Find a level in this stage
                level = next(l for l in curriculum['levels'] if l['tier'] == stage)
                concept = level['concepts'][0]
                guide = get_course_guide(domain, level['name'], concept)
                self.assertIsNotNone(guide, f"Missing guide for {domain} {level['name']} {concept}")

                # Build full 8-part lesson experience
                lesson = SmartLearningEngine.build_lesson(concept, guide, domain, stage)
                self.assertEqual(lesson['stage'], stage)
                self.assertEqual(lesson['domain'], domain)

                # Verify A. Understand
                self.assertTrue(lesson['understand']['what_is_it'])
                self.assertTrue(lesson['understand']['why_it_matters'])
                self.assertTrue(lesson['understand']['where_it_is_used'])
                self.assertTrue(lesson['understand']['problem_it_solves'])
                self.assertTrue(lesson['understand']['prerequisites'])

                # Verify B. Learn
                self.assertTrue(lesson['learn']['detailed_explanation'])
                self.assertTrue(lesson['learn']['how_it_works'])
                self.assertGreaterEqual(len(lesson['learn']['common_mistakes']), 1)

                # Verify C. Examples
                self.assertTrue(lesson['examples']['practical_example'])
                self.assertTrue(lesson['examples']['expected_outcome'])

                # Verify D. Practise
                self.assertTrue(lesson['practise']['guided_task']['instructions'])
                self.assertTrue(lesson['practise']['independent_task']['instructions'])
                self.assertGreaterEqual(len(lesson['practise']['guided_task']['hints']), 1)

                # Verify E. Revise
                self.assertTrue(lesson['revise']['summary'])
                self.assertGreaterEqual(len(lesson['revise']['important_points']), 2)

                # Verify F. Quiz
                quiz = SmartLearningEngine.build_quiz_questions(concept, guide, domain, stage)
                self.assertGreaterEqual(len(quiz), 4)
                self.assertLessEqual(len(quiz), 5)
                self.assertTrue(all(q['correct_answer'] in 'ABCD' for q in quiz))
                self.assertTrue(all(len({q[f'option_{l}'] for l in 'abcd'}) == 4 for q in quiz))

    def test_excel_curriculum_starts_with_fundamentals(self):
        from .course_teaching import get_course_guide
        from .smart_learning_engine import SmartLearningEngine

        guide = get_course_guide('data_analytics', 'Level 1: Excel basics', 'Excel formulas')
        self.assertIsNotNone(guide)
        lesson = SmartLearningEngine.build_lesson('Excel formulas', guide, 'data_analytics', 'Beginner')

        # Check that Excel fundamentals are thoroughly taught
        full_text = json.dumps(lesson).lower()
        self.assertIn("excel", full_text)
        self.assertIn("cell", full_text)
        self.assertIn("row", full_text)
        self.assertIn("column", full_text)
        self.assertIn("expense tracker", full_text)
        self.assertIn("sum", full_text)

    def test_practice_exercise_submission_persists_mastery_and_criteria(self):
        from .models import ConceptMasteryAttempt

        url = reverse('practice_submit', kwargs={'pk': self.skill.pk})
        solution_text = (
            "Step 1: Create a monthly expense table with columns Date, Category, Description, Amount. "
            "Step 2: Enter formatted currency values in column D. "
            "Step 3: In cell D11, implement the formula =SUM(D2:D10) to calculate total monthly expense. "
            "Step 4: Verify the result by testing with known sample inputs and checking that formatting displays as currency without error."
        )

        session = self.client.session
        session['current_goal_id'] = self.goal.pk
        session.save()

        response = self.client.post(
            url,
            data=json.dumps({'answer': solution_text}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['score'], 75)
        self.assertTrue(data['is_mastered'])

        # Verify DB persistence
        attempt = ConceptMasteryAttempt.objects.filter(skill_node=self.skill, concept_index=0).first()
        self.assertIsNotNone(attempt)
        self.assertEqual(attempt.score, data['score'])
        self.assertTrue(attempt.is_mastered)

    def test_context_aware_ai_teacher_offline_fallback(self):
        with patch('roadmap.groq_client.GroqClient._api_key', return_value=''):
            # 1. Ask for hints
            resp_hint = self.client.post(
                reverse('expert_chat', kwargs={'pk': self.goal.pk}),
                data=json.dumps({'message': 'Can you give me a hint for this exercise?', 'panel': 'teacher'}),
                content_type='application/json'
            )
            self.assertEqual(resp_hint.status_code, 200)
            self.assertIn('hint', resp_hint.json()['reply'].lower())

            # 2. Ask for mistakes
            resp_err = self.client.post(
                reverse('expert_chat', kwargs={'pk': self.goal.pk}),
                data=json.dumps({'message': 'What common mistakes should I avoid?', 'panel': 'teacher'}),
                content_type='application/json'
            )
            self.assertEqual(resp_err.status_code, 200)
            self.assertIn('mistake', resp_err.json()['reply'].lower())

            # 3. Ask for summary / revision
            resp_rev = self.client.post(
                reverse('expert_chat', kwargs={'pk': self.goal.pk}),
                data=json.dumps({'message': 'Can you give me a summary of this concept?', 'panel': 'teacher'}),
                content_type='application/json'
            )
            self.assertEqual(resp_rev.status_code, 200)
            self.assertIn('revision', resp_rev.json()['reply'].lower())

    def test_teach_concept_page_renders_complete_teaching_sections(self):
        session = self.client.session
        session['current_goal_id'] = self.goal.pk
        session.save()

        response = self.client.get(reverse('teach_concept', kwargs={'pk': self.skill.pk}))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # Check sections A through F are present in UI
        self.assertIn("A. Understand", content)
        self.assertIn("B. Learn Step-by-Step", content)
        self.assertIn("C. Examples & Working Implementation", content)
        self.assertIn("D. Practise & Apply", content)
        self.assertIn("E. Revise & Retain", content)
        self.assertIn("Take the 5-Question Quiz", content)



class StageProjectAndProgressionCorrectionTests(TestCase):
    """
    Tests for EXA AI HUB Learning Flow & Project System Corrections:
    1. Correct project visibility at roadmap beginning (indicators only, details hidden).
    2. TASBI AI SOLUTIONS branding everywhere (zero TABSI occurrences).
    3. Exactly 18 unique projects (6 domains x 3 stages).
    4. Projects unlock ONLY after completing their stage lessons.
    5. Direct URL access cannot bypass locked stages.
    """

    def setUp(self):
        self.client = Client()
        self.goal = UserGoal.objects.create(
            user_name="ProgressionTester",
            domain="Web Development",
            goal="Become a Full Stack Developer",
            chosen_tier="Beginner",
            current_level="Beginner",
        )
        # Create 4 beginner levels
        self.nodes = []
        for i in range(1, 5):
            node = SkillNode.objects.create(
                goal=self.goal,
                name=f"Level {i}: Web Dev Topic {i}",
                coach_level=i,
                order=i,
                tier="Beginner",
                status="not_started" if i > 1 else "in_progress",
                phase="learning",
                project_json={'is_active': False},
            )
            self.nodes.append(node)

    def test_tasbi_branding_everywhere_and_no_tabsi(self):
        # Home page
        home_resp = self.client.get(reverse('home'))
        self.assertEqual(home_resp.status_code, 200)
        home_content = home_resp.content.decode('utf-8')
        self.assertIn("TASBI AI SOLUTIONS", home_content)
        self.assertNotIn("TABSI", home_content)

        # Dashboard page
        dash_resp = self.client.get(reverse('dashboard', kwargs={'pk': self.goal.pk}))
        self.assertEqual(dash_resp.status_code, 200)
        dash_content = dash_resp.content.decode('utf-8')
        self.assertIn("TASBI AI SOLUTIONS", dash_content)
        self.assertNotIn("TABSI", dash_content)

    def test_home_view_handles_missing_session_table(self):
        with patch.object(SessionBase, 'get', side_effect=Exception('django_session missing')):
            with patch.object(SessionBase, '__setitem__', side_effect=Exception('django_session missing')):
                response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_eighteen_unique_projects_across_all_six_domains(self):
        from .stage_projects import STAGE_PROJECTS, get_stage_project
        domains = ['web_dev', 'ai_ml', 'robotics', 'data_analytics', 'electronics', 'cybersecurity']
        stages = ['Beginner', 'Intermediate', 'Advanced']

        titles = set()
        for d in domains:
            for s in stages:
                p = get_stage_project(d, s)
                self.assertIsNotNone(p, f"Missing project for domain={d}, stage={s}")
                self.assertEqual(p['domain'], d)
                self.assertEqual(p['stage'], s)
                self.assertTrue(len(p['what_you_will_build']) > 15)
                self.assertGreaterEqual(len(p.get('requirements_list', [])), 3)
                self.assertGreaterEqual(len(p.get('implementation_steps', [])), 4)
                titles.add(p['title'])

        self.assertEqual(len(titles), 18, "All 18 projects must have unique titles across stages and domains")

    def test_project_visibility_at_roadmap_beginning_hides_actual_project_details(self):
        # At start, 0 of 4 beginner lessons completed
        response = self.client.get(reverse('dashboard', kwargs={'pk': self.goal.pk}))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # Shows simple stage project indicators
        self.assertIn("Beginner Project", content)
        self.assertIn("Intermediate Project", content)
        self.assertIn("Advanced Project", content)
        self.assertIn("LOCKED", content)

        # Does NOT reveal the actual project title or details at beginning
        from .stage_projects import get_stage_project
        web_beg = get_stage_project('web_dev', 'Beginner')
        self.assertNotIn(web_beg['title'], content)
        self.assertNotIn(web_beg['task'], content)

    def test_direct_project_url_access_is_blocked_when_stage_is_locked(self):
        # Direct URL access to ?stage=Beginner when beginner lessons are not done is blocked with 403
        response = self.client.get(reverse('project', kwargs={'pk': self.goal.pk}) + '?stage=Beginner')
        self.assertEqual(response.status_code, 403)
        content = response.content.decode('utf-8')

        # Renders the Locked Stage Gate
        self.assertIn("Stage Project is Locked", content)
        self.assertIn("Lessons Mastered", content)
        self.assertIn("Return to Dashboard", content)

        # Form / Brief / Implementation are NOT rendered while locked
        self.assertNotIn("Step-by-Step Implementation Guide", content)
        self.assertNotIn("Submit Project for Instant AI Evaluation", content)

        # POST directly to locked project URL is rejected/redirected
        post_resp = self.client.post(
            reverse('project', kwargs={'pk': self.goal.pk}) + '?stage=Beginner',
            {'submission_text': 'trying to bypass'}
        )
        self.assertRedirects(post_resp, reverse('dashboard', kwargs={'pk': self.goal.pk}))

    def test_beginner_project_unlocks_only_after_all_stage_lessons_completed(self):
        # Mark all 4 beginner nodes as completed
        for node in self.nodes:
            node.status = 'completed'
            node.phase = 'completed'
            node.save()

        # Now GET project should be UNLOCKED!
        response = self.client.get(reverse('project', kwargs={'pk': self.goal.pk}) + '?stage=Beginner')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # The project is UNLOCKED
        self.assertNotIn("Stage Project is Locked", content)
        from .stage_projects import get_stage_project
        self.assertIn("Pennywise", content)
        self.assertIn("Mandatory Requirements Checklist", content)
        self.assertIn("Submit Project for Instant AI Evaluation", content)

    def test_intermediate_and_advanced_projects_remain_locked_until_stage_complete(self):
        # Even after completing Beginner lessons, Intermediate project must remain LOCKED
        for node in self.nodes:
            node.status = 'completed'
            node.save()

        # Direct access to Intermediate stage project is locked
        resp_int = self.client.get(reverse('project', kwargs={'pk': self.goal.pk}) + '?stage=Intermediate')
        self.assertEqual(resp_int.status_code, 403)
        content_int = resp_int.content.decode('utf-8')
        self.assertIn("Intermediate Stage Project is Locked", content_int)

        # Direct access to Advanced stage project is locked
        resp_adv = self.client.get(reverse('project', kwargs={'pk': self.goal.pk}) + '?stage=Advanced')
        self.assertEqual(resp_adv.status_code, 403)
        content_adv = resp_adv.content.decode('utf-8')
        self.assertIn("Advanced Stage Project is Locked", content_adv)
