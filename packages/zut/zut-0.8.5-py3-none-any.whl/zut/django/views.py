from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.forms.forms import BaseForm
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, View
from .mixins import AllowAnonymousMixin

class IndexView(AllowAnonymousMixin, TemplateView):
    template_name = 'zut/index.html'


class LangView(AllowAnonymousMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        redirect_to = self.request.POST.get('next', self.request.GET.get('next', '/'))

        if not settings.USE_I18N:
            messages.error(request, mark_safe(f"Translations are not enabled."))
            return HttpResponseRedirect(redirect_to)
            
        lang = self.request.POST.get('lang', self.request.GET.get('lang', None))
        if not lang:
            messages.error(request, mark_safe(f"No `lang` parameter provided."))
            return HttpResponseRedirect(redirect_to)
        
        lang_name = None
        for a_lang, a_name in settings.LANGUAGES:
            if a_lang == lang:
                lang_name = a_name
                break 
        
        if lang_name is None:
            messages.error(request, mark_safe(f"Unknown or unsupported language <strong>{lang}</strong>."))
            return HttpResponseRedirect(redirect_to)

        response = HttpResponseRedirect(redirect_to)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        messages.success(request, mark_safe(f"Language changed to <strong>{lang}</strong> ({lang_name})."))
        return response


class LoginView(AllowAnonymousMixin, auth_views.LoginView):
    template_name = 'zut/login.html'


class LogoutView(AllowAnonymousMixin, auth_views.LogoutView):
    template_name = 'zut/logged_out.html'
