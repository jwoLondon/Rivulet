# pylint: skip-file

list1 = []
list2 = []
list3 = []

def glyph1():    
    list1.append(0)

    list2.extend([0,  # fibonacci number
        1,   # number in waiting
        0,   # how many we've calculated
        10  # how many we'll calcuate
        ]) # stack 1: consts

    list3.append(0)
    list3.append(0)

def glyph2():

    while(True):
        global list1
        global list2
        global list3

        stack_bckup = [
            list(list1),
            list(list2),
            list(list3)
        ]

        list3[0] = list2[0]
        list2[0] += list2[1]
        list2[1] = list3[0]
        list2[2] += 1
        list1.append(list2[0])

        list3[1] = list2[3]
        list3[1] -= list2[2]
        # this is the revert
        if list3[1] <= 0:
            # set lists back to their previous condition
            list1 = stack_bckup[0]
            list2 = stack_bckup[1]
            list3 = stack_bckup[2]
            return

def glyph3():
    global lists
    print(list1)

glyph1()
glyph2()
glyph3()
