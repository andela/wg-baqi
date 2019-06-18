# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import logging
import uuid
import datetime
import json
import ast

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import (HttpResponseRedirect, HttpResponseForbidden,
                         HttpResponse, )
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy, ugettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, UpdateView
from rest_framework.response import Response
from rest_framework import status

from wger.core.models import (RepetitionUnit, WeightUnit, DaysOfWeek, )
from wger.manager.models import (Workout, WorkoutSession, WorkoutLog,
                                 Schedule, Day, Exercise, Setting, Set, )
from wger.manager.forms import (WorkoutForm, WorkoutSessionHiddenFieldsForm,
                                WorkoutCopyForm)
from wger.utils.generic_views import (WgerFormMixin, WgerDeleteMixin)
from wger.utils.helpers import make_token

logger = logging.getLogger(__name__)


# ************************
# Workout functions
# ************************
@login_required
def overview(request):
    '''
    An overview of all the user's workouts
    '''

    template_data = {}

    workouts = Workout.objects.filter(user=request.user)
    (current_workout, schedule) = Schedule.objects.get_current_workout(
        request.user)
    template_data['workouts'] = workouts
    template_data['current_workout'] = current_workout

    return render(request, 'workout/overview.html', template_data)


def view(request, pk):
    '''
    Show the workout with the given ID
    '''
    template_data = {}
    workout = get_object_or_404(Workout, pk=pk)
    user = workout.user
    is_owner = request.user == user

    if not is_owner and not user.userprofile.ro_access:
        return HttpResponseForbidden()

    canonical = workout.canonical_representation
    uid, token = make_token(user)

    # Create the backgrounds that show what muscles the workout will work on
    muscles_front = []
    muscles_back = []
    for i in canonical['muscles']['front']:
        if i not in muscles_front:
            muscles_front.append(
                'images/muscles/main/muscle-{0}.svg'.format(i))
    for i in canonical['muscles']['back']:
        if i not in muscles_back:
            muscles_back.append(
                'images/muscles/main/muscle-{0}.svg'.format(i))

    for i in canonical['muscles']['frontsecondary']:
        if i not in muscles_front and i not in canonical['muscles']['front']:
            muscles_front.append(
                'images/muscles/secondary/muscle-{0}.svg'.format(i))
    for i in canonical['muscles']['backsecondary']:
        if i not in muscles_back and i not in canonical['muscles']['back']:
            muscles_back.append(
                'images/muscles/secondary/muscle-{0}.svg'.format(i))

    # Append the silhouette of the human body as the last entry so the browser
    # renders it in the background
    muscles_front.append('images/muscles/muscular_system_front.svg')
    muscles_back.append('images/muscles/muscular_system_back.svg')

    template_data['workout'] = workout
    template_data['muscle_backgrounds_front'] = muscles_front
    template_data['muscle_backgrounds_back'] = muscles_back
    template_data['uid'] = uid
    template_data['token'] = token
    template_data['is_owner'] = is_owner
    template_data['owner_user'] = user
    template_data['show_shariff'] = is_owner

    return render(request, 'workout/view.html', template_data)


