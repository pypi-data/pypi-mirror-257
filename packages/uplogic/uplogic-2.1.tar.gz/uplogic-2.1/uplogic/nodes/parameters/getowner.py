from uplogic.nodes import ULOutSocket, ULParameterNode


class ULGetOwner(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.owner = None
        self.OUT = self.add_output(self.get_out)

    def get_out(self):
        self.owner
