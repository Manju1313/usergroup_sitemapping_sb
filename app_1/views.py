from django.shortcuts import render
from .models import *
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .forms import *
from django.views import View  
from django.views.generic.edit import CreateView  
from django.views.generic.list import ListView  
from django.views.generic.detail import DetailView  
from django.views.generic.edit import UpdateView  
from django.views.generic.edit  import DeleteView
from django.urls import reverse, reverse_lazy  


# Create your views here.


def getData(request):
    """ Get Data of subdomain """
    subDomain = request.META['HTTP_HOST'].lower().split('.')
    i = 0
    if subDomain[0] == 'www':
        i = (i + 1)
    codeobj = slugify(subDomain[i])

    try:
        site_obj = Site.objects.get(name = codeobj).domain
    except:
        site_obj = None

    return site_obj


def login_view(request):
    heading = "Login"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        data = getData(request)
        if UserSiteMapping.objects.filter(user__username = username, site__domain = data).exists():

            try:
                findUser = User._default_manager.get(username__iexact=username)
            except User.DoesNotExist:
                findUser = None
            if findUser is not None:
                username = findUser.get_username()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                current_site = Site.objects.get(domain=request.META['HTTP_HOST'])
                request.session['site_id'] = current_site.id
                user_role = str(get_user(request).groups.last())

                if (user_role == 'football'):
                    return HttpResponse('hai select')
                
                elif (user_role == 'cricket'):
                    return HttpResponseRedirect('/replace/')

                elif (user_role == 'volleyball'):
                    return HttpResponseRedirect('/select/')
               
            else:
                logout(request)
                error_message = "Invalid Username and Password"
        else:
            logout(request)
            error_message = "Do not have access"
    return render(request, 'dashboard/login.html', locals())



@ login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@ login_required(login_url='/login/')
def select(request):
    return HttpResponse('<h1>Hello people</h1>' )


@ login_required(login_url='/login/')
def replace(request):
    current_site = request.session.get('site_id')
    user = get_user(request)
    user_role = str(get_user(request).groups.last())
    current_site = request.session.get('site_id')
    if (user_role == 'football'):    
        pass
    return render(request, 'index.html', locals())
















from rest_framework.response import Response
from rest_framework import status, generics
from .models import NoteModel
from .serializers import NoteSerializer
import math
from datetime import datetime


class Notes(generics.GenericAPIView):
    serializer_class = NoteSerializer
    queryset = NoteModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        notes = NoteModel.objects.all()
        total_notes = notes.count()
        if search_param:
            notes = notes.filter(title__icontains=search_param)
        serializer = self.serializer_class(notes[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_notes,
            "page": page_num,
            "last_page": math.ceil(total_notes / limit_num),
            "notes": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "note": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class NoteDetail(generics.GenericAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer

    def get_note(self, pk):
        try:
            return NoteModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        note = self.get_note(pk=pk)
        if note == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(note)
        return Response({"status": "success", "note": serializer.data})

    def patch(self, request, pk):
        note = self.get_note(pk)
        if note == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "note": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_note(pk)
        if note == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




#  class based Generic views
def function_view(request):  
    if request.method == 'GET':  
        return HttpResponse('response') 


class NewView(View):  
    def get(self, request):  
        return HttpResponse('<h1>response of generic view</h1>')  


class EmployeeCreate(CreateView):  
    model = Employee  
    template_name = 'model_form.html'

    fields = '__all__'  
    # success_url = '/retrieve/'    
    success_url = reverse_lazy('EmployeeRetrieve')  



class EmployeeRetrieve(ListView):  
    model = Employee 
    template_name = 'model_list.html'


class EmployeeDetail(DetailView):  
    model = Employee  
    template_name = 'model_detail.html'
    

class EmployeeUpdate(UpdateView):  
    model = Employee  
    fields = '__all__'  
    template_name = 'model_form.html'
    success_url = '/retrieve/'  


class EmployeeDelete(DeleteView):  
    model = Employee
    fields = '__all__'  
    template_name = 'model_delete.html'
    success_url = '/retrieve/'






#  Email confirmation
from django.http import HttpResponse  
from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate  
from .forms import SignupForm  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
  
def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, 'signup.html', {'form': form})  


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  




