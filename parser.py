import csv
import xlsxwriter
import pandas as pd
# from ethnicolr import pred_wiki_name
import gender_guesser.detector as gender


# Dictionary Course Object
class Course:
	def __init__(self):
		self.courseCode = ""
		self.courseName = []
		self.professor = []
		self.quarter = []
		self.enrolled = []
		self.course_rec_percent = []
		self.prof_rec_percent = []
		self.studying = []
		self.given_grade = []

	# def compare_other_course(self, other_course):
	#     if(self.course[1:10] == other_course.course[1:10]):
	#         if(self.professor == other_course.professor):
	#             return 0
	#         return 1
	#     return -1

	def get_data_string(self):
		data_str = ""
		for i in range(0, len(self.professor)):
			data_str = data_str + self.courseName[i] + " " +self.professor[i] + " " + self.quarter[i] + " " + self.enrolled[i] + " " + self.course_rec_percent[i] + " " + self.prof_rec_percent[i] + " " + self.studying[i] + " " + self.given_grade[i] + "\n"
		return data_str

# Dictionary Setup
course_dict = {}

qOrder = ['WI','SP', 'SU','S1','S2', 'S3','FA']

gOrder = ['A+','A ','A-','B+', 'B ', 'B-', 'C+','C ','C-','D+','D ','D-','N/']

def quarterIsGreater(one, two):
	y1 = int(one[2:])
	y2 = int(two[2:])
	q1 = qOrder.index(one[:2])
	q2 = qOrder.index(two[:2])

	if(y2>y1):
		return 1
	elif(y2<y1):
		return -1
	elif(q2>q1):
		return 1
	elif(q2<q1):
		return -1
	else:
		return 0

def gradeCompare(one, two):
	return gOrder.index(one[:2])-gOrder.index(two[:2])

names = []


d = gender.Detector()
# CAPES Parser
filepath = 'allData.txt'
parsedList = []
fields = ["Prof","Course","Quarter","Enrolled","Evals Made","Course Rec %","Prof Rec %", "Hours/Week", "Expected Grade", "Given Grade"]

with open(filepath) as f:
	contents = f.readlines()
	
	# find a tag, beginning of a class
	# starts with teacher, then
	# prof,course,quarter,enrolled,evals made,rec class, rec prof,hrs/wk,grade exp, grade given
	
	i = 0
	while (i<len(contents)):
		if "<tr class" in contents[i]:
			courseList = []
			i += 1
			line = contents[i]
			prof = line[line.index('<td>')+4:line.index('</td>')].strip()
			i += 3
			line = contents[i]
			course = line[line.index('nk">')+4:line.index('</a>')].replace('&amp;', '&').strip()
			i += 1
			line = contents[i]
			quarter = line[line.index('<td>')+4:line.index('</td>',line.index('<td>'))].strip()
			enrolled = line[line.index('ht">')+4:line.index('</td>',line.index('ht">'))].strip()
			i += 1
			line = contents[i]
			evals = line[line.index('ht">')+4:line.index('</span>')].strip()
			i += 4
			line = contents[i]
			courseRec = line[line.index('">')+2:line.index('</span>')].strip()
			i += 4
			line = contents[i]
			profRec = line[line.index('">')+2:line.index('</span>')].strip()
			i += 2
			line = contents[i]
			hours = line[line.index('">')+2:line.index('</span>')].strip()
			i += 3
			line = contents[i]
			expGrade = line[line.index('">')+2:line.index('</span>')].strip()
			i += 3
			line = contents[i]
			givenGrade = line[line.index('">')+2:line.index('</span>')].strip()
			
			# prof_split = prof.split(" ")
			# print(prof_split[1])
			# print(d.get_gender(prof_split[1]))
			courseList.append(prof)
			courseList.append(course)
			courseList.append(quarter)
			courseList.append(enrolled)
			courseList.append(evals)
			courseList.append(courseRec)
			courseList.append(profRec)
			courseList.append(hours)
			courseList.append(expGrade)
			courseList.append(givenGrade)
			# firstN = prof[prof.index(',')+1:]
			# lastN = prof[:prof.index(',')]
			# if([firstN,lastN] not in names):
			# 	names.append([firstN,lastN])

			courseCode = course[0:course.index('-')].strip()

			if(courseCode not in course_dict):
				new_course = Course()
				new_course.courseCode = courseCode
				new_course.courseName.append(course)
				new_course.professor.append(prof)
				new_course.quarter.append(quarter)
				new_course.enrolled.append(enrolled)
				new_course.course_rec_percent.append(courseRec)
				new_course.prof_rec_percent.append(profRec)
				new_course.studying.append(hours)
				new_course.given_grade.append(givenGrade)

				course_dict[courseCode] = new_course
			else:
				old_course = course_dict[courseCode]
				if(prof in old_course.professor):
					prof_ind = old_course.professor.index(prof)
					 
					# WI21,SP21,S121,S221,FA21 --> chronological
					# while(prof_ind<old_course.professor.index(prof)+old_course.professor.count(prof) and quarterIsGreater(old_course.quarter[prof_ind],quarter)<0):
					# 	prof_ind = prof_ind + 1
					# Sort by grade
					while(prof_ind<old_course.professor.index(prof)+old_course.professor.count(prof) and gradeCompare(old_course.given_grade[prof_ind],givenGrade)<0):
						prof_ind = prof_ind + 1
					old_course.courseName.insert(prof_ind, course)
					old_course.professor.insert(prof_ind, prof)
					old_course.quarter.insert(prof_ind, quarter)
					old_course.enrolled.insert(prof_ind,enrolled)
					old_course.course_rec_percent.insert(prof_ind,courseRec)
					old_course.prof_rec_percent.insert(prof_ind,profRec)
					old_course.studying.insert(prof_ind,hours)
					old_course.given_grade.insert(prof_ind,givenGrade)
				else:
					old_course.courseName.append(course)
					old_course.professor.append(prof)
					old_course.quarter.append(quarter)
					old_course.enrolled.append(enrolled)
					old_course.course_rec_percent.append(courseRec)
					old_course.prof_rec_percent.append(profRec)
					old_course.studying.append(hours)
					old_course.given_grade.append(givenGrade)
			parsedList.append(courseList)
		i += 1

