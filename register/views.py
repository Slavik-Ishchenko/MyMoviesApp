import datetime

import jwt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import SignInForm, SignUpForm
from .models import MyUser
from .serializers import SignUpSerializer, UserSerializer


def in_profile(request):
    return render(request, 'register/profile.html')


def logout_view(request):
    logout(request)
    return HttpResponse('Вы успешно вышли :*')


class SignIn(View):

    def get(self, request, *args, **kwargs):
        form = SignInForm(request.POST or None)
        context = {'form': form}
        return render(request, 'register/sign_in.html', context)

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = authenticate(username=username, password=password, email=email)
            if user:
                login(request, user)
                return HttpResponseRedirect('profile')
        return render(request, 'register/sign_in.html', {'form': form})


class SignUp(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        context = {'form': form}
        return render(request, 'register/sign_up.html', context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=True)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.date_of_birth = form.cleaned_data['date_of_birth']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('profile')
        context = {'form': form}
        return render(request, 'register/sign_up.html', context)


class RegSignIn(APIView):

    def post(self, request):
        """Sign IN -- API view"""
        email = request.data['email']
        password = request.data['password']
        user = MyUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found :(')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password :(')
        payload = {'id': user.id,
                   'st': str(datetime.datetime.utcnow()) + str(datetime.timedelta(minutes=60)),
                   'dtc': str(datetime.datetime.utcnow())}
        """st = storage time of token,
                 dtc = date of creation"""
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated :(')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated :(')
        user = MyUser.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'SUCCESS :*'}
        return response


@api_view(['POST'])
def sign_up_api(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'SUCCESS'
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)
