from random import choice, randrange
from copy import deepcopy

class schedule_class:
	""" The main class for all schedule, containing forms, rooms, subjects, teachers and days """
	def __init__(self, classroom_object, empty = False, given_classes = None):
		self.classroom_object = classroom_object
		if empty: # chcemy pusta klase i taka dostajemy
			self.forms = {}
			self.rooms = {}
			self.subjects = {}
			self.teachers = {}
			self.days = {}
			self.not_correct_penalty = 0
		elif not given_classes: # wywoluje konstruktor losowego planu zajec
			self.forms, self.rooms, self.subjects, self.teachers, self.days, self.not_correct_penalty = create_schedule(classroom_object)
		else: # zwraca klase na podstawie podanych argumentow
			[self.forms, self.rooms, self.subjects, self.teachers, self.days, self.not_correct_penalty] = given_classes
		""" reset the used for each class"""
		form_class.used = []
		room_class.used = []
		subject_class.used = []
		day_class.used = []
		
		
	def count_penalty(self):
		""" Count the penalty value for a class object """
		self.penalty = rate(self.classroom_object, self) + self.not_correct_penalty
		
	def form_print(self):
		vals = self.forms.values()
		vals = sorted(vals, key=str)
		for item in vals:
			item.pretty_print()
			
	def teacher_print(self):
		vals = self.teachers.values()
		vals = sorted(vals, key=str)
		for item in vals:
			item.pretty_print()

def sort(list):	
	""" Very specific sorting, which can get day instances as arguments """
	if list and isinstance(list[0][0], day_class):
		temp_dict = dict(list)		
		new_list = []
		for name in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
			for item in [a[0] for a in list]:
				if str(item) == name:
					new_list.append([item, temp_dict[item]])
					break
		list = new_list
	else:
		list.sort()
	return list

class template:
	""" The template class for all others, containing printing only """
	def pretty_print(self):
		items = self.schedule.items() # metoda items() zmienia dict w kombinacje tuples: {a: b, c: d} => ((a, b), (c,d))
		items = sort(items) # sortuje po kluczach, no chyba, ze sa dni, to sortuje je po kolei
		for k, v in items:
			v.sort() # sortuje elementy wartosci, ktore sa lista
		print self.name + "\n" + "\n".join([str(k) + "\n\t" + "\n\t".join([" - ".join(map(str, i)) for i in v]) for k, v in items]) # ja sam nie wiem, jak to dziala
		
	def __str__(self):
		return self.name # __str__ jest wywolywane przez uzycie str(obiekt), ale tez przez 'print obiekt'

class form_class(template):
	""" The class for school classes """
	used = [] # statyczna lista nazw klas
	def __init__(self):
		if not self.used:
			self.name = 'A'
		else:
			self.name = chr(ord(self.used[-1])+1) # znajdz nastepny znak: ostatni z listy used -> zmien na ascii -> +1 -> zmien na char
		self.used.append(self.name)
		self.schedule = {} # schedule na razie jest pustym slownikiem
	
	""" Set how many lessons of each subject does this form have """
	def assign_subjects(self, subjects):
		self.unassigned_subjects = {}
		for subject in subjects.values(): # values zmienia dict na liste wartosci: {a:b, c:d} => [b, d]
			self.unassigned_subjects[subject] = subject.hours # unassigned_subjects bedzie miec forme typu {'math': 3, 'geo': 2}
			
class room_class(template):
	""" The class for classrooms """
	used = [] 
	def __init__(self):
		if not self.used:
			self.name = '1'
		else:
			self.name = str(int(self.used[-1])+1) # numery klas sa stringami, dlatego '3' -> int('3') = 3 -> 4 -> str(4) = '4'
		self.used.append(self.name)
		self.schedule = {}


