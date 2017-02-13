import random
import time

class MatchingGame():
    

    def __init__(self):
        '''
        Initilization of instance variables:
            flipped = []; will have dimensions nxm and will be initialized to 0
                          which signifies that the element has not been matched yet.
                          when an element is matched, its value in flipped will be
                          set to 1
            answers = []; will have letters randomly assigned into each location
                          in the matrix where each letter appears exactly twice
            n = 0; wil; be set to the number of rows of the game
            m = 0; will be set to the number of columns of the game
        '''
        self.flipped = []
        self.answers = []
        self.n = 0 #number of rows
        self.m = 0 #number of columns
    

    def make_answers(self, num_letters):
        '''
        This method randomly assigns letters to the self.answers instance variable.
        The number of unique letters is provided by parameter num_letters and each
        letter appears exactly twice in self.answers
        
        Args:
            num_letters: number of unique letters to be matched in the game
        
        Precondition:
            0 < num_letters <= 26
        '''
        letters = [chr(i) for i in range(65, 65+num_letters)]
        freqs = [2 for i in range(num_letters)]
        possible_indices = [i for i in range(num_letters)]
        for i in range(self.n):
            for j in range(self.m):
                index = random.choice(possible_indices)
                self.answers[i][j] = letters[index]
                freqs[index] -= 1
                if freqs[index] == 0:
                    possible_indices.remove(index)
   
    def make_board(self, num_letters):
        '''  
        This method creates the dimensions of the board by trying to find the
        factors of (num_letters*2) that are closest together, e.g:
            num_letters = 4 -> would have 16 total elements -> 4x4
            num_letters = 5 -> would have 10 total elements -> 5x5
        This method then sets all the instance variables. It sets self.n and
        self.m with the factors (as described above) and initializes self.flipped
        and self.answers to have nxm dimensions with default values 0 and '' 
        respectively. Then, this method calls the self.make_answers function
        to randomly fill the board with letters
        
        Args:
            num_letters: number of unique letters to be matched in the game
        
        Precondition:
            0 < num_letters <= 26
        ''' 
        factors = []
        for i in range(1, num_letters*2+1):
            if (num_letters*2) % i == 0:
                factors.append(i)
        
        n = factors[int(len(factors)/2)]
        m = int((num_letters*2)/n)
        
        #set the instance variables
        self.n = n
        self.m = m
        self.flipped = [[0 for j in range(m)] for i in range(n)]
        self.answers = [['' for j in range(m)] for i in range(n)]
        self.make_answers(num_letters)
    

    def print_current(self):
        '''
        This method prints the current state of the board. If letters have
        been matched those letters will be printed. Otherwise, a '+' will be
        printed in those spaces instead. Whether a letter has been matched
        with its counterpart is determined by if the corresponding point in 
        self.flipped is equal to 1. A top border of 0 through self.n and
        a left border of 0 through self.m are also printed for easier use by 
        the user. The top left most corner of the board is filled with a '-'. 
        '''
        result = ''
        for i in range(self.n+1):
            if i == 0: #top border
                for j in range(self.m+1):
                    if j == 0: #(0,0) spot in the printed matrix
                        result += '-   ' 
                    else: #numbers in the top border
                        result += str(j-1) + '  ' 
                result += '\n'
            else:
                for j in range(self.m+1):
                    if j == 0: #left border
                        if i > 10: #one digit number
                            result += str(i-1) + '  ' 
                        else:
                            result += str(i-1) + '   '
                    else:
                        if self.flipped[i-1][j-1] == 0:
                            result += '+  ' #default value
                        else: #matched numbers
                            result += str(self.answers[i-1][j-1]) + '  '
                result += '\n'
        print(result)

    def match(self, i1, j1, i2, j2):          
        '''        
        This method reveals the letters at the points the user selects by 
        temporarily setting the corresponding points in self.flipped to 1
        and calling self.print_current. If the two letters in the positions 
        match (which we can check by comparing their values in self.answers), 
        "It's a match!" is printed. Otherwise, "Sorry, it wasnt a match" is 
        printed and the corresponding points in self.flipped are reset to 0
        so that the letters at those points are not revealed the next time
        self.print_current is called. 
        
        Args:
            i1: row of the first point inputted by the user
            j1: column of the first point inputted by the user
            i2: row of the second point inputted by the user
            j2: column of the second point inputted by the user
        
        Precondition: i1, j1, i2, and j2 are integers and in bounds of self.answers
                      and self.flipped
        '''
        self.flipped[i1][j1] = 1
        self.flipped[i2][j2] = 1
        self.print_current()
        if self.answers[i1][j1] == self.answers[i2][j2]:
            print("It's a match!")
        else:
            print("Sorry, it wasn't a match.")
            self.flipped[i1][j1] = 0 
            self.flipped[i2][j2] = 0

    def game_over(self):
        '''
        This method checks if the game is over or not by iterating through
        self.flipped and seeing if any of the elements are equal to 0. If 
        there are elements equal to 0, return False since the game is not over.
        Otherwise, return True since all the letters have been matched.
        
        Returns: boolean
        '''
        for i in range(self.n):
            for j in range(self.m):
                if self.flipped[i][j] == 0:
                    return False
        return True
        

    def to_time(self, seconds):
        '''
        This method converts the number of seconds into the format:
            h hours m minutes s seconds
        and returns the resulting string.
        
        Returns: string
        '''
        seconds = round(seconds)
        if seconds < 60:
            return str(seconds) + " seconds"
        elif seconds < 3600:
            mins = int(seconds/60)
            seconds = seconds % 60
            return str(mins) + " mins " + str(seconds) + " seconds"
        else:
            hours = int(seconds/3600)
            seconds = seconds % 3600
            mins = int(seconds/60)
            seconds = seconds % 60
            return str(hours) + " hours " + str(mins) + " minutes " + \
                    str(seconds) + " seconds"
    

    def acceptable(self, string, coord_type):
        '''
        This method checks if the given string inputted by the user is an 
        integer and in bounds of a nxm matrix.
        
        Args:
            string: user input
            coord_type: what the user is being prompted to input
                    
        Returns: boolean
        '''
        if len(string) == 0:
            return False
        if coord_type == 'row':
            if self.n >= 10 and len(string) > 2:
                return False
            if self.n < 10 and len(string) > 1:
                return False
            if int(string) < 0 or int(string) >= self.n:
                return False
        elif coord_type != 'row':
            if self.m >= 10 and len(string) > 2:
                return False
            if self.m < 10 and len(string) > 1:
                return False
            if int(string) < 0 or int(string) >= self.m:
                return False

        if len(string) == 1 and (ord(string) > 57 or ord(string) < 48):
            return False
        if len(string) == 2 and (ord(string[0]) > 57 or ord(string[1]) > 57 or \
                                ord(string[0]) < 48 or ord(string[1]) < 48):
            return False
        return True
    

    def take_input(self, input_num, coord_type):
        '''
        This method calls the self.acceptable method to see if the user input
        is an integer and in bounds of a nxm matrix. If the user input fails 
        those requirements, this method will keep prompting the user to 
        enter valid input. Finally, the valid input is returned as an integer.
        
        Args:
            input_num: user input
            coord_type: a string that indicates what the user is being prompted for
                    
        Returns: int
        '''
        while not self.acceptable(input_num, coord_type):
            if coord_type == 'row':
                input_num = input("enter a row number between 0-" + str(self.n-1) + ": ")
            else:
                input_num = input("enter a column number between 0-" + str(self.m-1) + ": ")
        return int(input_num)
    
   
    def __main__(self):
        '''
        This method allows the user to play the game. It first prompts the user
        to choose the number of unique letters to match in the game and then calls
        self.make_board to set values to self.flipped and self.answers. Then,
        further instructions for what values the user can input to try to match
        letters are printed. While the player hasn't matched all the letters in the
        game, this method prompts the user to enter row and column values that
        two unique positions in the matrices that have not been matched before.
        Each time a user enters two positions, the current state of the board
        is displayed with the two letters at those positions and previously
        matched letters revealed. Whether or not those two positions are a match
        is printed. This method also keeps track of how long it takes the user to match
        all the letters in the game. When the player has matched all the letters
        in the game, "Nice work!" and the length of time it took the player
        to finish the game is printed.
        ''' 
        print("Ready to test your memory?")
        num_letters = input("Type in the number of letters you want to match: ")
        while len(num_letters) == 0 or len(num_letters) > 2 or \
        ord(num_letters[0]) < 48 or ord(num_letters[0]) > 57 or\
        int(num_letters) <= 0 or int(num_letters) > 26:
            num_letters = input("Please enter a number between 1 and 26: ")
            
        self.make_board(int(num_letters))
        
        print("You will be prompted to enter the row and column numbers of \
        the two points on the board you want to try to match." )
        print("Valid inputs for rows are 0 through " + str(self.n-1) + " inclusive" \
        " and valid inputs for columns are 0 through " + str(self.m-1) + " inclusive")
        self.print_current()
        
        start = time.time()        
        while not self.game_over():
            i1 = input("row: ")
            i1 = self.take_input(i1, "row")
            j1 = input("col: ")
            j1 = self.take_input(j1, "col")
            
            while self.flipped[i1][j1] == 1:
                print("Please enter values that you haven't matched before.")
                i1 = input("row: ")
                i1 = self.take_input(i1, "row")
                j1 = input("col: ")
                j1 = self.take_input(j1, "col")
                            
            i2 = input("row: ")
            i2 = self.take_input(i2, "row")
            j2 = input("col: ")
            j2 = self.take_input(j2, "col")
            

            while self.flipped[i2][j2] == 1:
                print("Please enter values that you haven't matched before.")
                i2 = input("row: ")
                i2 = self.take_input(i2, "row")
                j2 = input("col: ")
                j2 = self.take_input(j2, "col")                
            while i2 == i1 and j2 == j1:
                print("Please enter values different from your previous input.")
                i2 = input("row: ")
                i2 = self.take_input(i2, "row")
                j2 = input("col: ")
                j2 = self.take_input(j2, "col")
                
            self.match(i1,j1,i2,j2)
            
        end = time.time()
        
        print("Nice work!")   
        print("Duration: " + self.to_time(end-start))