import csv


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
			prof = line[line.index('<td>')+4:line.index('</td>')]
			i += 3
			line = contents[i]
			course = line[line.index('nk">')+4:line.index('</a>')]
			i += 1
			line = contents[i]
			quarter = line[line.index('<td>')+4:line.index('</td>',line.index('<td>'))] 
			enrolled = line[line.index('ht">')+4:line.index('</td>',line.index('ht">'))]
			i += 1
			line = contents[i]
			evals = line[line.index('ht">')+4:line.index('</span>')]
			i += 4
			line = contents[i]
			courseRec = line[line.index('">')+2:line.index('</span>')]
			i += 4
			line = contents[i]
			profRec = line[line.index('">')+2:line.index('</span>')]
			i += 2
			line = contents[i]
			hours = line[line.index('">')+2:line.index('</span>')]
			i += 3
			line = contents[i]
			expGrade = line[line.index('">')+2:line.index('</span>')]
			i += 3
			line = contents[i]
			givenGrade = line[line.index('">')+2:line.index('</span>')]
			
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

			parsedList.append(courseList)

		i += 1


with open('fullyParsedCapes.csv', 'w') as f:
	write = csv.writer(f)
	write.writerow(fields)
	write.writerows(parsedList)