class subject_class(template):
	""" The class for subjects """
	used = []
	def __init__(self, (name, hours)): # argumentami sa self (ktory jest zawsze dla metod na obiektach klasy) i tuple (name, hours).
		if name in self.used:
			raise Exception("The subject %s has already been declared" %name) # raise Exception wywoluje wyjatek o podanym komunikacie
		else:
			self.name = name
			self.used.append(self.name)
		self.teachers_assigned = [] # na razie pusta lista nauczycieli przypisanych do tego przedmiotu
		self.hours = hours # ile godzin tego przedmiotu tygodniowo ma miec klasa
		self.schedule = {}


class teacher_class(template):
	""" The class for teachers """
	def __init__(self, name, subject):
		self.name = name
		self.subject = subject
		self.subject.teachers_assigned.append(self) # od razu przypisz siebie do listy nauczycieli twojego przedmiotu
		self.schedule = {}

	
class day_class(template):
	""" The class for each day instance """
	used = []
	def __init__(self, classroom_object, name):
		if name in self.used:
			raise Exception("The day %s has already been declared" %name)
		else:
			self.name = name
			self.used.append(self.name)
			self.cells = classroom_object.daycells
			self.schedule = {}


def check_all_forms(forms):
	""" Check if there is any unassigned lesson in any class """
	for form in forms.values():
		for item in form.unassigned_subjects.values():
			if item:
				return True
	return False	

def create_schedule(classroom_object):
	""" Creates a random, correct schedule """
	
	""" Initialization """
	forms = {}
	for _ in range(classroom_object.forms_range): # Petla mowiaca tylko, ile razy ma byc uzyta jej zawartosc
		tmp = form_class() # tworzy tymczasowa instacje klasy
		forms[tmp.name] = tmp # i przypisuje ja do forms po nazwie
	
	rooms = {} # jak wyzej
	for _ in range(classroom_object.rooms_range):
		tmp = room_class()
		rooms[tmp.name] = tmp

	subjects = {}
	for pair in classroom_object.subject_list: # tutaj iterujemy po liscie tupli i dla wszystkich tworzymy instacje subject_class (dlatego tam w argumentach tez jest tuple)
		tmp = subject_class(pair)
		subjects[tmp.name] = tmp

	for f in forms.values(): # przypisuje zajecia do klas
		f.assign_subjects(subjects)
	
	teachers = {}
	for pair in classroom_object.teacher_list:
		tmp = teacher_class(pair[0], subjects[pair[1]]) # wywoluje sie dla pair[0] = imie nauczyciela i subjects[pair[1]], czyli subjects[przdmiot]
		teachers[tmp.name] = tmp
	
	days = {}
	for name in classroom_object.day_list:
		days[name] = day_class(classroom_object, name)
		
	penalty = 0
	
	unchanged = 0 # ilosc iteracji, przy ktorych nie zaszly zmiany
	while check_all_forms(forms): # tak dlugo, az istnieje nieprzypisana lekcja
		skipped = 0 # ilosc iteracji w ponizszym forze, przy ktorych nie zaszly zmiany
		iters = 0 # ilosc iteracji w ponizszym forze

		for day in days.values():
			for cell in day.cells:
				iters += 1
				# ten framgent mozna zoptymalizowac - po co ma szukac wsrod klas, ktore maja juz wszystkie zajecia?
				temp_form = choice(forms.values()) # wybierz losowa klase
				temp_room = choice(rooms.values()) # wybierz losowa sale
				temp_subject = choice(subjects.values()) # wybierz losowy przedmiot
				available_teachers = []
				
				""" make sure no teacher has two classes at same time """
				for t in temp_subject.teachers_assigned:
					if day in t.schedule.keys() and any(cell in s for s in t.schedule[day]):
						continue
					else:
						available_teachers.append(t)
				if not available_teachers:
					skipped += 1
					continue
				else:
					temp_teacher = choice(available_teachers)
					
				""" make sure no class has two lessons at same time """
				if day in temp_form.schedule.keys() and any(cell in s for s in temp_form.schedule[day]):
					skipped += 1
					continue
					
				""" make sure no classroom has two lessons at same time """
				if day in temp_room.schedule.keys() and any(cell in s for s in temp_room.schedule[day]):
					skipped += 1
					continue
					
				""" make sure the class does not have enough subjects """
				if not temp_form.unassigned_subjects[temp_subject]:
					skipped += 1
					continue
				
				""" assign the day table """
				if cell in day.schedule.keys():
					day.schedule[cell].append([temp_form, temp_room, temp_teacher])
				else:
					day.schedule[cell] = [[temp_form, temp_room, temp_teacher],]
					
				""" assign the class table """
				if day in temp_form.schedule.keys():
					temp_form.schedule[day].append([cell, temp_room, temp_subject, temp_teacher])
				else:
					temp_form.schedule[day] = [[cell, temp_room, temp_subject, temp_teacher],]
				temp_form.unassigned_subjects[temp_subject] -= 1
					
				""" assign the teacher table """
				if day in temp_teacher.schedule.keys():
					temp_teacher.schedule[day].append([cell, temp_room, temp_form])
				else:
					temp_teacher.schedule[day] = [[cell, temp_room, temp_form],] 
					
				""" assign the room table """
				if day in temp_room.schedule.keys():
					temp_room.schedule[day].append([cell, temp_form, temp_subject, temp_teacher])
				else:
					temp_room.schedule[day] = [[cell, temp_form, temp_subject, temp_teacher],] 
					
				""" assign the subject table """
				if day in temp_subject.schedule.keys():
					temp_subject.schedule[day].append([cell, temp_form, temp_room, temp_teacher])
				else:
					temp_subject.schedule[day] = [[cell, temp_form, temp_room, temp_teacher],] 
					
		if skipped == iters: # nie zaszla zadna zmiana
			unchanged += 1
			if unchanged >= 100: # jezeli przez 100 iteracji nie zajdzie zmiana, to nie zajdzie juz nigdy (sprawdzane tylko eksperymentalnie)
				penalty = 20
				break # zwraca niepelny plan zajec (ale zwraca)
					
	return [forms, rooms, subjects, teachers, days, penalty]