@login_required
def copy_workout(request, pk):
    '''
    Makes a copy of a workout
    '''

    workout = get_object_or_404(Workout, pk=pk)
    user = workout.user
    is_owner = request.user == user

    if not is_owner and not user.userprofile.ro_access:
        return HttpResponseForbidden()

    # Process request
    if request.method == 'POST':
        workout_form = WorkoutCopyForm(request.POST)

        if workout_form.is_valid():

            # Copy workout
            days = workout.day_set.all()

            workout_copy = workout
            workout_copy.pk = None
            workout_copy.comment = workout_form.cleaned_data['comment']
            workout_copy.user = request.user
            workout_copy.save()

            # Copy the days
            for day in days:
                sets = day.set_set.all()

                day_copy = day
                days_of_week = [i for i in day.day.all()]
                day_copy.pk = None
                day_copy.training = workout_copy
                day_copy.save()
                for i in days_of_week:
                    day_copy.day.add(i)
                day_copy.save()

                # Copy the sets
                for current_set in sets:
                    current_set_id = current_set.id
                    exercises = current_set.exercises.all()

                    current_set_copy = current_set
                    current_set_copy.pk = None
                    current_set_copy.exerciseday = day_copy
                    current_set_copy.save()

                    # Exercises has Many2Many relationship
                    current_set_copy.exercises.set(exercises)

                    # Go through the exercises
                    for exercise in exercises:
                        settings = exercise.setting_set.filter(
                            set_id=current_set_id)

                        # Copy the settings
                        for setting in settings:
                            setting_copy = setting
                            setting_copy.pk = None
                            setting_copy.set = current_set_copy
                            setting_copy.save()

            return HttpResponseRedirect(
                reverse('manager:workout:view', kwargs={'pk': workout.id}))
    else:
        workout_form = WorkoutCopyForm({'comment': workout.comment})

        template_data = {}
        template_data.update(csrf(request))
        template_data['title'] = _('Copy workout')
        template_data['form'] = workout_form
        template_data['form_action'] = reverse('manager:workout:copy',
                                               kwargs={'pk': workout.id})
        template_data['form_fields'] = [workout_form['comment']]
        template_data['submit_text'] = _('Copy')
        template_data[
            'extend_template'] = 'base_empty.html' if request.is_ajax() else 'base.html'

        return render(request, 'form.html', template_data)


@login_required
def add(request):
    '''
    Add a new workout and redirect to its page
    '''
    workout = Workout()
    workout.user = request.user
    workout.save()

    return HttpResponseRedirect(workout.get_absolute_url())


