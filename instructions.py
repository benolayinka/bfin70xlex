class Instruction(object):
    counter = 0
    def __init__(self, line_num = None):
        Instruction.counter += 1
        self.line_num = line_num

class Alu(Instruction):
    counter = 0
    current = 200
    def __init__(self, line_num = None):
        type(self).counter += 1
        super(type(self), self).__init__(line_num)

class Mac(Instruction):
    counter = 0
    current = 200
    def __init__(self, line_num = None):
        type(self).counter += 1
        super(type(self), self).__init__(line_num)

class Shift(Instruction):
    counter = 0
    current = 200
    def __init__(self, line_num = None):
        type(self).counter += 1
        super(type(self), self).__init__(line_num)

class Move(Instruction):
    counter = 0
    current = 200
    def __init__(self, line_num = None):
        type(self).counter += 1
        super(type(self), self).__init__(line_num)

class Jump(Instruction):
    counter = 0
    current = 200
    def __init__(self, line_num = None):
        type(self).counter += 1
        super(type(self), self).__init__(line_num)

class Other(Instruction):
    counter = 0
    current = 200
    def __init__(self, line_num = None):
        type(self).counter += 1
        super(type(self), self).__init__(line_num)

class Nop(Instruction):
    counter = 0
    current = 200
    def __init__(self, line_num = None):
        type(self).counter += 1
        super(type(self), self).__init__(line_num)

class Idle(Instruction):
    counter = 0
    current = 200
    def __init__(self, line_num = None):
        type(self).counter += 1
        super(type(self), self).__init__(line_num)  

class Parallel(Instruction):
    counter = 0
    current = 200
    def __init__(self, line_num = None):
        type(self).counter += 1
        super(type(self), self).__init__(line_num)

instructions = [Alu, Mac, Move, Shift, Jump, Other, Nop, Idle, Parallel]