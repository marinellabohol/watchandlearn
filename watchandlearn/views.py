from django.shortcuts import render,  get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .forms import *
from watchandlearn.models import *
from my_secrets import secrets
import re, requests, json, urllib
from django.template import *
import math

HIGHEST_SCORE = 6

def index(request):
    return render(
        request,
        'watchandlearn/index.html',
        context={},
    )

@login_required
def assessment(request):
  return render(
      request,
      'watchandlearn/assessment.html',
      context={},
  )

@login_required
def recommended(request):
  if request.method == 'POST':
      profile = request.user.profile
      voVal = int(request.POST.get('vocabulary'))
      reVal = int(request.POST.get('reading'))
      wrVal = int(request.POST.get('writing'))
      grVal = int(request.POST.get('grammar'))
      profile.vocabulary = round((voVal/100)*6)
      profile.reading = reVal
      profile.writing = wrVal
      profile.grammar = grVal
      profile.composite = voVal + reVal + wrVal + grVal
      profile.level = math.floor(profile.composite/40)
      profile.experience = 0
      profile.save()
  series_by_topic = []
  topics = Topic.objects.all()
  for topic in topics:
    series_by_topic.append((topic, Series.objects.filter(topic=topic)))
  return render(
      request,
      "watchandlearn/recommended.html",
      context={'topics': topics, 'series_by_topic':series_by_topic}
  )

@login_required
def episodes(request, pk):
  series = get_object_or_404(Series, pk=pk)
  episodes = Episode.objects.all().filter(series__pk=pk)
  return render(request, 'watchandlearn/episodes.html', context={'series': series, "episodes": episodes},)

@login_required
def quiz(request, pk):
  quiz = get_object_or_404(Quiz, pk=pk)
  questions = Question.objects.all().filter(quiz__pk=pk)
  return render( request, 'watchandlearn/quiz.html', context={'quiz': quiz, 'questions': questions},)

def episode_watch(request, pk):
    # convert timestamp string into an integer represenation (seconds)
    def get_seconds(timestamp):
      regex = r"([\d:]+):(\d\d),\d\d\d -->"
      matches = re.finditer(regex, timestamp, re.MULTILINE)
      for match in matches:
        time = match.group(1)
        seconds = match.group(2)
      # time = 26:49:14
      time_list = time.split(":")

      if(len(time_list) == 1):
        return int(time_list[0])
      else:
        total = 0
        for i in range(len(time_list)):
          t = int(time_list[i])
          total += t
          total *= 60
        total+=int(seconds)
        return total

    episode = get_object_or_404(Episode, pk=pk)
    terms = request.session.get('terms')
    for term in terms:
      timestamp = term.get('timestamp')
      word = term.get('word')
      definition = term.get('definition')
      term["timestamp"] = get_seconds(timestamp)
    quiz = episode.quiz
    return render(request, 'watchandlearn/episode_watch.html', context={'episode': episode, 'terms': terms, 'quiz': quiz})



