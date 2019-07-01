import numpy as np
from csv import *
from xlwt import *
from xlrd import *
from genetic import *
from pandas import *
kechengnum=13
banjinum=5
teachernum=23
course_teacher=[]

classdetailfile=open('课程信息.csv','r')
classdetail=DictReader(classdetailfile)
courseid={}
for item in classdetail:
    courseid[item['课程编号']]=item['课程名称']
    
classdetailfile=open('课程信息.csv','r')    
detail=DictReader(classdetailfile)
courses=[row['课程编号'] for row in detail]

teacherfile=open('教师信息.csv','r')
teacherdetail=DictReader(teacherfile)
teacherid={}
for item in teacherdetail:
    teacherid[item['编号']]=item['姓名']

with open('教师信息.csv') as f:
    r=reader(f)
    data=list(r)
    for kecheng in range(1,kechengnum+1):
        L=[]
        for tid in range(1,teachernum+1):
            if data[tid][kecheng+3]=='1':
                L.append(tid)
        course_teacher.append(L)

s=[]
data=[]
with open('培养方案.csv') as f:
    r=reader(f)
    data=list(r)
    for banji in range(1,banjinum+1):
        for kecheng in range(1,kechengnum+1):
            for i in range(int(data[kecheng][banji])):
                tid=np.random.randint(0, len(course_teacher[kecheng-1]), 1)[0]
                s.append(Schedule(data[kecheng][0], banji,course_teacher[kecheng-1][tid]))

#种群规模popsize，精英个体数elite，进化代数maxiter
ga = GeneticOptimize()
res = ga.evolution(schedules=s, roomRange=5,slotnum=19)

col_labels = ['weekNu5mber','weekStart','weekEnd','Mon','Tue','Wed','Thu','Fri','Sat','Sun']
size=len(col_labels)
w=Workbook(encoding = 'ascii')
style = XFStyle()
style.alignment.wrap = 1
style.alignment.vert = 1
style.alignment.horz = 2
with open('教学日历.csv') as rili:
    #re=reader()
    r = rili.readlines()
    for i in range(len(r)):
        r[i] = r[i].split(',')
    for banji in range(1,banjinum+1):
        sheet=w.add_sheet(data[0][banji])
        for i in range(11):
            sheet.col(i).width=256*13
        for j in range(size):
            sheet.write(0,j,col_labels[j],style)
        for j in range(1,20):
            for k in range(3):
                sheet.write(j,k,r[j][k],style)
        schedule = []
        for k in res:
            if k.classId == banji:
                schedule.append(k)
        for s in schedule:
            weekDay = s.weekDay
            slot = s.slot
            #text = 'course: {} \n class: {} \n room: {} \n teacher: {}'.format(s.courseId, s.classId, s.roomId, s.teacherId)
            
            text = str(courseid[s.courseId])+'\n地点：301-'+ str(100+s.roomId)+'\n教员：'+str(teacherid[str(s.teacherId)])
            sheet.write(slot,weekDay+2,text,style)
                
w.save('各班课程安排.xlsx')



