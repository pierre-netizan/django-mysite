class Xxx:
    def __init__(self,title):
        self.title=title
    def __str__(self):
        return f"{self.__class__.__name__}({self.title})"

print(Xxx('ooo'))

    