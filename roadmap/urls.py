from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('onboarding/', views.odin_onboarding_view, name='odin_onboarding'),
    path('dashboard/<int:pk>/', views.dashboard_view, name='dashboard'),
    
    # Technology Expert Workflows
    path('skill/<int:pk>/learn/', views.learning_view, name='learning'),
    path('skill/<int:pk>/practice/submit/', views.practice_submit_view, name='practice_submit'),
    path('goal/<int:pk>/project/', views.project_view, name='project'),
    path('project/<int:pk>/submission/', views.project_submission_upload_view, name='project_submission_upload'),
    path('submission/<int:pk>/', views.submission_result_view, name='submission_result'),
    path('expert/chat/<int:pk>/', views.expert_chat_view, name='expert_chat'),
    
    # Mentor Flow Routes
    path('skill/<int:pk>/assessment/', views.skill_assessment_view, name='skill_assessment'),
    path('skill/<int:pk>/map/', views.skill_map_view, name='skill_map'),
    path('skill/<int:pk>/teach/', views.teach_concept_view, name='teach_concept'),
    path('skill/<int:pk>/quiz/', views.quiz_view, name='quiz'),
    path('skill/<int:pk>/quiz/submit/', views.quiz_submit_view, name='quiz_submit'),
    path('quiz/result/<int:pk>/', views.quiz_result_view, name='quiz_result'),
    path('skill/<int:pk>/advance/', views.advance_concept_view, name='advance_concept'),
    path('skill/<int:pk>/review/', views.review_view, name='review'),
    path('skill/<int:pk>/overview/', views.concept_overview_view, name='concept_overview'),
    path('goal/<int:pk>/delete/', views.delete_goal_view, name='delete_goal'),
    path('goal/<int:pk>/restart/', views.restart_goal_view, name='restart_goal'),
    path('goal/<int:pk>/enroll/', views.enroll_course_view, name='enroll_course'),
    path('library/', views.library_view, name='library'),
]