def auto_complete(classroom_object, schedules):
	""" Fills up randomly given schedules by looking at their pre-built skeleton (containing day: class and teacher collocations) """
	schedule_return = [] # to zwrocimy na koncu
	for schedule in schedules:
		for subject in schedule.subjects.values():
			if subject.schedule:
				for vals in subject.schedule.values():
					for item in vals:
						if len(item) != 4:
							continue
						# tutaj niszczymy godzine i sale zostawiajac tylko klase i nauczyciela
						del item[0] # z [godzina, klasa, sala, nauczyciel] usuwamy element 0, wiec zostaje [klasa, sala, nauczyciel]
						del item[1] # z [klasa, sala, nauczyciel] usuwamy element 1, wiec zostaje [klasa, nauczyciel]
					
		# zeruje used we wszystkich klasach (na wszelki wypadek)
		form_class.used = []
		room_class.used = []
		subject_class.used = []
		day_class.used = []
	
		""" Initialization """ # dokladnie tak samo, jak w create_schedule
		forms = {}
		for _ in range(classroom_object.forms_range): 
			tmp = form_class() 
			forms[tmp.name] = tmp 
		
		rooms = {} # jak wyzej
		for _ in range(classroom_object.rooms_range):
			tmp = room_class()
			rooms[tmp.name] = tmp
			
		subjects = {}
		for pair in classroom_object.subject_list: 
			tmp = subject_class(pair)
			subjects[tmp.name] = tmp
			
		for f in forms.values():
			f.assign_subjects(subjects)
		
		teachers = {}
		for pair in classroom_object.teacher_list:
			tmp = teacher_class(pair[0], subjects[pair[1]]) # wywoluje sie dla pair[0] = imie nauczyciela i subjects[pair[1]], czyli subjects[przdmiot]
			teachers[tmp.name] = tmp
		
		days = {}
		for name in classroom_object.day_list:
			days[name] = day_class(classroom_object, name)
			
		unchanged = 0 # ilosc iteracji, przy ktorych nie zaszly zmiany
		penalty = 0
		while check_all_forms(forms): # tak dlugo, az istnieje nieprzypisana lekcja	
			unchanged += 1
			if unchanged >= 100: # jezeli przez 100 iteracji wciaz sie nie uda, to mozemy zwrocic niepelny plan
				penalty += 1
				break # zwraca niepelny plan zajec (ale zwraca)
			
			""" Fixed choices """
			if not any(a for a in schedule.subjects.values() if a.schedule):
				# inny sposob wyjscia z petli
				break # to nie powinno sie nigdy wywolywac, a jednak sie wywoluje i to czesto... w kazdym razie jesli nie zadziala, to nic sie nie dzieje
			
			parent_subject = choice([a for a in schedule.subjects.values() if a.schedule])
			temp_subject = subjects[str(parent_subject)]
			if not parent_subject.schedule.items():
				print schedule.subjects.values()
			tuple = choice(parent_subject.schedule.items())
			day = days[str(tuple[0])]
			temp = tuple[1]
			tuple = choice(temp)
			if len(tuple) != 2:
				continue
			temp_form = forms[str(tuple[0])]
			temp_teacher = teachers[str(tuple[1])]
			cell = choice(day.cells)
			temp_room = rooms[str(choice(rooms.values()))]

			""" make sure this teacher doesn't have two classes at same time """
			if day in temp_teacher.schedule.keys() and any(cell in s for s in temp_teacher.schedule[day]):
				continue
						
			""" make sure no class has two lessons at same time """
			if day in temp_form.schedule.keys() and any(cell in s for s in temp_form.schedule[day]):
				continue
						
			""" make sure no classroom has two lessons at same time """
			if day in temp_room.schedule.keys() and any(cell in s for s in temp_room.schedule[day]):
				continue
						
			""" make sure the class does not have enough subjects """
			if not temp_form.unassigned_subjects[temp_subject]:
				print temp_form.unassigned_subjects[temp_subject]
				continue

			""" assign the day table """
			if cell in day.schedule.keys():
				day.schedule[cell].append([temp_form, temp_room, temp_teacher])
			else:
				day.schedule[cell] = [[temp_form, temp_room, temp_teacher],]
						
			""" assign the class table """
			if day in temp_form.schedule.keys():
				temp_form.schedule[day].append([cell, temp_room, temp_subject, temp_teacher])
			else:
				temp_form.schedule[day] = [[cell, temp_room, temp_subject, temp_teacher],]
			temp_form.unassigned_subjects[temp_subject] -= 1
						
			""" assign the teacher table """
			if day in temp_teacher.schedule.keys():
				temp_teacher.schedule[day].append([cell, temp_room, temp_form])
			else:
				temp_teacher.schedule[day] = [[cell, temp_room, temp_form],] 
						
			""" assign the room table """
			if day in temp_room.schedule.keys():
				temp_room.schedule[day].append([cell, temp_form, temp_subject, temp_teacher])
			else:
				temp_room.schedule[day] = [[cell, temp_form, temp_subject, temp_teacher],] 
						
			""" assign the subject table """
			if day in temp_subject.schedule.keys():
				temp_subject.schedule[day].append([cell, temp_form, temp_room, temp_teacher])
			else:
				temp_subject.schedule[day] = [[cell, temp_form, temp_room, temp_teacher],] 
			
			""" if this cell is assigned, delete it from parent_subject """
			for key, value in parent_subject.schedule.items():
				if str(key) == str(day):
					for tuple in value:
						if str(tuple[0]) == str(temp_form) and str(tuple[1]) == str(temp_teacher):
							value.remove(tuple)
							unchanged -= 1
							break
					if not value:
						del parent_subject.schedule[key]
			if not parent_subject.schedule:
				del schedule.subjects[str(parent_subject)]
		
		schedule_return.append( [forms, rooms, subjects, teachers, days, penalty] )
	return schedule_return

