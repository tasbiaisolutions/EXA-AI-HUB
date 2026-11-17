from django import forms
from .models import UserGoal

class GoalGenerationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', args[0] if args else None)
        if data is not None and 'chosen_tier' not in data and 'current_level' in data:
            data = data.copy()
            selected_level = data['current_level']
            data['chosen_tier'] = (
                selected_level
                if selected_level in ('Beginner', 'Intermediate', 'Advanced')
                else 'Beginner'
            )
            if args:
                args = (data, *args[1:])
            else:
                kwargs['data'] = data
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserGoal
        fields = ['goal', 'domain', 'chosen_tier', 'existing_skills', 'user_name']
        widgets = {
            'goal': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Become a Full Stack Developer, Robotics Engineer, or Data Analyst'
            }),
            'domain': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Web Development, Robotics, Data Analytics, Cloud, UI/UX'
            }),
            'chosen_tier': forms.Select(attrs={
                'class': 'form-select'
            }),
            'existing_skills': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'e.g. Basic HTML, Python syntax, or none (complete beginner)',
                'rows': 3
            }),
            'user_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Name'
            }),
        }
