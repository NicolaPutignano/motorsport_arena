from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Community, CommunityMember
from .serializers import CommunitySerializer
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .forms import EventForm, RaceForm, CircuitForm, CarForm
from .models import Event, Race, Circuit, Car


class CommunityCreateView(generics.CreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        community = serializer.save(created_by=self.request.user)
        CommunityMember.objects.create(user=self.request.user, community=community, role='Admin')
        return Response(serializer.data)
    


def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.created_by = request.user
            event.save()
            
            if event.mode in ['singola', 'squadre']:
                race_form = RaceForm(request.POST)
                if race_form.is_valid():
                    race = race_form.save(commit=False)
                    race.event = event
                    race.save()
                    
                    car_formset = CarFormSet(request.POST, queryset=Car.objects.none())
                    if car_formset.is_valid():
                        for car_form in car_formset:
                            car = car_form.save(commit=False)
                            car.race = race
                            car.save()
                    return redirect('event_detail', event_id=event.id)

            elif event.mode == 'torneo':
                RaceFormSet = modelformset_factory(Race, form=RaceForm, extra=5)
                race_formset = RaceFormSet(request.POST, queryset=Race.objects.none())
                if race_formset.is_valid():
                    for race_form in race_formset:
                        race = race_form.save(commit=False)
                        race.event = event
                        race.save()
                        
                        car_formset = CarFormSet(request.POST, queryset=Car.objects.none())
                        if car_formset.is_valid():
                            for car_form in car_formset:
                                car = car_form.save(commit=False)
                                car.race = race
                                car.save()
                    return redirect('event_detail', event_id=event.id)

    else:
        event_form = EventForm()
        race_form = RaceForm()
        RaceFormSet = modelformset_factory(Race, form=RaceForm, extra=5)
        race_formset = RaceFormSet(queryset=Race.objects.none())
        CarFormSet = modelformset_factory(Car, form=CarForm, extra=3)
        car_formset = CarFormSet(queryset=Car.objects.none())

    return render(request, 'create_event.html', {
        'event_form': event_form,
        'race_form': race_form,
        'race_formset': race_formset,
        'car_formset': car_formset,
    })