def crossing(classroom_object, pair_of_schedules):
	new_schedule = []
	new_schedule.append(schedule_class(classroom_object, empty = True))
	new_schedule.append(schedule_class(classroom_object, empty = True))
	for subject in pair_of_schedules[0].subjects.keys():
		i = randrange(0,2)
		try:
			new_schedule[0].subjects[subject] = pair_of_schedules[i].subjects[subject]
			new_schedule[1].subjects[subject] = pair_of_schedules[1-i].subjects[subject]
		except KeyError:
			pass
	return new_schedule

def rate(classroom_object, schedule):
	penalty = 0
	for item, ratio in [(schedule.forms, classroom_object.penalty_for_forms), (schedule.teachers, classroom_object.penalty_for_teachers)]: #ratio means, that classes are more important than teachers
		for i in item.values():
			sum_of_hours = 0
			for day, content in i.schedule.items():
				cells = []
				for cell in content:
					sum_of_hours += 1
					cells.append(classroom_object.daycells.index(cell[0]))
				cells.sort()
				if len(cells) == 1:
					penalty += classroom_object.penalty_for_short_days * ratio
				else:
					for i in range(len(cells)-1):
						penalty += (cells[i+1] - cells[i] - 1) * ratio
						

						
	return penalty

def find_best_fitting(schedules):
	hash_table = [0]
	max_penalty = 0
	for item in schedules:
		if item.penalty > max_penalty:
			max_penalty = item.penalty
	for item in schedules:
		hash_table.append(max_penalty - item.penalty + hash_table[-1])
		
	best = []
	for _ in range(2):
		try:
			rand = randrange(0, hash_table[-1])
		except ValueError:
			rand = randrange(0, len(hash_table))
			
		for i in range(len(hash_table)-1):
			if rand < hash_table[i]:
				break
		si = schedules[i]
		#sc = schedule_class(given_classes = (si.forms, si.rooms, si.subjects, si.teachers, si.days, si.not_correct_penalty))
		#sc.count_penalty()
		#sc2 = deepcopy(si)
		#best.append(sc)
		best.append(deepcopy(si))

	return best

