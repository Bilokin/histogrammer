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
            sys.exit('Bye!')
        return True

    def ask_user_choice(self, message: str, mlist: list, default: int = None,
                         ask_exit: bool = False) -> int:
        """
        Asks user to choose the value amoung the proposed ones.
        """
        list_length = len(mlist)
        while True:
            self.say(message)
            # single column print:
            if (len(mlist) < self.column_limit):
                for item, iteration in zip(mlist, range(0, list_length)):
                    if iteration == default:
                        self.say(f'{iteration}: {item} [default]')
                        continue
                    self.say(f'{iteration}: {item}')
            else: #three column print
                strlist = []
                for i in range(0,list_length):
                    if default is not None and i == default:
                        strlist += [f'{i}: {mlist[i]} [default]']
                        continue
                    strlist += [f'{i}: {mlist[i]}']
                strlist = self.add_spaces(strlist)
                for a,b,c in zip(strlist[::3],strlist[1::3],strlist[2::3]):
                    print('{}{}{}'.format(a,b,c))
                if (len(strlist)%3 == 1):
                    print(strlist[-1])
                if (len(strlist)%3 == 2):
                    print('{}{}'.format(strlist[-2],strlist[-1]))
            if ask_exit:
                self.say("To exit: please type 'e'")
            answer = input()
            if self.is_int(answer):
                if int(answer) < list_length:
                    return int(answer)
            if not answer and default is not None:
                return default
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
