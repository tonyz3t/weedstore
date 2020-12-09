from django import forms
from .models import Product, Category


class ProductModelForm(forms.ModelForm):
   
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Product Name'}),
            'price': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'The Price'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'A Description'}),
            
            'category': forms.Select(attrs={'class':'form-control dropDown '}),
            'is_featured': forms.CheckboxInput(attrs={'class':'bigCheckbox'}),
        }
      