from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket


class ULToggleProperty(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.mode = 0
        self.done = False
        self.OUT = self.add_output(self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        if not self.get_input(self.condition):
            return
        game_object = self.get_input(self.game_object)
        property_name = self.get_input(self.property_name)
        obj = game_object.blenderObject if self.mode else game_object
        value = obj.get(property_name)
        obj[property_name] = not value
        self.done = True
