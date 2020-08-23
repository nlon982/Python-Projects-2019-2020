def print_out(a_sudoku):
    print()
    for row in a_sudoku.row.keys():
        for cell in a_sudoku.row[row]:
            if isinstance(cell, list):
                continue
            if cell.data == None:
                #print("N", end = ";  ")
                print("{}".format(cell.canditates), end = ";  ")
            else:
                print("{}".format(cell.data), end = ";  ")
            #print("d: {}, c: {}".format(data, cell.canditates), end = ";  ")
        print()

class Cell:
    def __init__(self, col_num, row_num, box_id): # I could work out the box id again, or just work it out once and pass it
        self.data = None
        self.col_num = col_num
        self.row_num = row_num
        self.box_id = box_id # atleast, id implies string
        self.canditates = []

    def update_canditates(self):
        self.canditates = list(set(a_sudoku.row[self.row_num][0]) & set(a_sudoku.col[self.col_num][0]) & set(a_sudoku.box[self.box_id][0]))

    def print_canditates(self): # debugging use only
        print(a_sudoku.row[self.row_num][0])
        print(a_sudoku.col[self.col_num][0])
        print(a_sudoku.box[self.box_id][0])

    def set_data(self, data):
        # todo: check data is within constraints
        self.data = data
        a_sudoku.row[self.row_num][0].remove(data) # this is O(n) for sure
        a_sudoku.col[self.col_num][0].remove(data)
        a_sudoku.box[self.box_id][0].remove(data)
        
        a_sudoku.empty_cells.remove(self) ## EXTRA
        
        for cell in a_sudoku.row[self.row_num][1:] + a_sudoku.col[self.col_num][1:] + a_sudoku.box[self.box_id][1:]: # it will do the changed one many times, I can fix this with sets (-intersection)
            cell.update_canditates()
        # update candiates in respective, row, col, box (or wait until all possible solves can be done?)
    

def get_box_id(x, y, option = False): # First part: you give it x, y coords and it gives you the box_id. Second part: real to psuedo x (i.e. give x, y coords and get psuedo x)
    quotient_x, remainder_x = divmod(x, 3)
    quotient_y, remainder_y = divmod(y, 3)
    box_id = str(quotient_x) + str(quotient_y)
    if option == True: # i.e. Option True gives you both part 1 and 2 (box_id and psuedo_x)
        psuedo_x = remainder_x + (remainder_y * 3)
        return box_id, psuedo_x
    return box_id

def import_from_text(file_name):
    a_file = open("SudokuInput.txt","r")
    a_string = a_file.read()
    a_list = a_string.split("\n")
    for i in range(len(a_list)):
        a_list[i] = a_list[i].split(" ")
    return a_list # i've forgotten how this works
    


class Sudoku:
    def __init__(self, width, height):
        self.row = dict() # I could set onetonine as first element up better with dict comprehension
        self.col = dict()
        self.box = dict()
        self.empty_cells = [] ## EXTRA
        for col_num in range(width):
            self.col[col_num] = [onetonine.copy()]
            for row_num in range(height):
                box_id = get_box_id(col_num, row_num) # maybe I need to consider making them all strings
                imported = import_from_text("SudokuInput.txt")
                    
                a_cell = Cell(col_num, row_num, box_id)
                if row_num not in self.row.keys():
                    self.row[row_num] = [onetonine.copy()] + [a_cell]
                else:
                    self.row[row_num].append(a_cell)
                self.col[col_num].append(a_cell)
                if box_id not in self.box.keys():
                    self.box[box_id] = [onetonine.copy()] + [a_cell]
                else:
                    self.box[box_id].append(a_cell)

                try:
                    imported_val = int(imported[row_num][col_num])
                except: # basically an else
                    imported_val = None

                if imported_val in onetonine: # y, x,
                    data = imported_val
                    a_cell.data = data
                    self.row[row_num][0].remove(data) # this is O(n) for sure
                    self.col[col_num][0].remove(data)
                    self.box[box_id][0].remove(data)
                else:
                    self.empty_cells.append(a_cell) ## EXTRA
                    
        
width = 9
height = 9 # should probably limit width/height to being same?
onetonine = [1, 2, 3, 4, 5, 6, 7, 8, 9] # should probably make this via list comprehension for adaptability
a_sudoku = Sudoku(width, height)
for cell in a_sudoku.empty_cells:
    cell.update_canditates()

## Note, unaffected cells haven't been made to update their candiate lists. An idea is that canditate lists are made when cell first instantated?
## Moreover, if cell first instantated is on a baln kcanvas, we know what the candidate list is going to be (1, 2, 3, 4, 5, 6, 7, 8, 9)


### Filling the first box with 1 to 9
"""
count = 1
for cell in a_sudoku.box["00"][1:]:
    cell.set_data(count)
    count += 1
"""
###

# my first attempt as visualization
#print_out(a_sudoku)


count = 10000
while count != 0:
    count = 0
    for cell in a_sudoku.empty_cells:
        if len(cell.canditates) == 1:
            count += 1
            cell.set_data(cell.canditates[0])
            #print_out(a_sudoku)
            #print(cell.data, cell.col_num, cell.row_num)
        

print_out(a_sudoku)
    



#  Wow! it all works