class WorkoutDeleteView(WgerDeleteMixin, LoginRequiredMixin, DeleteView):
    '''
    Generic view to delete a workout routine
    '''

    model = Workout
    fields = ('comment',)
    success_url = reverse_lazy('manager:workout:overview')
    messages = ugettext_lazy('Successfully deleted')

    def get_context_data(self, **kwargs):
        context = super(WorkoutDeleteView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('manager:workout:delete',
                                         kwargs={'pk': self.object.id})
        context['title'] = _(u'Delete {0}?').format(self.object)

        return context


class WorkoutEditView(WgerFormMixin, LoginRequiredMixin, UpdateView):
    '''
    Generic view to update an existing workout routine
    '''

    model = Workout
    form_class = WorkoutForm
    form_action_urlname = 'manager:workout:edit'

    def get_context_data(self, **kwargs):
        context = super(WorkoutEditView, self).get_context_data(**kwargs)
        context['title'] = _(u'Edit {0}').format(self.object)

        return context


class LastWeightHelper:
    '''
    Small helper class to retrieve the last workout log for a certain
    user, exercise and repetition combination.
    '''
    user = None
    last_weight_list = {}

    def __init__(self, user):
        self.user = user

    def get_last_weight(self, exercise, reps, default_weight):
        '''
        Returns an emtpy string if no entry is found

        :param exercise:
        :param reps:
        :param default_weight:
        :return: WorkoutLog or '' if none is found
        '''
        key = (self.user.pk, exercise.pk, reps, default_weight)
        if self.last_weight_list.get(key) is None:
            last_log = WorkoutLog.objects.filter(user=self.user,
                                                 exercise=exercise,
                                                 reps=reps).order_by('-date')
            default_weight = '' if default_weight is None else default_weight
            weight = last_log[
                0].weight if last_log.exists() else default_weight
            self.last_weight_list[key] = weight

        return self.last_weight_list.get(key)


@login_required
def timer(request, day_pk):
    '''
    The timer view ("gym mode") for a workout
    '''

    day = get_object_or_404(Day, pk=day_pk, training__user=request.user)
    canonical_day = day.canonical_representation
    context = {}
    step_list = []
    last_log = LastWeightHelper(request.user)

    # Go through the workout day and create the individual 'pages'
    for set_list_dict in canonical_day['set_list']:

        if not set_list_dict['is_superset']:
            for exercise_dict in set_list_dict['exercise_list']:
                exercise = exercise_dict['obj']
                for key, element in enumerate(exercise_dict['reps_list']):
                    reps = exercise_dict['reps_list'][key]
                    rep_unit = exercise_dict['repetition_units'][key]
                    weight_unit = exercise_dict['weight_units'][key]
                    default_weight = last_log.get_last_weight(exercise, reps,
                                                              exercise_dict[
                                                                  'weight_list'][
                                                                  key])

                    step_list.append(
                        {'current_step': uuid.uuid4().hex, 'step_percent': 0,
                         'step_nr': len(step_list) + 1, 'exercise': exercise,
                         'type': 'exercise', 'reps': reps,
                         'rep_unit': rep_unit, 'weight': default_weight,
                         'weight_unit': weight_unit})
                    if request.user.userprofile.timer_active:
                        step_list.append({'current_step': uuid.uuid4().hex,
                                          'step_percent': 0,
                                          'step_nr': len(step_list) + 1,
                                          'type': 'pause',
                                          'time': request.user.userprofile.timer_pause})

        # Supersets need extra work to group the exercises and reps together
        else:
            total_reps = len(set_list_dict['exercise_list'][0]['reps_list'])
            for i in range(0, total_reps):
                for exercise_dict in set_list_dict['exercise_list']:
                    reps = exercise_dict['reps_list'][i]
                    rep_unit = exercise_dict['repetition_units'][i]
                    weight_unit = exercise_dict['weight_units'][i]
                    default_weight = exercise_dict['weight_list'][i]
                    exercise = exercise_dict['obj']

                    step_list.append(
                        {'current_step': uuid.uuid4().hex, 'step_percent': 0,
                         'step_nr': len(step_list) + 1, 'exercise': exercise,
                         'type': 'exercise', 'reps': reps,
                         'rep_unit': rep_unit, 'weight_unit': weight_unit,
                         'weight': last_log.get_last_weight(exercise, reps,
                                                            default_weight)})

                if request.user.userprofile.timer_active:
                    step_list.append(
                        {'current_step': uuid.uuid4().hex, 'step_percent': 0,
                         'step_nr': len(step_list) + 1, 'type': 'pause',
                         'time': 90})

    # Remove the last pause step as it is not needed. If the list is empty,
    # because the user didn't add any repetitions to any exercise, do nothing
    try:
        step_list.pop()
    except IndexError:
        pass

    # Go through the page list and calculate the correct value for step_percent
    for i, s in enumerate(step_list):
        step_list[i]['step_percent'] = (i + 1) * 100.0 / len(step_list)

    # Depending on whether there is already a workout session for today, update
    # the current one or create a new one (this will be the most usual case)
    if WorkoutSession.objects.filter(user=request.user,
                                     date=datetime.date.today()).exists():
        session = WorkoutSession.objects.get(user=request.user,
                                             date=datetime.date.today())
        url = reverse('manager:session:edit', kwargs={'pk': session.pk})
        session_form = WorkoutSessionHiddenFieldsForm(instance=session)
    else:
        today = datetime.date.today()
        url = reverse('manager:session:add',
                      kwargs={'workout_pk': day.training_id,
                              'year': today.year, 'month': today.month,
                              'day': today.day})
        session_form = WorkoutSessionHiddenFieldsForm()

    # Render template
    context['day'] = day
    context['step_list'] = step_list
    context['canonical_day'] = canonical_day
    context['workout'] = day.training
    context['session_form'] = session_form
    context['form_action'] = url
    context['weight_units'] = WeightUnit.objects.all()
    context['repetition_units'] = RepetitionUnit.objects.all()
    return render(request, 'workout/timer.html', context)


def export_json(request, id):
    '''
    export workout data as json
    '''
    workout = get_object_or_404(Workout, pk=id, user=request.user)
    if len(workout.canonical_representation['day_list']) > 0:
        workout_details = {
            'description': workout.canonical_representation['day_list'][0][
                'obj'].description, 'workout_days':
                workout.canonical_representation['day_list'][0][
                    'days_of_week']['text']}

        exercise_set = workout.canonical_representation['day_list'][0][
            'set_list']

        set_list = []
        set_list_dict = {}

        for _set in exercise_set:
            set_list_dict['set_id'] = _set['obj'].id
            set_list_dict['set_order'] = _set['obj'].order
            set_list_dict['sets'] = _set['obj'].sets
            set_list_dict['excerciseday_id'] = _set['obj'].exerciseday_id
            set_list_dict['muscles'] = _set['muscles']

            exercise_list = []
            exercise_list_dict = {}

            for exercise in _set['exercise_list']:
                exercise_list_dict['name_of_exercise'] = exercise['obj'].name
                exercise_list_dict['description'] = exercise[
                    'obj'].description
                exercise_list_dict['category_id'] = exercise[
                    'obj'].category_id
                exercise_list_dict['license_id'] = exercise['obj'].license_id
                exercise_list_dict['settings_list'] = exercise['setting_list']
                repetition_list = [repetition.name for repetition in
                                   exercise['repetition_units']]
                weight_units = [unit.name for unit in
                                exercise['weight_units']]
                exercise_list_dict['weight_units'] = weight_units
                exercise_list_dict['repetition_list'] = repetition_list
                exercise_list_dict['comments'] = exercise['comment_list']
                exercise_list_dict['reps'] = exercise['setting_obj_list'][
                    0].reps
                exercise_list_dict['order'] = exercise['setting_obj_list'][
                    0].order
                exercise_list.append(exercise_list_dict)

            set_list_dict['exercise_list'] = exercise_list
            set_list.append(set_list_dict)

        workout_details['set_list'] = set_list
    else:
        return Response(data={"error": "No data to export"},
                        status=status.HTTP_400_BAD_REQUEST)

    dataset = json.dumps(workout_details, indent=2)

    response = HttpResponse(dataset, content_type='application/json')
    if workout_details.get('description'):
        response[
            'Content-Disposition'] = 'attachment; filename="{}.json"'\
            .format(workout_details['description'])
    else:
        response[
            'Content-Disposition'] = 'attachment; filename="workout-{}.json"'\
            .format(id)
    return response


def import_json(request):
    '''
    import workout data from valid json
    '''
    try:
        content = request.FILES['data']
        data = content.read()
        if type(data) == bytes:
            data = data.decode("utf-8")
            data = ast.literal_eval(data)
            data = json.dumps(data)
        data = json.loads(data)
        days = data['workout_days'].split(', ')
        set_list = data['set_list']
        workout = Workout.objects.create(user=request.user, imported=True)
        workout.comment = data['description']
        workout.save()
        days_of_week = DaysOfWeek.objects.filter(day_of_week__in=days)
        day_save = Day.objects.create(training=workout,
                                      description=data['description'])
        day_save.day.set(days_of_week)

        for _set in set_list:
            no_of_sets = _set['sets']
            exercise_names = [exercise['name_of_exercise'] for exercise in
                              _set['exercise_list']]
            exercises = Exercise.objects.filter(name__in=exercise_names)
            for exercise in exercises:
                exercise_in_list = next(
                    (item for item in _set['exercise_list'] if
                     item['name_of_exercise'] == exercise.name), {})
                reps = exercise_in_list.get('reps', 0)
                order = exercise_in_list.get('order', 1)
                day_set = Set(exerciseday=day_save, sets=no_of_sets,
                              order=_set['set_order'])
                day_set.save()
                day_set.exercises.add(exercise)
                settings = Setting(set=day_set, exercise=exercise, reps=reps,
                                   order=order)
                settings.save()
        messages.success(request, 'Workout imported successfully')
        return HttpResponseRedirect(reverse('manager:workout:overview'))
    except Exception:
        messages.warning(request, 'There was a problem importing your '
                                  'workout. Please confirm JSON is valid')
    return HttpResponseRedirect(reverse('manager:workout:overview'))
