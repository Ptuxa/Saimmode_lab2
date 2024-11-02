class ActivityInfo:
    def __init__(self, start_time, end_time, activity_count, typeValue):
        self.start_time = start_time
        self.end_time = end_time
        self.activity_count = activity_count
        self.typeValue = typeValue


class ActivityInfoStatistics:
    def __init__(self):
        self.activities_statistics = []
        self.strings = []

    def append_acivities_statistics(self, new_start, new_end, activity_increment, new_type):
        self.strings.append(f"\t{new_start:.2f}\t{new_end:.2f}\t{activity_increment:.2f}\t{new_type:.2f}")

        new_intervals = []
        inserted = False

        for activity in self.activities_statistics:
            # Если новый интервал полностью до или после текущего - добавляем его как есть
            if new_end <= activity.start_time:
                if not inserted:
                    new_intervals.append(ActivityInfo(new_start, new_end, activity_increment, new_type))
                    inserted = True
                new_intervals.append(activity)
            elif new_start >= activity.end_time:
                new_intervals.append(activity)
            else:
                # Разделяем текущий интервал с учётом приоритета типа
                if activity.start_time < new_start:
                    new_intervals.append(ActivityInfo(activity.start_time, new_start, activity.activity_count, activity.typeValue))
                
                overlap_start = max(activity.start_time, new_start)
                overlap_end = min(activity.end_time, new_end)
                combined_activity_count = activity.activity_count + activity_increment
                combined_type = min(activity.typeValue, new_type)  # Приоритет для меньшего типа

                new_intervals.append(ActivityInfo(overlap_start, overlap_end, combined_activity_count, combined_type))
                
                # Обрабатываем правую часть текущего интервала, если она остаётся
                if activity.end_time > new_end:
                    new_intervals.append(ActivityInfo(new_end, activity.end_time, activity.activity_count, activity.typeValue))
                    inserted = True
                elif new_start < activity.end_time:
                    new_start = activity.end_time

        # Добавляем оставшийся новый интервал, если он ещё не вставлен
        if not inserted:
            new_intervals.append(ActivityInfo(new_start, new_end, activity_increment, new_type))                    

        # Обновляем список активностей
        self.activities_statistics = new_intervals
        
        self.consolidate_intervals()

    def consolidate_intervals(self):
        # Инициализируем список для объединенных интервалов
        consolidated_intervals = []
        
        # Проходим по каждому интервалу и объединяем с последним, если тип и активность совпадают
        for interval in self.activities_statistics:
            if consolidated_intervals:
                last_interval = consolidated_intervals[-1]
                # Проверяем, что активности и типы совпадают
                if (last_interval.activity_count == interval.activity_count and
                        (last_interval.typeValue in [1, 2]) and (interval.typeValue in [1,2])):
                    last_interval.end_time = interval.end_time  # Обновляем конец последнего интервала
                    last_interval.typeValue = min(last_interval.typeValue, interval.typeValue)
                else:
                    consolidated_intervals.append(interval)
            else:
                consolidated_intervals.append(interval)
        
        # Обновляем основное хранилище слияния
        self.activities_statistics = consolidated_intervals

    def average(self, time_limit):
        activities_statistics_total = 0 
        time_summary = 0 
        for item in self.activities_statistics:
            count = item.activity_count
            time = item.end_time - item.start_time
            time_summary = time_summary + time 
            activities_statistics_total = activities_statistics_total + (item.activity_count * (item.end_time - item.start_time))
            
        

        return activities_statistics_total / (time_limit)

    def show_activity_info(self):      
        print()
        for item1 in self.strings:
            print(item1)
        print()

        print("start\tend\tactivity\ttypeValue")
        for item in self.activities_statistics:            
            print(f"{item.start_time:.2f}\t{item.end_time:.2f}\t{item.activity_count:.2f}\t\t{item.typeValue:.2f}")

        print()
