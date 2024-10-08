from django import forms
from django.forms import inlineformset_factory
from .models import Category, Product, Image
from apps.store.models import AutomaticBuy, AwardedQuota, Promotion


class_default = 'form-control mb-3'

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'scheduled_date', 'number_quantity', 'category', 'price', 'min_quantity', 'digital', 'description', 'owner']
		labels = {
			'title': 'Nome da Rifa',
			'scheduled_date': 'Data',
			'number_quantity': 'Quantidade de números',
			'category': 'Categorias',
			'price': 'Preço',
			'min_quantity': 'Quantidade mínima',
			'digital': 'Digital',
			'description': 'Descrição',
			'owner': '',
		}
		widgets = {
			'title': forms.TextInput(attrs={'class': class_default}),
			'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': class_default}),
			'number_quantity': forms.Select(attrs={'class': class_default}),
			'category': forms.Select(attrs={'class': 'form-control mb-3'}),
			'price': forms.TextInput(attrs={'class': class_default}),
			'min_quantity': forms.NumberInput(attrs={'class': class_default}),
			'digital': forms.NullBooleanSelect(attrs={'class': class_default}),
			'description': forms.Textarea(attrs={'class': class_default, 'rows': 3, 'cols': 50, 'aria-describedby': 'Descrição de Rifa'}),
			'owner': forms.TextInput(attrs={'readonly': True, 'hidden': True,})
		}

	def __init__(self, *args, **kwargs):
		super(ProductForm, self).__init__(*args, **kwargs)
		self.fields['owner'].required = False


class ImageForm(forms.ModelForm):
	image = MultipleFileField()

	class Meta:
		model = Image
		fields = '__all__'
		widgets = {
			'product': forms.TextInput(attrs={'hidden': True,}),
			'image': forms.TextInput(
				attrs={'type': 'file', 'accept': 'image/png, image/jpeg', 'multiple': True}),
		}

	def __init__(self, *args, **kwargs):
		product = kwargs.pop('product', None)
		super(ImageForm, self).__init__(*args, **kwargs)
		if product:
			self.fields['product'].initial = product
		self.fields['product'].required = False
		self.fields['image'].required = False

	def save(self, commit=True):
		instance = super(ImageForm, self).save(commit=False)
		return instance.save() if commit else instance


class AutomaticBuyForm(forms.ModelForm):
	class Meta:
		model = AutomaticBuy
		fields = ['quantity', 'more_popular']
		widgets = {
			'quantity': forms.NumberInput(
				attrs={'class': class_default, 'id': 'radio1'}),
			'more_popular': forms.TextInput(
				attrs={'type': 'radio', 'class': 'form-check-input mb-3', 'id': 'radio1'}),
		}


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name']
		widgets = {
			'name': forms.TextInput(attrs={'class': class_default}),
		}


class PromotionForm(forms.ModelForm):
	class Meta:
		model = Promotion
		fields = ['amount', 'price']
		widgets = {
			'amount': forms.NumberInput(
				attrs={'type': 'number', 'class': class_default}),
			'price': forms.TextInput(
				attrs={'class': 'form-control'}),
		}


class AwardedQuotaForm(forms.ModelForm):
	class Meta:
		model = AwardedQuota
		fields = ['number']
		widgets = {
			'number': forms.NumberInput(
				attrs={'type': 'number', 'class': class_default}),
		}


ImageInlineFormSet = inlineformset_factory(
	Product,
	Image,
	fields=['image'],
	widgets = {
		'image': forms.ClearableFileInput(
			attrs={'allow_multiple_selected': True, 'type': 'file', 'class': 'bi bi-image mb-3'}),
	},
	max_num=5,
	extra=1,
	can_delete=False
)

AutomaticBuyFormSet = inlineformset_factory(
	Product,
	AutomaticBuy,
	fields=['quantity', 'more_popular'],
	widgets = {
		'quantity': forms.NumberInput(
			attrs={'class': class_default}),
		'more_popular': forms.TextInput(
			attrs={'type': 'radio', 'class': 'form-check-input mb-3'}),
	},
	extra=4,
	can_delete=False
)

PromotionFormSet = inlineformset_factory(
	Product,
	Promotion,
	fields = ['amount', 'price'],
	widgets = {
		'amount': forms.NumberInput(
			attrs={'type': 'number', 'class': class_default}),
		'price': forms.TextInput(
			attrs={'class': 'form-control'}),
	},
	extra=1,
	can_delete=False
)

AwardedQuotaFormSet = inlineformset_factory(
	Product,
	AwardedQuota,
	fields = ['number'],
	widgets = {
		'number': forms.NumberInput(
			attrs={'type': 'number', 'class': class_default}),
	},
	extra=1,
	can_delete=False
)
