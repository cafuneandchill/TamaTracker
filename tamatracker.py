import datetime
from abc import ABC, abstractmethod

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


class Tamagotchi(ABC):
    """
    Abstract base class for different types of Tamagotchi
    """

    def __init__(self, name, stage="baby"):
        """
        Creates an instance of a Tamagotchi class

        :param name: Tamagotchi's name
        :type name: str
        :param stage: Tamagotchi's life stage; can be "baby" (default if not specified), "child", "teen", "adult"
        :type stage: str
        :return: None
        """
        self.age = []  # PLACEHOLDER
        self.name = name
        self.stage = stage
        self.spouse = None
        self.is_married = False
        self._children = []

    @property
    def children(self):
        """
        Returns Tamagotchi's children

        :rtype: list
        """
        return self._children

    @children.setter
    def children(self, children):
        """
        Defines Tamagotchi's children

        :param children: Children of a Tamagotchi instance
        :type children: list
        :return: None
        """
        self._children = children
        self.is_married = True

    @abstractmethod
    @property
    def gender(self):
        raise NotImplementedError

    def marry(self, spouse, child_1=None, child_2=None):
        """
        Marries two instances of Tamagotchi together

        :param spouse: Tamagotchi instance that is considered the spouse
        :type spouse: Tamagotchi
        :param child_1: First child
        :type child_1: MyTama
        :param child_2: Second child
        :type child_2: MyTama
        :return: None
        """
        if self.gender is not spouse.gender:
            self.spouse = spouse
            self.is_married = True
            spouse.spouse = self
            spouse.is_married = True
            self.children = [child_1, child_2]
        else:
            raise ValueError("Spouse Tamagotchi object has the same gender")


class Firstborn(Tamagotchi):
    """
    Child class of Tamagotchi class that is used to define Tamagotchi of the first generation in a family line
    """

    def __init__(self, name, stage="baby"):
        """
        Creates an instance of Firstborn class

        :param name: Firstborn's name
        :type name: str
        :param stage: Firstborn's life stage
        :type stage: str
        :return: None
        """
        super().__init__(name, stage)
        self.traits = {
            "body": self.name,
            "eyes": self.name,
            "headgear": self.name,
            "misc": self.name,
            "color": self.name
        }

    @property
    def gender(self):
        raise NotImplementedError


class MyTama(Tamagotchi):
    """
    Child class of Tamagotchi class that is used to define Tamagotchi from the second generation onward.

    Traits are defined by the name (string) of the first generation Tamagotchi that has that trait.
    """

    def __init__(self, name,  body, eyes, headgear, misc, color, stage="baby"):
        """
        Creates an instance of MyTama class

        :param name: MyTama's name; usually follows the naming pattern of {base name} + 'tchi'
        :type name: str
        :param stage: MyTama's life stage
        :type stage: str
        :param body: Inherited body type; defined by the name of the first-gen Tamagotchi that has that type
        :type body: str
        :param eyes: Inherited eyes type
        :type eyes: str
        :param headgear: Inherited headgear type
        :type headgear: str
        :param misc: Inherited miscellaneous type
        :type misc: str
        :return: None
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

    def __init__(self, tama):
        """
        Create an instance of Timeline

        :param tama: Defines the Tamagotchi that would be tracked in the Timeline instance
        :type tama: Tamagotchi
        :return: None
        """
        self.timeline = []
        self.tama = tama

    def add_event(self, timestamp, **kwargs):
        """
        Adds an event to the timeline

        :param timestamp: Used to set up a timestamp for the event - [year, month, day, hour, minute, second]
        :type timestamp: list
        :param kwargs: May have optional parameters such as happiness, hunger and Tamagotchi stage
        :key happiness: Tamagotchi's happiness at the time of the event, should be int
        :key hunger: Tamagotchi's hunger at the time of the event, should be int
        :key stage: Tamagotchi's growth stage, should be "baby", "child", "teen" or "adult"
        :key ate: Food that Tamagotchi ate; is a list - [[food_1, amount_1], [food_2, amount_2], ...]
        :key played_with: Toys that Tamagotchi played with; is a list - [[toy_1, times_played_1], ...]
        :return: None
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

        :param event_n: The number of the event; the order of events in the timeline starts from 1
        :type event_n: int
        :return: None
        """
        self.timeline.pop(event_n - 1)

    def edit_event(self, event_n, **kwargs):
        """
        Edits an event in the timeline

        :param event_n: Event number, starts from 1
        :param kwargs: Optional keyword arguments
        :key timestamp: Event's new timestamp, defines as in the add_event() method
        :key happiness: New happiness level
        :key hunger: New hunger level
        :key stage: New growth stage
        :key ate: The food Tamagotchi ate, defined in the same way as in the add_event() method
        :key played_with: The toys Tamagotchi played with, defined in the same way as on the add_event() method
        :return: None
        """
        event = self.timeline[event_n - 1]
        event.update(kwargs)

    @staticmethod
    def predict_happiness(initial, stage):
        """
        Predicts the time required for the happiness meter to drop to zero starting from the initial happiness

        :param initial: Defines the initial happiness
        :type initial: int
        :param stage: Defines the life stage of a Tamagotchi, so the function knows which decay rate to use
        :type stage: str
        :return: Returns time to zero happiness
        :rtype: float
        """
        decay_rate = HAPPINESS_DECAY_RATE.get(stage)

        time_to_zero = - initial / decay_rate
        return time_to_zero

    @staticmethod
    def predict_hunger(initial, stage):
        """
        Predicts the time required for the hunger meter to drop to zero starting from the initial hunger

        :param initial: Defines the initial hunger
        :type initial: int
        :param stage: Defines the life stage of a Tamagotchi, so the function knows which decay rate to use
        :type stage: str
        :return: Returns time to zero hunger
        :rtype: float
        """
        decay_rate = HUNGER_DECAY_RATE.get(stage)

        time_to_zero = - initial / decay_rate
        return time_to_zero