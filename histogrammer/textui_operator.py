import sys

class TextUIOperator():
    """
    Class that interacts with the user.
    """
    def __init__(self):
        """
        Constructor method.
        """
        self.column_limit = 10

    def say(self, message: str) -> None:
        """
        Prints a message.
        """
        print(message)

    def ask_continue_or_exit(self) -> bool:
        """
        Asks user if we want to continue the main loop
        """
        self.say("To continue press Enter, to exit please type 'e'")
        answer = input()
        if answer == 'e':
            return False
        return True

    def ask_user_choice(self, message: str, mlist: list, ask_exit: bool = False) -> int:
        """
        Asks user to choose the value amoung the proposed ones
        """
        while True:
            self.say(message)
            # single column print:
            if (len(mlist) < self.column_limit):
                iteration = 0
                for item in mlist:
                    print (str(iteration) + ": " + item)
                    iteration += 1
            else: #three column print
                strlist = [f'{i}: {mlist[i]}' for i in range(0,len(mlist))]
                strlist = self.add_spaces(strlist)
                for a,b,c in zip(strlist[::3],strlist[1::3],strlist[2::3]):
                    print('{}{}{}'.format(a,b,c))
                if (len(strlist)%3 == 1):
                    print(strlist[-1])
                if (len(strlist)%3 == 2):
                    print('{}{}'.format(strlist[-2],strlist[-1]))
            if ask_exit:
                print("To exit: please type 'e'")
            answer = input()
            if self.is_int(answer):
                if int(answer) < len(mlist):
                    return int(answer)
            if answer == 'e':
                sys.exit('Bye!')
            self.say(f'Answer {answer} not correct, please try again!')
    
    def is_int(self, s: str) -> bool:
        """
        Returns True if argument is integer.
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

            
    def add_spaces(self, strlist: list) -> list:
        """
        Adds spaces to make columns.
        """
        maxlen = len(max(strlist, key=len)) +1
        return [ s.ljust(maxlen) for s in strlist]
