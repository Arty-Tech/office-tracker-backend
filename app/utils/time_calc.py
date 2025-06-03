from datetime import datetime, time, timedelta
from typing import List, Tuple

def calculate_hours_for_day(
    date_obj: datetime.date,
    punches: List[Tuple[datetime, bool]],
    workday_configs: List[Tuple[time, time, time, time]]
) -> Tuple[float, float]:
    """
    punches: lista di tuple (timestamp, is_entry) ordinate per timestamp
    workday_configs: per quel giorno della settimana, lista di tuple (start1, end1, start2, end2)
    Ritorna: (ore_ordinarie, ore_extra) in decimale (es. 7.50 = 7h30m)
    """
    # Ricaviamo gli intervalli effettivi di presenza
    intervals = []
    stack = []
    for ts, is_entry in punches:
        if is_entry:
            stack.append(ts)
        else:
            if stack:
                start = stack.pop()
                end = ts
                if end > start:
                    intervals.append((start, end))
    # Intersezione con fasce e calcolo
    ore_ordinarie = timedelta(0)
    ore_totali = timedelta(0)
    # Calcolo ore totali
    for (start, end) in intervals:
        ore_totali += (end - start)
    # Calcolo intersezione con ogni fascia
    for cfg in workday_configs:
        # cfg = (start1, end1, start2, end2)
        start1, end1, start2, end2 = cfg
        for (start, end) in intervals:
            # converto date+time
            cfg_start1 = datetime.combine(date_obj, start1)
            cfg_end1 = datetime.combine(date_obj, end1)
            # fascia1
            inter1_start = max(start, cfg_start1)
            inter1_end = min(end, cfg_end1)
            if inter1_end > inter1_start:
                ore_ordinarie += (inter1_end - inter1_start)
            # fascia2 se esiste
            if start2 and end2:
                cfg_start2 = datetime.combine(date_obj, start2)
                cfg_end2 = datetime.combine(date_obj, end2)
                inter2_start = max(start, cfg_start2)
                inter2_end = min(end, cfg_end2)
                if inter2_end > inter2_start:
                    ore_ordinarie += (inter2_end - inter2_start)
    ore_extra = ore_totali - ore_ordinarie
    # restituisco in ore decimali
    dec_ord = round(ore_ordinarie.total_seconds() / 3600, 2)
    dec_tot = round(ore_totali.total_seconds() / 3600, 2)
    dec_extra = round(ore_extra.total_seconds() / 3600, 2) if ore_extra > timedelta(0) else 0.0
    return dec_ord, dec_extra
