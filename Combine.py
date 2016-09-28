import pickle
import json
from os import listdir

def handle_course_real():
  reals = {}
  with(open('./course_dep.p')) as openfile:
    while True:
      try:
        tmp =pickle.load(openfile)
        for c in tmp:
          course_id = c.split(',')[0].split('\'')[1].split('\'')[0]
          real = c.split(',')[3].split('\'')[1].split('\'')[0]
          reals[course_id] = real
      except EOFError:
        break
  return reals

def handle_course_time():
  times = {}
  with(open('./course_dep.p')) as openfile:
    while True:
      try:
        tmp =pickle.load(openfile)
        for c in tmp:
          course_id = c.split(',')[0].split('\'')[1].split('\'')[0]
          time = c.split(',')[5].split('\'')[1].split('\'')[0]
          if '<br>' in time :
            time = time.split('<br>')[0]
          times[course_id] = time 
      except EOFError:
        break
  return times 

def merge_data(reals):
  objects = []
  for f in listdir('./CourseINFO/'):
    with(open('./CourseINFO/'+f)) as openfile:
      while True:
        try:
          tmp =pickle.load(openfile)
          for c in tmp:
            try:
              try:
                course = {'value': c['CourseNO'], 'label': c['CourseTitle'] + ' ' + c['Teacher'].decode('utf8') + '\n' + c['Time'], 'real': reals[c['CourseNO']]}
              except:
                pass
            except:
              # try if course number exist
              try:
                course = {'value': c['CourseNO'], 'label': c['CourseTitle'], 'real': reals[c['CourseNO']] }
              except:
                pass
            objects.append(course)
        except EOFError:
          break

  pickle.dump(objects, open('course.p','wb'))

#reals = handle_course_real()
#merge_data(reals)
times = handle_course_time()
print times
with open('./course_time.json', 'w') as outfile:
    json.dump(times, outfile)
