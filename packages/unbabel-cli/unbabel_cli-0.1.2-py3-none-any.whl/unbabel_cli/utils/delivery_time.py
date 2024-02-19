import math
from datetime import datetime, timedelta
from typing import List, TypedDict

from unbabel_cli.utils.interfaces import TranslationEvent


def process_avg_delivery_time(
    events: List[TranslationEvent], windows_size: int
) -> None:
    average_calculator = AverageCalculator(windows_size)
    starting_time = events[0]["timestamp"].replace(second=0, microsecond=0)

    number_of_minutes = get_difference_in_minutes(
        starting_time, events[-1]["timestamp"]
    )

    for minute in range(0, number_of_minutes + 1):
        average_calculator.remove_active_value(minute)

        duration_in_minute = 0
        actual_time = starting_time + timedelta(minutes=minute)

        # This while loop checks for all the events that are in the same minute
        # and adds them all to the average calculator
        # as well as removing the value from the events list
        while events[0]["timestamp"] <= actual_time:
            event = events.pop(0)
            duration_in_minute += event["duration"]
            if len(events) == 0:
                break
        if duration_in_minute > 0:
            average_calculator.add_active_value(minute, duration_in_minute)

        display_average_delivery_time(actual_time, average_calculator.get_average())


def display_average_delivery_time(date: datetime, average_delivery_time: float) -> None:
    # Why function just to print?
    # To separate the logic of the calculation from the logic of the display, which can be useful
    # for scaling and testing
    print(
        {
            "date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "average_delivery_time": average_delivery_time,
        }
    )


def get_difference_in_minutes(
    reference_date: datetime, date_to_compare: datetime
) -> int:
    return math.ceil((date_to_compare - reference_date).total_seconds() / 60)


class AverageCalculator:
    """Class to calculate the moving average of the delivery time"""

    def __init__(self, window_range: int):
        self.active_values: List[ActiveAverageValue] = []
        self.window_range = window_range

    def add_active_value(self, relative_first_minute: int, duration: int):
        """This Adds the active value to the list of averages, which means
        that the average will be calculated with this value until it is removed

        Args:
            relative_first_minute (int): the minute at which the value starts
            duration (int): the delivery time duration in seconds
        """
        self.active_values.append(
            ActiveAverageValue(minute=relative_first_minute, duration=duration)
        )

    def get_average(self):
        """Calculates the average using the active values

        Returns:
            int: the average value of the array
        """
        # This could be optimized by storing the total duration and the number of elements
        # and updating them as the values are added and removed

        if len(self.active_values) == 0:
            return 0
        total_duration = 0

        for average in self.active_values:
            total_duration += average["duration"]
        return total_duration / len(self.active_values)

    def remove_active_value(self, relative_minute: int):
        """removes the oldest from the list of active values if it is older than the window range

        Args:
            relative_minute (int): the minute to compare with the oldest value
        """
        if len(self.active_values) == 0:
            return
        if relative_minute - self.active_values[0]["minute"] == self.window_range:
            self.active_values.pop(0)


class ActiveAverageValue(TypedDict):
    minute: int
    duration: int
