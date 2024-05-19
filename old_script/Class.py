def classificate(dict1,xx,b,c,ww):
    maxnumber=0
    clas=[]
    for i in range(len(xx)):
        clas.append([])
    where=[[],[],[],[],[],[],[],[],[],[]]
    numbers=['0','2','3','4','5','6','7','8','9']
    list0=dict1['words_result']
    for i in range(0,len(list0)):
        list0_5=list0[i].get('chars')
        same_words=list0[i].get('words')
        if len(same_words)!=1:
            maxcount=0
            frequency=[[],[],[],[],[],[],[],[],[],[]]
            for i in range(0,10):
                number=str(i)
                if same_words.count(number)>0:
                    if same_words.count(number)>maxcount:
                        maxcount=same_words.count(number)
                    frequency[i].append(same_words.count(number))
            truenumber=str(frequency.index([maxcount]))
            # for j in range(0,len(list0_5)):
            #     list0_5[j]['char']=truenumber
        else:
            truenumber=same_words
            
        
        for j in range(0,len(list0_5)):
            str_=list0_5[j].get('char')
            if str_!=truenumber:
                pass
            else:
                for number in numbers:
                    if str_.find(number)!= -1:
                    #print(number)
                        where[int(number)].append(list0_5[j].get('location'))
                        if int(number)>maxnumber:
                            maxnumber=int(number)
                        for x in xx:
                            if list0_5[j].get('location').get('left') in range(x,x+ww[-1]):
                                if clas[xx.index(x)]==[]:
                                    clas[xx.index(x)].append(number)
                                elif int(str_)>int(clas [xx.index(x)][-1]):
                                    clas[xx.index(x)].append(number)

    print(clas)
    column=[member for member in clas if len(member)>maxnumber-2]
    print(column)



    ii=[i for i in range(0,len(clas)) if clas[i] not in column]
    ii.sort(reverse=True)
    for i in ii:
        if i+1>len(xx):
            pass
        else:
            xx.pop(i)
    #print(where)
    print(len(xx))
    print(len(column))

    listb=[]
    listb0=column[b-1]
    for i in range(0,maxnumber+1):
        i=str(i)
        if listb0.count(i)==0:
            listb.append(i)

    if listb!=[1]:
        for item in listb:
            if where[int(item)]!=[] and item!='1':
                b_=int(item)
    else:
        b_=1



    listc=[]
    listc0=column[c-1]
    for i in range(0,10):
        i=str(i)
        if listc0.count(i)==0:
            listc.append(i)

    if listc!=[1]:
        for item in listc:
            if where[int(item)]!=[] and item!='1':
                c_=int(item)
    else:
        c_=1

    print('班级:',b_,c_,sep='')
    number_top=[]
    for element in where:
        if element==[]:
            number_top.append(0)
        else:
            number_top.append(element[1].get('top'))
    number_top[1]=(number_top[0]+number_top[2])//2
    return xx,number_top












def compare(locations,column_location,W,number_top,b,c):
    for point in locations:
        # Check if the point is within the target region
        print("\npoint:", point)
        if (point[0] < column_location[0] - W or point[0] > column_location[-1] + W or
                point[1] < number_top[0] - W or point[1] > number_top[-1] + W):
            continue
        # Match the point with the rows and columns
        # Rows
        left = 0
        right = len(column_location) - 1
        while left < right:
            mid = (left + right) // 2
            if point[0] < column_location[mid]+W/2:
                right = mid
            elif point[0]> column_location[mid]-W/2:
                left = mid + 1
            else:
                break
        col = left

        # Columns
        left = 0
        right = len(number_top) - 1
        while left < right:
            mid = (left + right) // 2
            if point[1] < number_top[mid]+W/2:
                right = mid
            elif point[1] > number_top[mid]-W/2:
                left = mid + 1
            else:
                break
        row = left

        if col+1==b:
            b_=row
        elif col+1==c:
            c_=row
        # Extract the class ID
        # if col >= 0 and row >= 0:
        #     serial_num[col] = row

        print("col:", col, "row:", row)

    print("class:",b_,c_,sep='')
    return 10*b_+c_