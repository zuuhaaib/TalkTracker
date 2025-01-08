from django import forms

class TextInputForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10,  # Customize the number of rows in the textarea
            'placeholder': 'Enter your text here...',
            'style': 'width: 100%; padding: 12px; border-radius: 5px;'  # Inline CSS for styling
        }),
        label='Enter your text',
        required=True
    )
