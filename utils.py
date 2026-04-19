from typing import List, Dict, Tuple

def classify_subject(mark: float) -> str:
    if mark < 50:
        return 'Weak'
    elif mark < 75:
        return 'Moderate'
    else:
        return 'Strong'


def analyse_subjects(subjects: List[Dict]) -> List[Dict]:
    diff_multiplier = {'Easy': 0.9, 'Medium': 1.2, 'Hard': 1.6}
    result = []

    for sub in subjects:
        mark = float(sub['mark'])
        difficulty = sub.get('difficulty', 'Medium')
        classification = classify_subject(mark)

        base_weight = (100 - mark) / 100
        base_weight = max(base_weight, 0.15)

        weight = base_weight * diff_multiplier.get(difficulty, 1.0)

        result.append({
            'name': sub['name'],
            'mark': mark,
            'difficulty': difficulty,
            'classification': classification,
            'weight': weight
        })

    return result


def allocate_study_time(subjects: List[Dict], total_hours: float) -> List[Dict]:
    total_weight = sum(s['weight'] for s in subjects)
    result = []

    for s in subjects:
        proportion = s['weight'] / total_weight
        allocated = round(total_hours * proportion, 2)

        hours_part = int(allocated)
        minutes_part = int((allocated - hours_part) * 60)

        result.append({
            **s,
            'allocated_hours': allocated,
            'time_display': f"{hours_part}h {minutes_part}m"
        })

    result.sort(key=lambda x: x['mark'])
    return result


def generate_timetable(subjects_with_time: List[Dict], start_hour: int = 18) -> List[Dict]:
    timetable = []
    current_minutes = start_hour * 60

    for sub in subjects_with_time:
        duration_minutes = round(sub['allocated_hours'] * 60)

        start_h = current_minutes // 60
        start_m = current_minutes % 60

        end_minutes = current_minutes + duration_minutes
        end_h = end_minutes // 60
        end_m = end_minutes % 60

        timetable.append({
            'subject': sub['name'],
            'classification': sub['classification'],
            'difficulty': sub['difficulty'],
            'start': f"{start_h:02d}:{start_m:02d}",
            'end': f"{end_h:02d}:{end_m:02d}",
            'duration': sub['time_display'],
            'allocated_hours': sub['allocated_hours']
        })

        current_minutes = end_minutes + 10

    return timetable


def generate_recommendations(performance_category: str, subjects: List[Dict],
                             hours_studied: float, sleep_hours: float,
                             attendance_percent: float) -> List[str]:

    recs = []

    if performance_category == 'At Risk':
        recs.append("Overall performance is at risk. Immediate improvement needed.")
    elif performance_category == 'Average':
        recs.append("Overall performance is moderate. Improvement is possible.")
    else:
        recs.append("Overall performance is good. Maintain consistency.")

    for s in subjects:
        if s['classification'] == 'Weak':
            recs.append(f"{s['name']}: Focus on basics and increase practice time.")
        elif s['classification'] == 'Moderate':
            recs.append(f"{s['name']}: Revise concepts and solve more problems.")
        else:
            recs.append(f"{s['name']}: Continue regular revision.")

    if hours_studied < 2:
        recs.append("Increase total study time to at least 4 hours.")

    if sleep_hours < 6:
        recs.append("Maintain proper sleep cycle (7–8 hours).")

    if attendance_percent < 65:
        recs.append("Improve attendance for better academic performance.")

    return recs


def validate_inputs(attendance: float, hours: float, sleep: float,
                    subjects: List[Dict]) -> Tuple[bool, str]:

    if not (0 <= attendance <= 100):
        return False, "Attendance must be between 0 and 100."

    if not (0 < hours <= 16):
        return False, "Study hours must be between 0 and 16."

    if not (0 < sleep <= 12):
        return False, "Sleep hours must be between 0 and 12."

    if len(subjects) == 0:
        return False, "Add at least one subject."

    return True, ""


def compute_average_previous_score(subjects: List[Dict]) -> float:
    marks = [float(s['mark']) for s in subjects]
    return round(sum(marks) / len(marks), 2) if marks else 0.0