def find_best(classroom_object, schedules):
	top1 = None
	top2 = None
	top1_penalty = 10000
	top2_penalty = 10000
	
	for item in schedules:
		if top1 == 10000:
			top1 = item
			top1_penalty = item.penalty
		elif item.penalty < top1_penalty:
			top2 = top1
			top2_penalty = top1_penalty
			top1 = item
			top1_penalty = item.penalty
		elif item.penalty < top2_penalty:
			top2 = item
			top2_penalty = item.penalty
	
	top_1_copy = schedule_class(classroom_object, given_classes = (top1.forms, top1.rooms, top1.subjects, top1.teachers, top1.days, top1.not_correct_penalty))
	top_2_copy = schedule_class(classroom_object, given_classes = (top2.forms, top2.rooms, top2.subjects, top2.teachers, top2.days, top2.not_correct_penalty))
	top_1_copy.count_penalty()
	top_2_copy.count_penalty()
	return [top_1_copy, top_2_copy]
	#return [deepcopy(top1), deepcopy(top2)]

def find_worst(schedules):
	top1 = None
	top2 = None
	top1_penalty = 0
	top2_penalty = 0
	
	for item in schedules:
		if not top1:
			top1 = item
			top1_penalty = item.penalty
		elif item.penalty > top1_penalty:
			top2 = top1
			top2_penalty = top1_penalty
			top1 = item
			top1_penalty = item.penalty
		elif item.penalty > top2_penalty:
			top2 = item
			top2_penalty = item.penalty
	
	return [top1, top2]


