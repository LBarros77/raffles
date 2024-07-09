import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from django.contrib.auth.decorators import (
	login_required,
	permission_required
)
from django.contrib import messages
from django.views import View
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from core import settings
from .models import Raffle, Image
from .forms import (
	RaffleForm,
	ImageForm,
	AutomaticBuyFormSet,
	PromotionFormSet,
	AwardedQuotaFormSet
)


permissions = ['raffle.*']
decorators = [login_required, permission_required(permissions, raise_exception=True)]

# @method_decorator(decorators, name='dispatch')
class CreateView(View):
	template_name = 'raffle/create.html'
	context = {}

	def get(self, request):
		form = RaffleForm()
		form_image = ImageForm()
		formset_autobuy = AutomaticBuyFormSet()
		# formset_promotion = PromotionFormSet()
		# formset_quota = AwardedQuotaFormSet()
		self.context = {
			'form': form,
			'form_image': form_image,
			'formset_autobuy': formset_autobuy,
			# 'formset_promotion': formset_promotion,
			# 'formset_quota': formset_quota,
		}
		return render(request, self.template_name, self.context)

	def post(self, request):
		form = RaffleForm(request.POST)
		images = request.FILES.getlist('image')
		if not form.is_valid():
			self.context['form'] = form
			return render(request, self.template_name, self.context)
		if not request.user.is_authenticated:
			return redirect('signin')
		product = form.save(commit=False)
		product.owner = request.user
		product.save()
		for image in images:
			Image.objects.create(product=product, image=image)
		formset_autobuy = AutomaticBuyFormSet(instance=product)
		# formset_promotion = PromotionFormSet(instance=product)
		# formset_quota = AwardedQuotaFormSet(instance=product)
		if formset_autobuy.is_valid(): formset_autobuy.save()
		# if formset_promotion.is_valid(): formset_promotion.save()
		# if formset_quota.is_valid(): formset_quota.save()
		messages.success(request, "Your Raffle has been created succesfully!")
		return redirect('product:list')


# @method_decorator(decorators, name='dispatch')
class UpdateView(View):
	template_name = 'raffle/update.html'
	context = {}

	def get(self, request, id):
		product = Raffle.objects.get(id=id)
		self.context = {
			'form': RaffleForm(instance=product),
			'form_image': ImageForm(instance=product),
			'formset_autobuy': AutomaticBuyFormSet(instance=product),
		}
		return render(request, self.template_name, self.context)

	def post(self, request, id):
		product = Raffle.objects.get(id=id)
		form = RaffleForm(request.POST, instance=product)
		if form.is_valid():
			product = form.save()
		images = request.FILES.getlist('image')
		gallery = Image.objects.filter(product=product)
		gallery_filenames = [(obj.image.path).split('/')[-1] for obj in gallery]
		image_filenames = [image.name for image in images]
		for index, filename in enumerate(image_filenames):
			if filename not in gallery_filenames:
				image = images[index]
				Image.objects.create(product=product, image=image)
		formset_autobuy = AutomaticBuyFormSet(request.POST, instance=product)
		if formset_autobuy.is_valid(): formset_autobuy.save()
		messages.success(request, 'Successfully updated!')
		return redirect('product:list')
		# messages.error(request, 'Changes not valids. Retry, please.')
		# return render(request, self.template_name, self.context)

	def patch(self, request, id):
		try:
			product = Raffle.objects.get(id=id)
			gallery = Image.objects.filter(product=product)
			gallery_data = serialize('json', gallery)
			return JsonResponse(gallery_data, safe=False)
		except Raffle.DoesNotExist:
			return JsonResponse({'error': 'Product or Image not found'}, status=404)

	def delete(self, request, id, image_id=None):
		try:
			image = Image.objects.get(id=image_id)
			image.delete()
			return JsonResponse({'success': 'Image deleted succesfully'}, status=200)
		except Image.DoesNotExist:
			return JsonResponse({'error': 'Image not found'}, status=404)


@login_required(redirect_field_name='signin')
def list(request):
	try:
		raffles = Raffle.objects.all()
		return render(request, 'raffle/list.html', {'products': raffles})
	except:
		return render(request, 'raffle/list.html', {'products': ()})

@login_required(redirect_field_name='signin')
def details(request, id):
	user = request.user
	raffle = Raffle.objects.filter(owner=user, id=id)
	return render(request, 'raffle/details.html', {'raffle': raffle})

@login_required(redirect_field_name='signin')
@require_http_methods(['DELETE'])
def delete(request, id):
	raffle = get_object_or_404(Raffle, id=id)
	raffle.delete()
	return render(request, 'partials/tbody.html')
