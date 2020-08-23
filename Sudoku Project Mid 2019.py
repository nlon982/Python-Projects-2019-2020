import math

# So the dictionary is just a snapshot of the lists, it can only ever be that way.
# The good thing about the dictionary is that I can code actions so easily; just like another abstraction layer.
# With every action though, the "snapshot" has to update. 


def main():
    global b_col
    global b_row
    global b_box
    global oglist
    global list1to9
    global missing_list
    global missing_pos_list
    list1to9 = ["1","2","3","4","5","6","7","8","9"]
    oglist = text_to_list() # setup oglist
    # b stands for board
    b_col = dict()
    for x in range(0,9):
        b_col[str(x)] = []
        for y in range(0,9):
            b_col[str(x)].append(oglist[y][x])
    b_row = dict()
    for y in range(0,9):
        b_row[str(y)] = []
        for x in range(0,9):
            b_row[str(y)].append(oglist[y][x])
    b_box = dict()
    for y in range(0,9):
        for x in range(0,9):
            quotient_x, remainder_x = divmod(x, 3)
            quotient_y, remainder_y = divmod(y, 3)
            box_id = str(quotient_x) + str(quotient_y)
            if box_id not in b_box.keys():
                b_box[box_id] = []
            b_box[box_id].append(oglist[y][x])
    #testing()
    solving_manager()
    #unhighlight_all()
    #check_row(5)
    print_function()
    #testing()

def solving_manager():
    while get_finished_status() == False:
        for y in range(0,9):
            single_row_solver(y)
        for x in range(0,9):
            single_col_solver(x)
        for box_id in b_box.keys(): # I could do similiar for col/row but chose this way because it's cleaner.
            single_box_solver(box_id)

def get_finished_status(): # unhighlight is in terms of row, so let's do the same here
    print("checking....................")
    for row_num in b_row.keys(): #I chose row, but could've chosen col or box too
        missing_list = list(set(list1to9) - set(b_row[row_num]))
        print(missing_list)
        if len(missing_list) != 0:
            print("Not finished")
            return False
    print("finished")
    return True


def single_row_solver(y):
    missing_list, missing_pos_list = gen_check_row(y) # a reminder, that i'm putting the references on to these boys'
    for item in missing_list:
        for x in missing_pos_list: # Answers the question: should I highlight this single value (at y, x)?
            #### Highlight Col
            if item in b_col[str(x)]: 
                bfa(y, x, "B", "H")
            else: #I.e. if it's already highlighted, why re-highlight it
                ### Highlight Box
                box_id = get_box_id(x, y)
                if item in b_box[box_id]:
                    bfa(y, x, "B", "H")
        #### Assigner
        if b_row[str(y)].count("B") == 1:
            position = b_row[str(y)].index("B")
            bfa(y, position, "B", item)
            missing_pos_list.pop(missing_pos_list.index(position))
        unhighlight_all()

def single_col_solver(x): # Yes, I could condense the single row/col solver into one thing, but I think it's better - from a reading with ease perspective, not too.
    missing_list, missing_pos_list = gen_check_col(x)
    for item in missing_list:
        for y in missing_pos_list:
            ### Highlight Row
            if item in b_row[str(y)]:
                bfa(y, x, "B", "H")
            else:
                ### Highlight Box
                box_id = get_box_id(x, y)
                if item in b_box[box_id]:
                    bfa(y, x, "B", "H")
        ### Assigner
        if b_col[str(x)].count("B") == 1:
            position = b_col[str(x)].index("B")
            bfa(position, x, "B", item)
            missing_pos_list.pop(missing_pos_list.index(position))
        unhighlight_all()

def single_box_solver(box_id):
    missing_list, missing_pos_list = gen_check_box(box_id)
    for item in missing_list:
        for psuedo_x in missing_pos_list:
            x, y = get_psuedo_x_to_real(box_id, psuedo_x) # get psuedo to real
            ### Highlight Row
            if item in b_row[str(y)]:
                bfa(y, x, "B", "H")
            else:
                ### Highlight Column
                if item in b_col[str(x)]:
                    bfa(y, x, "B", "H")
        ### Assigner
        if b_box[box_id].count("B") == 1:
            psuedo_x = b_box[box_id].index("B")
            x, y = get_psuedo_x_to_real(box_id, psuedo_x)
            bfa(y, x, "B", item)
            missing_pos_list.pop(missing_pos_list.index(psuedo_x))
        unhighlight_all()
            
                    