# Printing
# with open('fullyParsedCapes.csv', 'w') as f:
# 	write = csv.writer(f)
# 	write.writerow(fields)
# 	write.writerows(parsedList)

arr = []
arrFields = ['Course Code', 'Professor', 'Gender', 'Quarter','Enrolled Count', 'Course Rec %', 'Prof Rec %', 'Hours/Week', 'Grade']

df = pd.DataFrame(names, columns = ['first', 'last'])
# 
# odf = pred_wiki_name(df, 'last', 'first')


genderCalc = {
	'male': {
		'A+': 0,
		'A ': 0,
		'A-': 0,
		'B+': 0,
		'B ': 0,
		'B-': 0,
		'C+': 0,
		'C ': 0,
		'C-': 0,
		'D+': 0,
		'D ': 0,
		'D-': 0,
		'N/': 0,
		'sum': 0
	},
	'female': {
		'A+': 0,
		'A ': 0,
		'A-': 0,
		'B+': 0,
		'B ': 0,
		'B-': 0,
		'C+': 0,
		'C ': 0,
		'C-': 0,
		'D+': 0,
		'D ': 0,
		'D-': 0,
		'N/': 0,
		'sum': 0
	}
}

departmentDict = {}

for i in course_dict:
	c = 0
	dep = course_dict[i].courseCode.split(" ")[0]
	if(dep not in departmentDict):
		departmentDict[dep] = {
			'male': {
				'A+': 0,
				'A ': 0,
				'A-': 0,
				'B+': 0,
				'B ': 0,
				'B-': 0,
				'C+': 0,
				'C ': 0,
				'C-': 0,
				'D+': 0,
				'D ': 0,
				'D-': 0,
				'N/': 0,
				'sum': 0
			},
			'female': {
				'A+': 0,
				'A ': 0,
				'A-': 0,
				'B+': 0,
				'B ': 0,
				'B-': 0,
				'C+': 0,
				'C ': 0,
				'C-': 0,
				'D+': 0,
				'D ': 0,
				'D-': 0,
				'N/': 0,
				'sum': 0
			}
		}
	for j in course_dict[i].professor:
		arrY = []
		if (c ==  0):
			arrY.append(course_dict[i].courseCode)
		else:
			arrY.append("")
		arrY.append(j)
		prof_split = j.split(" ")
		profIndex = len(prof_split)
		if (profIndex == 1):
			profIndex = 0
		else:
			profIndex = 1
		gender = d.get_gender(prof_split[profIndex])
		arrY.append(gender)

		if ('female' in gender):
			departmentDict[dep]['female'][course_dict[i].given_grade[c][:2]] += 1
			departmentDict[dep]['female']['sum'] += 1
		elif('male' in gender):
			departmentDict[dep]['male'][course_dict[i].given_grade[c][:2]] += 1
			departmentDict[dep]['male']['sum'] += 1

		# firstN = j[j.index(',')+1:]
		# lastN = j[:j.index(',')]
		# arrY.append(odf.at(names.index([firstN,lastN]),'race'))
		arrY.append(course_dict[i].quarter[c])
		arrY.append(course_dict[i].enrolled[c])
		arrY.append(course_dict[i].course_rec_percent[c])
		arrY.append(course_dict[i].prof_rec_percent[c])
		arrY.append(course_dict[i].studying[c])
		arrY.append(course_dict[i].given_grade[c])
		arr.append(arrY)
		c += 1
	if(departmentDict[dep]['male']['sum'] == 0):
		departmentDict[dep]['male']['sum'] = 1

	if(departmentDict[dep]['female']['sum'] == 0):
		departmentDict[dep]['female']['sum'] = 1 
		

