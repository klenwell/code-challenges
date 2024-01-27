class PulseModule:
    TYPES = {
        '%': 'flip-flop',
        '&': 'conjunction',
        'b': 'broadcaster'
    }

    @staticmethod
    def create(id):
        mod_type = PulseModule.TYPES.get(id[0])
        if mod_type == 'flip-flop':
            return FlipFlopModule(id)
        elif mod_type == 'conjunction':
            return ConjunctionModule(id)
        elif mod_type == 'broadcaster':
            return BroadcasterModule(id)
        else:
            raise Exception(f"Invalid module id: {id}")

    def __init__(self, id):
        self.id = id
        self.on = 0
        self.last_pulse_from = {}
        self.pulses_received = {
            'low': 0,
            'high': 0
        }
        self.pulses_sent = {
            'low': 0,
            'high': 0
        }
        self.input_mods = None
        self.initial_state = None

    @property
    def state(self):
        memory = sorted([(k.name, v) for k, v in self.last_pulse_from.items()])
        return (self.name, self.on, memory)

    @property
    def name(self):
        return self.id[1:]

    def wire_up_inputs(self, input_mods):
        self.input_mods = input_mods
        self.reset_memory()
        self.initial_state = self.state

    def reset_memory(self):
        for input_mod in self.input_mods:
            self.last_pulse_from[input_mod] = 'low'
        return self

    def receive_pulse_from_mod(self, type, origin_mod):
        self.pulses_received[type] += 1

    def send_pulse(self, type):
        self.pulses_sent[type] += 1
        return type

    def __repr__(self):
        on_off = 'ON' if self.on == 1 else 'off'
        return f"<{self.__class__.__name__} name={self.name} {on_off} {self.pulses_sent}>"


class FlipFlopModule(PulseModule):
    def receive_pulse_from_mod(self, type, origin_mod):
        super().receive_pulse_from_mod(type, origin_mod)

        # If a flip-flop module receives a high pulse, it is ignored and nothing happens.
        if type == 'high':
            return None

        # However, if a flip-flop module receives a low pulse, it flips between on and off.
        # If it was off, it turns on and sends a high pulse. If it was on, it turns off and
        # sends a low pulse.
        if self.on == 0:
            self.on = 1
            return 'high'
        else:
            self.on = 0
            return 'low'


class ConjunctionModule(PulseModule):
    @property
    def pulse_type(self):
        # Conjunction modules (prefix &) remember the type of the most recent pulse received
        # from each of their connected input modules; they initially default to remembering a
        # low pulse for each input. When a pulse is received, the conjunction module first updates
        # its memory for that input. Then, if it remembers high pulses for all inputs, it sends a
        # low pulse; otherwise, it sends a high pulse.
        memory_set = set(list(self.last_pulse_from.values()))
        if memory_set == set(['high']):
            return 'low'
        else:
            return 'high'

    def receive_pulse_from_mod(self, type, input_mod):
        super().receive_pulse_from_mod(type, input_mod)
        self.last_pulse_from[input_mod] = type
        return self.pulse_type


class BroadcasterModule(PulseModule):
    @property
    def name(self):
        return 'broadcaster'

    def receive_pulse_from_mod(self, type, origin_mod):
        # There is a single broadcast module (named broadcaster). When it receives a pulse, it
        # sends the same pulse to all of its destination modules.
        super().receive_pulse_from_mod(type, origin_mod)
        return type


class ButtonModule(PulseModule):
    @property
    def name(self):
        return 'button'


class TerminalModule(PulseModule):
    @property
    def name(self):
        return self.id

    def receive_pulse_from_mod(self, type, origin_mod):
        super().receive_pulse_from_mod(type, origin_mod)
        return None
