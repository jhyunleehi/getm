print("hello, world!")

marks = [90, 25, 67, 45, 80]
for m in marks:
    #if m < 60:   continue
    print("%d번 학생 축하합니다. %d 합격입니다." % (marks.index(m),m))


marks = [90, 25, 67, 45, 80]
for n in range(len(marks)) :    
    print("%d번 학생 축하합니다. %d 합격입니다." % (n, marks[n]))

marks.sort()
print(marks)



