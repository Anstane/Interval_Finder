from datetime import datetime, timedelta
from typing import List, Dict


def generate_free_windows(
        start_time_str: str,
        end_time_str: str,
        busy_periods: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
    """
    The function takes as input the beginning of the working day, the end and a list of occupied periods ->
    returns a list of windows during the workday, excluding periods from the busy_periods dictionary.
    """

    start_time = datetime.strptime(start_time_str, '%H:%M')
    end_time = datetime.strptime(end_time_str, '%H:%M')

    busy_periods = [
        (
            datetime.strptime(period['start'], '%H:%M'),
            datetime.strptime(period['stop'], '%H:%M')
        ) for period in busy_periods
    ]

    free_windows = []

    current_time = start_time

    while current_time < end_time:
        busy_flag = False

        # Check whether the window falls into busy periods.
        for busy_start, busy_stop in busy_periods:
            if busy_start <= current_time < busy_stop:
                busy_flag = True
                current_time = busy_stop
                break

        # If the flag is busy != True -> add the window to the free_windows list
        if not busy_flag:
            window_end = current_time + timedelta(minutes=30)

            if window_end <= end_time:
                free_windows.append(
                    {
                        'start': current_time.strftime('%H:%M'),
                        'stop': window_end.strftime('%H:%M')
                    }
                )

            current_time += timedelta(minutes=30)

    return free_windows


if __name__ == '__main__':

    start_time = '09:00'
    end_time = '21:00'

    busy_periods = [
        {'start': '10:30', 'stop': '10:50'},
        {'start': '18:40', 'stop': '18:50'},
        {'start': '14:40', 'stop': '15:50'},
        {'start': '16:40', 'stop': '17:20'},
        {'start': '20:05', 'stop': '20:20'},
        {'start': '20:50', 'stop': '21:20'}
    ]

    free_windows = generate_free_windows(start_time, end_time, busy_periods)
    print('Free periods:')
    
    for window in free_windows:
        print(f"{window['start']} - {window['stop']}")
