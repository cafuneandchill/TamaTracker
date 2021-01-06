import datetime
from abc import ABC, abstractmethod
from typing import Optional, TypedDict, MutableSequence

HAPPINESS_DECAY_RATE = {
    "baby": -60,  # bar/h, PLACEHOLDER
    "child": -1,  # bar/h, PLACEHOLDER
    "teen": -1,  # bar/h, PLACEHOLDER
    "adult": -1,  # bar/h, PLACEHOLDER
}
HUNGER_DECAY_RATE = {
    "baby": -60,  # bar/h, PLACEHOLDER
    "child": -1,  # bar/h, PLACEHOLDER
    "teen": -1,  # bar/h, PLACEHOLDER
    "adult": -1,  # bar/h, PLACEHOLDER
}


Owner = TypedDict('Owner', {'name': str, 'friend_code': str})
Traits = TypedDict('Traits', {'body': str,
                              'eyes': str,
                              'headgear': str,
                              'misc': str,
                              'color': str})


class Tamagotchi(ABC):
    """
    Abstract base class (interface, protocol) for different types of Tamagotchi
    """

    def __init__(self, name: str, stage: int = 0):
        """
        Creates an instance of a Tamagotchi class
        """
        self._age = []  # PLACEHOLDER
        self._name: str = name
        self._stage: int = stage
        self._traits: Traits = dict()
        self._owner: Owner = dict()
        self._spouse: Optional[Tamagotchi] = None
        self._children: MutableSequence[Tamagotchi] = []
        self._timeline: Optional[Timeline] = None

    @abstractmethod
    @property
    def age(self):
        pass

    @abstractmethod
    @age.setter
    def age(self, age):
        pass

    @abstractmethod
    @property
    def age_in_tama_years(self) -> int:
        pass

    @abstractmethod
    @property
    def name(self):
        pass

    @abstractmethod
    @name.setter
    def name(self, name: str):
        pass

    @abstractmethod
    @property
    def stage(self):
        pass

    @abstractmethod
    @stage.setter
    def stage(self, stage: int):
        pass

    @abstractmethod
    @property
    def traits(self):
        pass

    @abstractmethod
    @traits.setter
    def traits(self, traits: Traits):
        pass

    @abstractmethod
    @property
    def owner(self):
        pass

    @abstractmethod
    @owner.setter
    def owner(self, owner: Owner):
        pass

    @abstractmethod
    @property
    def children(self):
        pass

    @abstractmethod
    @children.setter
    def children(self, children: MutableSequence['Tamagotchi']):
        pass

    @abstractmethod
    @property
    def gender(self):
        pass

    @abstractmethod
    @gender.setter
    def gender(self, gender: str):
        pass

    @abstractmethod
    @property
    def timeline(self):
        pass

    @abstractmethod
    @timeline.setter
    def timeline(self, timeline: 'Timeline'):
        pass

    @abstractmethod
    @property
    def is_married(self):
        if self._spouse:
            return True
        else:
            return False

    @abstractmethod
    def marry(self, spouse: 'Tamagotchi', child_1: 'Tamagotchi', child_2: 'Tamagotchi'):
        pass


class Firstborn(Tamagotchi):
    """
    Child class of Tamagotchi class that is used to define Tamagotchi of the first generation in a family line
    """

    def __init__(self, name: str, stage: int = 0):
        """
        Creates an instance of Firstborn class
        """
        super().__init__(name, stage)
        self._traits = {
            "body": self._name,
            "eyes": self._name,
            "headgear": self._name,
            "misc": self._name,
            "color": self._name
        }

    @property
    def gender(self):
        raise NotImplementedError


class MyTama(Tamagotchi):
    """
    Child class of Tamagotchi class that is used to define Tamagotchi from the second generation onward.

    Traits are defined by the name (string) of the first generation Tamagotchi that has that trait.
    """

    def __init__(self, name,  body, eyes, headgear, misc, color, stage=0):
        """
        Creates an instance of MyTama class
        """
        super().__init__(name, stage)
        self.traits = {
            "body": body,
            "eyes": eyes,
            "headgear": headgear,
            "misc": misc,
            "color": color
        }


class Timeline:
    """
    An object that represents the sequence of events in the live of a Tamagotchi
    """

    def __init__(self, tama: Tamagotchi):
        """
        Create an instance of Timeline
        """
        self.timeline = []
        self.tama: Tamagotchi = tama

    def add_event(self, timestamp, **kwargs):
        """
        Adds an event to the timeline
        """
        event = {
            "timestamp": datetime.datetime(*timestamp),
            "happiness": kwargs.get("happiness", None),
            "hunger": kwargs.get("hunger", None),
            "stage": kwargs.get("stage", None),
            "ate": kwargs.get("ate", None),
            "played_with": kwargs.get("played_with", None),
        }
        self.timeline.append(event)
        self.timeline.sort()  # WRITE THE KEY FOR SORTING

    def remove_event(self, event_n):
        """
        Removes an event from the timeline
        """
        self.timeline.pop(event_n - 1)

    def edit_event(self, event_n, **kwargs):
        """
        Edits an event in the timeline
        """
        event = self.timeline[event_n - 1]
        event.update(kwargs)

    @staticmethod
    def predict_happiness(initial, stage):
        """
        Predicts the time required for the happiness meter to drop to zero starting from the initial happiness
        """
        decay_rate = HAPPINESS_DECAY_RATE.get(stage)

        time_to_zero = - initial / decay_rate
        return time_to_zero

    @staticmethod
    def predict_hunger(initial, stage):
        """
        Predicts the time required for the hunger meter to drop to zero starting from the initial hunger
        """
        decay_rate = HUNGER_DECAY_RATE.get(stage)

        time_to_zero = - initial / decay_rate
        return time_to_zero
