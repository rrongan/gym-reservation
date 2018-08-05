from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime

from reservation.models import User, Facility, Reservation
from reservation.forms import UserForm, UserUpdateForm, FacilityForm, ReservationForm, SignUpForm, ProfileUpdateForm, UserReservationForm
from django.contrib.auth.forms import PasswordChangeForm


# Check Admin Account
def check_admin(user):
    return user.user_type == 'Admin'


# Permission Denied
@login_required
def permission_denied(request):
    return render(request, 'registration/no_permission.html')


# User CRUD
@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def user_list(request):
    user = User.objects.all()
    return render(request, 'user/user_list.html', {'users': user})


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def save_user_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            data['form_is_valid'] = True
            user = User.objects.all()
            data['html_user_list'] = render_to_string('user/includes/partial_user_list.html', {
                'users': user
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
    else:
        form = UserForm()
    return save_user_form(request, form, 'user/includes/partial_user_create.html')


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    data = dict()
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            user = User.objects.all()
            data['html_user_list'] = render_to_string('user/includes/partial_user_list.html', {
                'users': user
            })
        else:
            data['form_is_valid'] = False
    else:
        form = UserUpdateForm(instance=user)

    context = {'form': form}
    data['html_form'] = render_to_string('user/includes/partial_user_update.html', context, request=request)
    return JsonResponse(data)


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    data = dict()
    if request.method == 'POST':
        user.delete()
        data['form_is_valid'] = True
        user = User.objects.all()
        data['html_user_list'] = render_to_string('user/includes/partial_user_list.html', {
            'users': user
        })
    else:
        context = {'users': user}
        data['html_form'] = render_to_string('user/includes/partial_user_delete.html', context, request=request,)
    return JsonResponse(data)


# Facility CRUD
@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def facility_list(request):
    facility = Facility.objects.all()
    return render(request, 'facility/facility_list.html', {'facility': facility})


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def save_facility_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            facility = Facility.objects.all()
            data['html_facility_list'] = render_to_string('facility/includes/partial_facility_list.html', {
                'facility': facility
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def facility_create(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST)
    else:
        form = FacilityForm()
    return save_facility_form(request, form, 'facility/includes/partial_facility_create.html')


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def facility_update(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    if request.method == 'POST':
        form = FacilityForm(request.POST, instance=facility)
    else:
        form = FacilityForm(instance=facility)
    return save_facility_form(request, form, 'facility/includes/partial_facility_update.html')


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def facility_delete(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    data = dict()
    if request.method == 'POST':
        facility.delete()
        data['form_is_valid'] = True
        facility = Facility.objects.all()
        data['html_facility_list'] = render_to_string('facility/includes/partial_facility_list.html', {
            'facility': facility
        })
    else:
        context = {'facility': facility}
        data['html_form'] = render_to_string('facility/includes/partial_facility_delete.html', context, request=request,)
    return JsonResponse(data)


# Reservation CRUD
@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def reservation_list(request):
    reservation = Reservation.objects.all()
    return render(request, 'reservation/reservation_list.html', {'reservation': reservation})


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def save_reservation_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            reservation = Reservation.objects.all()
            data['html_reservation_list'] = render_to_string('reservation/includes/partial_reservation_list.html', {
                'reservation': reservation
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
    else:
        form = ReservationForm()
    return save_reservation_form(request, form, 'reservation/includes/partial_reservation_create.html')


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def reservation_update(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
    else:
        form = ReservationForm(instance=reservation)
    return save_reservation_form(request, form, 'reservation/includes/partial_reservation_update.html')


@login_required
@user_passes_test(check_admin, login_url='permission_denied', redirect_field_name=None)
def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    data = dict()
    if request.method == 'POST':
        reservation.delete()
        data['form_is_valid'] = True
        reservation = Reservation.objects.all()
        data['html_reservation_list'] = render_to_string('reservation/includes/partial_reservation_list.html', {
            'reservation': reservation
        })
    else:
        context = {'reservation': reservation}
        data['html_form'] = render_to_string('reservation/includes/partial_reservation_delete.html', context, request=request,)
    return JsonResponse(data)


# Sign Up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# User Profile
@login_required
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'profile/user_profile.html', {'users': user})


@login_required
def user_profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    data = dict()
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            user = get_object_or_404(User, pk=pk)
            data['html_user_profile_list'] = render_to_string('profile/includes/partial_user_profile_list.html', {
                'users': user
            })
        else:
            data['form_is_valid'] = False
    else:
        form = ProfileUpdateForm(instance=user)

    context = {'form': form}
    data['html_form'] = render_to_string('profile/includes/partial_user_profile_update.html', context, request=request)
    return JsonResponse(data)


@login_required
def user_profile_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    data = dict()
    if request.method == 'POST':
        user.delete()
        data['form_is_valid'] = True
        logout(request)
    else:
        context = {'users': user}
        data['html_form'] = render_to_string('profile/includes/partial_user_profile_delete.html', context, request=request,)
    return JsonResponse(data)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/change_password.html', {
        'form': form
    })


# User Reservation
@login_required
def user_reservation_list(request, uid):
    reservation = Reservation.objects.all().filter(uid=uid)
    date = reservation.values_list('date', flat=True).distinct()
    res_ids = [reservation.id for reservation in Reservation.objects.all() if reservation.get_end_datetime() > datetime.now()]
    print(res_ids)
    reservation = reservation.filter(id__in=res_ids)
    return render(request, 'user_reservation/user_reservation_list.html', {'reservation': reservation, 'date': date})


@login_required
def save_user_reservation_form(request, form, template_name, uid):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.uid = get_object_or_404(User, pk=uid)
            reservation.save()
            data['form_is_valid'] = True
            reservation = Reservation.objects.all().filter(uid=uid)
            user = get_object_or_404(User, pk=uid)
            date = reservation.values_list('date', flat=True).distinct()
            res_ids = [reservation.id for reservation in Reservation.objects.all() if
                       reservation.get_end_datetime() > datetime.now()]
            reservation = reservation.filter(id__in=res_ids)
            data['html_user_reservation_list'] = render_to_string('user_reservation/includes/partial_user_reservation_list.html', {
                'user': user,
                'reservation': reservation,
                'date': date
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def user_reservation_create(request, uid):
    if request.method == 'POST':
        form = UserReservationForm(request.POST)
    else:
        form = UserReservationForm()
    return save_user_reservation_form(request, form, 'user_reservation/includes/partial_user_reservation_create.html', uid)


@login_required
def user_reservation_update(request, uid, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = UserReservationForm(request.POST, instance=reservation)
    else:
        form = UserReservationForm(instance=reservation)
    return save_user_reservation_form(request, form, 'user_reservation/includes/partial_user_reservation_update.html', uid)


@login_required
def user_reservation_delete(request, uid, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    data = dict()
    if request.method == 'POST':
        reservation.delete()
        data['form_is_valid'] = True
        reservation = Reservation.objects.all().filter(uid=uid)
        user = get_object_or_404(User, pk=uid)
        date = reservation.values_list('date', flat=True).distinct()
        res_ids = [reservation.id for reservation in Reservation.objects.all() if
                   reservation.get_end_datetime() >= datetime.now()]
        reservation = reservation.filter(id__in=res_ids)
        data['html_user_reservation_list'] = render_to_string(
            'user_reservation/includes/partial_user_reservation_list.html', {
                'user': user,
                'reservation': reservation,
                'date': date
            })
    else:
        context = {'reservation': reservation}
        data['html_form'] = render_to_string('user_reservation/includes/partial_user_reservation_delete.html', context, request=request,)
    return JsonResponse(data)


# User History
@login_required
def user_history_list(request, uid):
    reservation = Reservation.objects.all().filter(uid=uid)
    date = reservation.values_list('date', flat=True).distinct()
    res_ids = [reservation.id for reservation in Reservation.objects.all() if reservation.get_end_datetime() < datetime.now()]
    reservation = reservation.filter(id__in=res_ids)
    return render(request, 'user_history/user_history_list.html', {'reservation': reservation, 'date': date})


# User Facility
@login_required
def user_facility_list(request):
    facility = Facility.objects.all()
    if request.GET.get('facility_select'):
        facility_filter = request.GET.get('facility_select')
        reservation = Reservation.objects.filter(fid=facility_filter)
        facility = sorted(facility, key=lambda x: x.id == int(facility_filter), reverse=True)
    else:
        reservation = Reservation.objects.filter(fid=facility.first())
    date = reservation.values_list('date', flat=True).distinct()
    res_ids = [reservation.id for reservation in Reservation.objects.all() if reservation.get_end_datetime() > datetime.now()]
    reservation = reservation.filter(id__in=res_ids)
    return render(request, 'user_facility/user_facility_list.html', {'facility': facility, 'reservation': reservation, 'date': date})