class classroom:
	""" Init parameters """
	forms_range = 7
	rooms_range = 6
	subject_list = (('math', 5), ('eng', 5), ('chem', 1), ('geo', 2), ('phis', 2), ('PE', 2), ('art', 1), ('hist', 2))
	all_hours = sum(a[1] for a in subject_list)
	teacher_list = (("Ann", "math"), ("Bert", "math"), ("Chris", "math"), ("Daniel", "eng"), ("Eustache", "eng"), ("Filip", "eng"), 
				("Goudy", "eng"), ("Hubert", "chem"), ("Ivone", "geo"), ("Jonas", "phis"), ("Kevin", "PE"), ("Louis", "art"),
				("Monica", "hist"))
	day_list = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
	daycells = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]

	def __init__(self, genom_length = None, iterations = None, penalty_for_forms = None, penalty_for_teachers = None, penalty_for_short_days = None):
		self.genom_length = 10 #Number of schedules
		self.iterations = 10
		
		self.penalty_for_forms = 5
		self.penalty_for_teachers = 1
		self.penalty_for_short_days = 1
		
	def count(self):
		schedules = []		
		for _ in range(self.genom_length):
			sc = schedule_class(self)
			sc.count_penalty()
			schedules.append(sc)
		
		
		ok = 0
		not_ok = 0
		c = None
		d = None
		for i in range(self.iterations):
			to_crossing = find_best_fitting(schedules) #Much better then find_best
			
			penalties = [a.penalty for a in schedules]
			penalties.sort()
			#yield "All genom penalties sorted: \n" + str(penalties)
			
			f = find_best(self, schedules)[0]
			not_correct_penalty = f.not_correct_penalty
			f = f.penalty
			#if c and d:
			#	if f == c or f == d:
			#		if not_correct_penalty:
			#			print "This schedule is not all appropriate"
			#		print f
						
			""" Crossing of two schedules """	
			temp_schedules = auto_complete(self, crossing(self, to_crossing))
			a, b = to_crossing[0].penalty, to_crossing[1].penalty
			e = []
			for item in temp_schedules:
				sc = schedule_class(self, empty = False, given_classes = item)
				sc.count_penalty()
				schedules.append(sc)
				e.append(sc.penalty)
			c, d = e
			
			for item in find_worst(schedules):
				if item in schedules:
					schedules.remove(item)
			
			if c < a or c < b or d < a or d < b:
				ok += 1
			else:
				not_ok += 1
		
			del temp_schedules
			
		#print "OK: %s" %ok
		#print "NOT OK: %s" %not_ok
			
		#print "Finished"
		the_best = find_best(self, schedules)[0]
		#print "The best penalty: ", the_best.penalty
		#the_best.form_print()
		return the_best

		

		
#for tup in [(5, 1, 1)]:#, (1, 0, 1), (1, 1, 0), (1, 1, 1), (5, 1, 0), (5, 1, 1)]:
#
#	penalty_for_forms = tup[0]
#	penalty_for_teachers = tup[1]
#	penalty_for_short_days = tup[2]
#	
#	print "Penalty for: forms = %s, teachers = %s, penalty_for_short_days = %s " %(penalty_for_forms, penalty_for_teachers, penalty_for_short_days)
#
#	get_it_started(forms_range, rooms_range, subject_list, all_hours, teacher_list, day_list, daycells, genom_length, iterations)
	
	



#the_best.teacher_print()

#for item in to_crossing[0].teachers.values(): # przykladowy sposob wyswietlania (wszyscy nauczyciele we wszystkich planach)
#	item.pretty_print()

# for item in schdules[0].subjects['math']: - tylko matematyka dla pierwszego podzialu (z 3)
# for item in schdules[2].rooms['3']: - tylko trzecia sala dla ostatniego podzialu

##for s in schedules:
##	s.forms["A"].pretty_print()
##	print "-"*40

##print "="*40	