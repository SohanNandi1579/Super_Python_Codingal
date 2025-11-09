# class dad:
#     def __init__(self,eyes,aggressive):
#         self.eyes=eyes
#         self.aggressive=aggressive
#
#     def disp(self):
#         print("eye color is ", self.eyes)
#         print ("aggressive is ", self.aggressive)
#
# class mom:
#     def __init__(self,haircolor):
#         self.haircolor=haircolor
#
# class son(dad,mom):
#     def __init__(self,name,age, eyes, aggressive,haircolor):
#         dad.__init__(self,eyes,aggressive)
#         mom.__init__(self,haircolor)
#         self.name=name
#         self.age=age
#
# obj = son("john", 20, "brown", "yes")
# obj.disp()


class dad:
    def __init__(self,eyes,aggressive):
        self.eyes=eyes
        self.aggressive=aggressive

    def disp(self):
        print("eye color is ", self.eyes)
        print ("aggressive is ", self.aggressive)

class mom:
    def __init__(self,haircolor):
        self.haircolor=haircolor

class son(mom, dad):
    def __init__(self,name,age, eyes, aggressive,haircolor):
        super().__init__(haircolor) # super(only takes first paramter i.e. mom)
        dad.__init__(self,eyes,   aggressive)
        self.name=name
        self.age=age

obj = son("john", 20, "brown", "yes", "criminal hair")
obj.disp()

