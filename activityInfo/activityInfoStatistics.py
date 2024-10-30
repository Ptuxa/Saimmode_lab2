class ActivityInfo:
    def __init__(self, start_time, end_time, activity_count):
        self.start_time = start_time
        self.end_time = end_time
        self.activity_count = activity_count

class ActivityInfoStatistics:
    def __init__(self):
        self.activities_statistics = []
        self.strings = []

    def append_acivities_statistics(self, new_start, new_end, activity_increment):
        self.strings.append(f"\t\t\t\t{new_start:.2f}\t{new_end:.2f}\t{activity_increment:.2f}")
        
        new_intervals = []
        inserted = False

        for activity in self.activities_statistics:
            # Если новый интервал полностью до или после текущего - добавляем его как есть
            if new_end <= activity.start_time:
                if not inserted:
                    new_intervals.append(ActivityInfo(new_start, new_end, activity_increment))
                    inserted = True
                new_intervals.append(activity)
            elif new_start >= activity.end_time:
                new_intervals.append(activity)
            else:
                # Если пересекается - разделяем текущий интервал
                if activity.start_time < new_start:
                    new_intervals.append(ActivityInfo(activity.start_time, new_start, activity.activity_count))
                overlap_start = max(activity.start_time, new_start)
                overlap_end = min(activity.end_time, new_end)
                new_intervals.append(ActivityInfo(overlap_start, overlap_end, activity.activity_count + activity_increment))
                
                # Обрабатываем правую часть текущего интервала, если она остаётся
                if activity.end_time > new_end:
                    new_intervals.append(ActivityInfo(new_end, activity.end_time, activity.activity_count))
                    inserted = True
                elif new_start < activity.end_time:
                    new_start = activity.end_time

        # Добавляем оставшийся новый интервал, если он еще не вставлен
        if not inserted:
            new_intervals.append(ActivityInfo(new_start, new_end, activity_increment))

        # Обновляем список активностей
        self.activities_statistics = new_intervals

    def consolidate_intervals(self):
        merged_intervals = []
        for activity in self.activities_statistics:
            # Объединение только при совпадении активности
            if merged_intervals and merged_intervals[-1].end_time == activity.start_time and \
                merged_intervals[-1].activity_count == activity.activity_count:
                merged_intervals[-1].end_time = activity.end_time
            else:
                merged_intervals.append(activity)

        self.activities_statistics = merged_intervals

    def average(self):
        activities_statistics_total = sum(item.activity_count for item in self.activities_statistics)

        if len(self.activities_statistics) == 0:
            return None    

        return activities_statistics_total / len(self.activities_statistics)

    def show_activity_info(self):      
        print()
        for item1 in self.strings:
            print(item1)
        print()

        print("start\tend\tactivity")
        for item in self.activities_statistics:            
            print(f"{item.start_time:.2f}\t{item.end_time:.2f}\t{item.activity_count:.2f}")

        print()