class EpisodeDetailView(LoginRequiredMixin, generic.DetailView):
  model = Episode

  # HELPER METHODS

  # inclusive range function
  def irange(self, x, y):
    return range(x, y+1)

  # turns the content of an srt file into a list of unique words
  def strip_captions(self, caption):
    # remove non-word characters (except for ' )
    caption = re.sub('[\d:,->!"?^]', ' ', caption)

    # remove new lines
    caption = caption.replace('\n', ' ')

    # remove tabs
    caption = caption.replace('\t', ' ')

    caption = caption.replace('\r', ' ')

    # remove extra spaces
    caption = re.sub(' +',' ', caption)

    # to lower case
    caption = caption.lower()

    # split into a set of unique words, delimited by spaces
    return set(caption.split(" "))

  # find timestamp where search_term was said
  def find_timestamp(self, arr, search_term):
    line = 1
    captions = {}
    chunk = []
    timestamp = ''
    i = 0

    while i < len(arr):
      item = arr[i]
      # if it gets to the next line
      if item == str(line):
        i+=1
        timestamp = arr[i]
      elif item == '':
        word = " ". join(chunk)
        captions[timestamp] = word
        chunk = []
        timestamp = ''
        line += 1
      else:
        chunk.append(item)
      i += 1
    word = " ". join(chunk)
    captions[timestamp] = word

    # reverse dict
    captions = {y:x for x,y in captions.items()}

    for line, timestamp in captions.items():
      if search_term in line:
        return timestamp
    return 'Not Found'

  # use OwlAPI to find definitions for search_term
  def find_definition(self, search_term):
    url = 'https://owlbot.info/api/v2/dictionary/' + search_term

    r = requests.get(url).json()
    return r[0]['definition']


  def get_context_data(self, **kwargs):

    # context is a dict of info available in the view
    context = super(EpisodeDetailView, self).get_context_data(**kwargs)

    # list of vocab to eventually put into the context dict
    vocab_list = []

    # selected episode
    episode = context['episode']

    # compare words to user's vocab score
    u = self.request.user.profile
    vocab = u.vocabulary
    print(vocab)
    # create list of unique words
    script_list = self.strip_captions(episode.subtitle)
    for diff_lvl in reversed(self.irange(vocab, HIGHEST_SCORE)):
      if len(vocab_list) >= 5:
        break
      word_list = Word.objects.filter(difficulty__gte=diff_lvl)
      for word_obj in word_list:
        # word_list is a list of word objects, but we just want the word itself
        word = word_obj.name
        if(len(word) < 5):
          continue
        if word in script_list:
          vocab_list.append(word)
          if len(vocab_list) >= 5:
            break

    terms = []
    arr = episode.subtitle.splitlines()
    for search_term in vocab_list:
      timestamp = self.find_timestamp(arr, search_term)
      definition = self.find_definition(search_term)
      terms.append({'timestamp': timestamp, 'word': search_term.capitalize(), 'definition': definition})
    context['terms'] = terms
    self.request.session['terms'] = terms
    return context

@login_required
def lvlup(request):
    profile = request.user.profile

    imgs = ["http://i.imgur.com/e8C02kF.png", "http://i.imgur.com/GoN6UEA.png", "http://i.imgur.com/IGepXLH.png",
    "http://i.imgur.com/7lOka50.png", "http://i.imgur.com/I2GwTfk.png", "http://i.imgur.com/O3j5lQ8.png",
    "http://i.imgur.com/4InrBmC.png", "http://i.imgur.com/87ZzC47.png", "http://i.imgur.com/pIBZwEF.png",
    "http://i.imgur.com/GPHtSUW.png"]

    profile.level += math.floor(profile.experience/1000)
    profile.experience = profile.experience % 1000
    profile.save()

    return render(
        request,
        'watchandlearn/lvlup.html',
        context={'profile': profile, 'imgs': imgs},
      )

@login_required
def feedback(request, pk):
  imgs = ["http://i.imgur.com/e8C02kF.png", "http://i.imgur.com/GoN6UEA.png", "http://i.imgur.com/IGepXLH.png",
    "http://i.imgur.com/7lOka50.png", "http://i.imgur.com/I2GwTfk.png", "http://i.imgur.com/O3j5lQ8.png",
    "http://i.imgur.com/4InrBmC.png", "http://i.imgur.com/87ZzC47.png", "http://i.imgur.com/pIBZwEF.png",
    "http://i.imgur.com/GPHtSUW.png"]
  profile = request.user.profile

  if request.method == 'POST':
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = list(Question.objects.all().filter(quiz__pk=pk))
    answers = []
    answer_text = []
    submissions = []
    qop = []
    curr = []
    xp = 0
    print(request.POST)
    for i in range(len(questions)):
      submitted_answer = request.POST.get('question' + str(i+1))
      submissions.append(submitted_answer)
      question = questions[i]
      answers.append(str(question.answer-1) == submitted_answer)
      if (str(question.answer-1) == submitted_answer):
        answer_text.append("Correct.")
      else:
        print(question.answer)
        if question.answer == 0:
          answer_text.append('Sorry the answer was "' + question.option1 + '".')
        elif question.answer == 1:
          answer_text.append('Sorry the answer was "' + question.option2 + '".')
        elif question.answer == 2:
          answer_text.append('Sorry the answer was "' + question.option3 + '".')
      if (str(question.answer-1) == submitted_answer):
        xp += question.experience
      curr = [question.option1, question.option2, question.option3]

      print(str(i) + " this is the current question list: " + str(curr))
      qop.append(curr)
    profile.experience += xp
    profile.save()
    print("this is the overall list of lists: " + str(qop))
  return render(request, 'watchandlearn/feedback.html', context={'questions': questions, 'answers': answers, "submissions":submissions, 'imgs': imgs, 'profile': profile, 'options': qop, 'answer_text': answer_text})