# print(genderCalc)

# for dep in departmentDict:
# 	if(departmentDict[dep]['male']['sum'] == 0 or departmentDict[dep]['female']['sum'] == 0):
# 		print(dep)
# 		print(departmentDict[dep]['male']['sum'])
# 		print(departmentDict[dep]['female']['sum'])

for dep in departmentDict:
	counter = 0
	weightSumMale = 0
	weightSumFemale = 0
	for i in departmentDict[dep]['male']:
		if counter < 12:
			weightSumMale += int(counter*departmentDict[dep]['male'][i])
		print(i,departmentDict[dep]['male'][i])
		counter += 1

	counter = 0
	for i in departmentDict[dep]['female']:
		if counter < 12:
			weightSumFemale += int(counter*departmentDict[dep]['female'][i])
		print(i,departmentDict[dep]['female'][i])
		counter += 1


	print(departmentDict[dep]['male']['sum'])
	print(departmentDict[dep]['female']['sum'])
	aveMale = weightSumMale/departmentDict[dep]['male']['sum']
	aveFemale = weightSumFemale/departmentDict[dep]['female']['sum']
	print(dep)
	print('male: ',gOrder[int(aveMale)])
	print('female: ',gOrder[int(aveFemale)])


# with open('formattedParsed.csv', 'w') as f:
# 	write = csv.writer(f)
# 	write.writerow(arrFields)
# 	write.writerows(arr)

# Excel Setup
workbook = xlsxwriter.Workbook('formattedColoredData.xlsx')
worksheet = workbook.add_worksheet()
header = workbook.add_format({'bold': True, 'align': 'center', 'size': 18, 'bg_color':'#A6A6A6'})
colZero = workbook.add_format({'bg_color':'#BFBFBF'})
light1 = workbook.add_format({'bg_color':'#BFD9C0'})
dark1 = workbook.add_format({'bg_color':'#9AB59B'})
light2 = workbook.add_format({'bg_color':'#F7D5A8'})
dark2 = workbook.add_format({'bg_color':'#D1B38E'})
colArr = [[light1,dark1],[light2,dark2]]
gradientDict = {
	"A+": workbook.add_format({'bg_color':'#fa6e7b'}),
	"A ": workbook.add_format({'bg_color':'#e0648a'}),
	"A-": workbook.add_format({'bg_color':'#d0618f'}),
	"B+": workbook.add_format({'bg_color':'#ae5d94'}),
	"B ": workbook.add_format({'bg_color':'#9c5c94'}),
	"B-": workbook.add_format({'bg_color':'#8a5a92'}),
	"C+": workbook.add_format({'bg_color':'#675688'}),
	"C ": workbook.add_format({'bg_color':'#575381'}),
	"C-": workbook.add_format({'bg_color':'#484f78'}),
	"D+": workbook.add_format({'bg_color':'#3c4b6e'}),
	"D ": workbook.add_format({'bg_color':'#324663'}),
	"D-": workbook.add_format({'bg_color':'#2a4158'}),
	"N/": workbook.add_format({'bg_color':'#dda646'}),

}
# 5 diff colors 
# tan
#E5C59C
#BFA482
# blue
##a6e5ff
#81bcd4
# pink
#FFDDDF
##F1C0B9
# green
#BFD9C0
##B4D4B5
# purple
#CABFD9
#9D8EBF

# sum of everything up to digit results in 

# COLORS:
# Red #FF5455
# F24F73
# F363AB
# D95EC8
# BF58E6

# a+
# a
# a-
# b+
# b
# b-
# c+
# c
# c-
# d
# f

# purple


# Excel Input
row = 0
col = 0
for title in arrFields:
	worksheet.set_column(col, col, len(title)*2)
	worksheet.write(row, col,title, header)
	col += 1

col = 0
row = 1
perCourse = ""
perProf = ""
colorIter1 = 0
colorIter2 = 0
for eachClass in arr:
	perCourse = eachClass[0]
	if(perCourse != ""):
		colorIter1 = (colorIter1+1)%2
	
	if(perProf != eachClass[1]):
		colorIter2 = (colorIter2+1)%2
	perProf = eachClass[1]

	for eachItem in eachClass:
		if(col == 8):
			worksheet.write(row, col, eachItem, gradientDict[eachItem[:2]])
		else:
			worksheet.write(row, col, eachItem, colArr[colorIter1][colorIter2])
		col += 1
	row += 1
	col = 0

# Excel Close
workbook.close()