def highlight(kind, info): # THIS IS REDUNDANT***, no need to highlight the whole row/col/box - I only need to highlight the relevant positions.
    if kind == "row":
        while "B" in b_row[str(info)]:
            position = b_row[str(info)].index("B")
            bfa(info, position, "B", "H") 
    elif kind == "col":
        while "B" in b_col[str(info)]:
            position = b_col[str(info)].index("B")
            print_function()
            bfa(position, info, "B", "H")
            print_function()
    elif kind == "box":
        while "B" in b_box[info]:
            psuedo_x = b_box[info].index("B") 
            x, y = get_psuedo_x_to_real(info, psuedo_x)
            bfa(y, x, "B", "H") 
        
def get_psuedo_x_to_real(box_id, psuedo_x): # You give it the box_id and the element# (psuedo x) and it gives you x, y coords
        quotient, remainder = divmod(psuedo_x, 3)
        y = quotient + 3 * int((box_id[1]))
        x = remainder + 3 * int((box_id[0]))
        return x, y

def get_box_id(x, y, option = False): # First part: you give it x, y coords and it gives you the box_id. Second part: real to psuedo x (i.e. give x, y coords and get psuedo x)
    quotient_x, remainder_x = divmod(x, 3)
    quotient_y, remainder_y = divmod(y, 3)
    box_id = str(quotient_x) + str(quotient_y)
    if option == True: # i.e. Option True gives you both part 1 and 2 (box_id and psuedo_x)
        psuedo_x = remainder_x + (remainder_y * 3)
        return box_id, psuedo_x
    return box_id

def gen_check_col(x):
    missing_pos_list = []
    missing_list = []
    if "B" in b_col[str(x)]:
        missing_list = list(set(list1to9) - set(b_col[str(x)]))
        for y in range(0, 9):
            if "B" in oglist[y][x]:
                missing_pos_list.append(y) #should missing pos list be a string? ------ It makes sense that positions are ints, and the values are strings
    return missing_list, missing_pos_list

def gen_check_row(y): # general check, as in all
    missing_pos_list = []
    missing_list = []
    if "B" in b_row[str(y)]:
        missing_list = list(set(list1to9) - set(b_row[str(y)]))
        for x in range(0, 9):
            if "B" in oglist[y][x]:
                missing_pos_list.append(x)
    return missing_list, missing_pos_list

def gen_check_box(box_id):
    missing_list = []
    missing_pos_list = []
    if "B" in b_box[box_id]:
        missing_list = list(set(list1to9) - set(b_box[box_id]))
        for psuedo_x in range(0,9):
            if "B" in b_box[box_id][psuedo_x]:
                missing_pos_list.append(psuedo_x)
    return missing_list, missing_pos_list # what's going to be the convention of passing / returning x, y (what order)
# pass a column number, get returned the missing_pos_list in terms of rows. row """ in terms of columns. box in terms of both?
# *** So box is returning in terms of psuedo_x



def unhighlight_all():
    for row_num in b_row.keys(): #I chose row, but could've chosen col or box too
        while "H" in b_row[row_num]:
            position = b_row[row_num].index("H")
            bfa(row_num, position, "H", "B") #giving y and x coords, old and new, now 'bfa' needs to orchestrate that change

def bfa(y, x, old, new): #bfa, for big fricking assigner
    if type(y) != int:
        y = int(y)
    if type(x) != int:
        x = int(x)
    oglist[y][x] = new
    ### col ###
    if old in b_col[str(x)]:
        b_col[str(x)][y] = oglist[y][x]
    ### row ###
    if old in b_row[str(y)]:
        b_row[str(y)][x] = oglist[y][x]
    ### box ###
    box_id, psuedo_x = get_box_id(x, y, True)
    if old in b_box[box_id]:
        b_box[box_id][psuedo_x] = oglist[y][x]

#def highlight(row1

def text_to_list():
    f = open("SudokuInput.txt","r")
    flist = f.readlines()
    oglist = list()
    for i in range(9):
        oglist.append(flist[i].split())
    return oglist

def print_function(statement = ""):
    length_dashes = 21 - len(statement)
    length_dash1 = math.ceil(length_dashes/2)
    length_dash2 = math.floor(length_dashes/2)
    print("/" * length_dash1, statement, "/" * length_dash2, sep="")
    for y in range(9):
        if y == 3 or y == 6 :
            print("-" * 21)
        for x in range(9):
            if x == 3 or x == 6:
                print("|", end=" ")
            print(oglist[y][x], end=" ")
        print()

def testing():
    response = input("Run as normal (any), or test? (t)? ")
    if response == "t":
        input_u = "blank"
        while input_u != "":
            input_u = input("What do you want to look up? ")
            if input_u[0:3] == "col":
                print(b_col[input_u[3:]])
            elif input_u[0:3] == "row":
                print(b_row[input_u[3:]])
            elif input_u[0:3] == "box":
                print(b_box[input_u[3:]])
            else:
                input_u=""
                print("Ending testing..")
main()

