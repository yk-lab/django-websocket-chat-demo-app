from chat.models.room import Room
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.urls.base import reverse
from django.views.generic import CreateView


class RoomCreateForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name']


class IndexView(LoginRequiredMixin, CreateView):
    form_class = RoomCreateForm
    template_name = 'chat/index.html'
    queryset = Room.objects.order_by('-created_at')[:5]

    def get_context_data(self):
        context = super().get_context_data()
        context['objects'] = self.get_queryset()
        return context

    def get_success_url(self) -> str:
        return reverse('chat:room', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super(CreateView, self).form_valid(form)


index_view = IndexView.as_view()
