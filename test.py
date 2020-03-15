class Test:
    def __init__(self, name):
        self.name = name
        self.age = 25

    def hello(self):
        print(self.name)
        print(self.age)


class Test2(Test):
    def __init__(self, name):
        super().__init__(name)
        self.x = "ABC"


a = Test("qjhafbdnui")
b = Test("jwenif")
c = Test2("wknofg")

[["Vorspeise1", "Hauptgericht1", "Nachspeise1"], ["Vorspeise2", "Hauptgericht2", "Nachspeise2"]]

["primarykey1", ]
