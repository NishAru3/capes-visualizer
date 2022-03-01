import csv


filepath = 'allData.txt'

parsedList = []
fields = ["Prof","Course","Quarter","Enrolled","Evals Made","Course Rec %","Prof Rec %", "Hours/Week", "Expected Grade", "Given Grade"]
    
class Course(object):
    professor = []
    course = ""
    enrolled = []
    course_rec_percent = []
    prof_rec_percent = []
    studying = []
    given_grade = []


    # def compare_other_course(self, other_course):
    #     if(self.course[1:10] == other_course.course[1:10]):
    #         if(self.professor == other_course.professor):
    #             return 0
    #         return 1
    #     return -1

    def get_data_string(self):
        data_str = ""
        for i in range(0, len(self.professor)):
            data_str = data_str + self.professor[i] + " " + self.enrolled[i] + " " + self.course_rec_percent[i] + " " + self.prof_rec_percent[i] + " " + self.studying[i] + " " + self.given_grade[i] + "\n"
        return data_str


course_dict = {}

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

            if(course[1:10] not in course_dict):
                new_course = Course()
                new_course.professor.append(prof)
                new_course.course = course
                new_course.enrolled.append(enrolled)
                new_course.course_rec_percent.append(courseRec)
                new_course.prof_rec_percent.append(profRec)
                new_course.studying.append(hours)
                new_course.given_grade.append(givenGrade)

                course_dict[course[1:10]] = new_course
            else:
                old_course = course_dict[course[1:10]]
                if(prof in old_course.professor):
                    prof_ind = old_course.professor.index(prof)
                    prof_ind += 1
                    old_course.professor.insert(prof_ind, prof)
                    old_course.enrolled.insert(prof_ind,enrolled)
                    old_course.course_rec_percent.insert(prof_ind,courseRec)
                    old_course.prof_rec_percent.insert(prof_ind,profRec)
                    old_course.studying.insert(prof_ind,hours)
                    old_course.given_grade.insert(prof_ind,givenGrade)
                else:
                    old_course.professor.append(prof)
                    old_course.enrolled.append(enrolled)
                    old_course.course_rec_percent.append(courseRec)
                    old_course.prof_rec_percent.append(profRec)
                    old_course.studying.append(hours)
                    old_course.given_grade.append(givenGrade)


            

            parsedList.append(courseList)

        i += 1


with open('fullyParsedCapes.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(parsedList)

arr = []

for i in course_dict:
    arr.append([str(course_dict[i].course)])
    # print(course_dict[i].course)
    # print(course_dict[i].get_data_string())

print(len(course_dict))



with open('newCSV.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(["The Only Column"])
    write.writerows(arr)



