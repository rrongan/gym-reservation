from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from reservation.models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class UserForm(UserCreationForm):
    USERTYPE_CHOICES = (
        ('Admin', 'Admin'),
        ('Default', 'Default'),
    )
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    role = forms.CharField(max_length=30)
    mobile_number = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    user_type = models.CharField(max_length=15, choices=USERTYPE_CHOICES, default='Default')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'mobile_number', 'role', 'user_type')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role', 'mobile_number', 'user_type')
        exclude = ('password',)


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ('name',)


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ('uid', 'fid', 'date', 'time', 'duration', 'status')
        widgets = {
            'date': DateInput(),
            'time': TimeInput()
        }

    def clean(self):
        cleaned_data = super(ReservationForm, self).clean()
        dt = datetime.combine(cleaned_data.get('date'), cleaned_data.get('time')) + timedelta(minutes=cleaned_data.get('duration') * 60)
        if dt < datetime.now():
            raise ValidationError("The Date And Time Cannot Be In The Past!")


class UserReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ('fid', 'date', 'time', 'duration')
        widgets = {
            'date': DateInput(),
            'time': TimeInput()
        }

    def clean(self):
        reservation = Reservation.objects.all()
        cleaned_data = super(UserReservationForm, self).clean()
        sdt = datetime.combine(cleaned_data.get('date'), cleaned_data.get('time'))
        edt = datetime.combine(cleaned_data.get('date'), cleaned_data.get('time')) + timedelta(minutes=cleaned_data.get('duration') * 60)
        for r in reservation:
            rsdt = r.get_start_datetime()
            redt = r.get_end_datetime()
            facility = r.fid
            if r.status != 'Declined':
                if facility == cleaned_data.get('fid'):
                    if rsdt < sdt < redt:
                        raise ValidationError("The facility has been booked between "
                                              + str(rsdt.time()) + " and " + str(redt.time()) + "!")
                    elif rsdt < edt < redt:
                        raise ValidationError("The facility has been booked between "
                                              + str(rsdt.time()) + " and " + str(redt.time()) + "!")
        if sdt < datetime.now():
            raise ValidationError("The Date And Time Cannot Be In The Past!")


class UserHistoryForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('fid', 'date', 'time', 'duration', 'status')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    role = forms.CharField(max_length=30)
    mobile_number = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'mobile_number', 'role')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role', 'mobile_number')
        exclude = ('password',)
