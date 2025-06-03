from app.crud.time_entry import crud_time_entry
from app.crud.workday_config import crud_workday_config
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from app.models.time_entry import DayType
from app.utils.time_calc import calculate_hours_for_day
from typing import List, Dict
from uuid import UUID
from sqlalchemy.future import select
from app.models.time_entry import TimeEntry

class CRUDReport:
    async def generate_month_report(
        self, db: AsyncSession, user_id: str, anno: int, mese: int
    ) -> Dict:
        # Recupera tutte le entry del mese
        detail_list = []
        summary = {
            "total_worked_days": 0,
            "total_ore_ordinarie": 0.0,
            "total_ore_extra": 0.0,
            "ferie": 0,
            "permessi": 0,
            "malattia": 0
        }
        # Preleva configurazioni settimanali
        configs = await crud_workday_config.get_by_user(db, user_id)
        cfg_map = {}
        for cfg in configs:
            wd = cfg.weekday
            cfg_map.setdefault(wd, []).append((cfg.start_time_1, cfg.end_time_1, cfg.start_time_2, cfg.end_time_2))
        # Ottieni tutte le days del mese, incluse quelle senza entry
        start_date = date(anno, mese, 1)
        if mese == 12:
            end_date = date(anno + 1, 1, 1)
        else:
            end_date = date(anno, mese + 1, 1)
        # Genera lista di date giorno per giorno
        current = start_date
        delta_day = date(anno, mese, 2) - date(anno, mese, 1)
        # (oppure usare datetime.timedelta)

        while current < end_date:
            # Controlla se esiste TimeEntry per questa data
            result = await db.execute(
                select(TimeEntry).where(
                    TimeEntry.user_id == UUID(user_id),
                    TimeEntry.date == current
                )
            )
            entry = result.scalars().first()
            if entry:
                day_type = entry.day_type.value
                # Ricalcola ore in base a punches
                punch_list = [(p.timestamp, p.is_entry) for p in entry.punches]
                weekday = current.weekday()
                workday_cfgs = cfg_map.get(weekday, [])
                if entry.day_type == DayType.normal:
                    ore_ord, ore_extra = calculate_hours_for_day(current, punch_list, workday_cfgs)
                    summary["total_worked_days"] += 1
                    summary["total_ore_ordinarie"] += ore_ord
                    summary["total_ore_extra"] += ore_extra
                else:
                    ore_ord, ore_extra = 0.0, 0.0
                    summary[entry.day_type.value if entry.day_type.value in summary else entry.day_type.value] += 1
                punches_formatted = "; ".join([
                    f"{p.timestamp.astimezone().strftime('%H:%M')} {'IN' if p.is_entry else 'OUT'}" for p in sorted(entry.punches, key=lambda x: x.timestamp)
                ])
                detail_list.append({
                    "date": current,
                    "day_type": day_type,
                    "punches_formatted": punches_formatted,
                    "ore_ordinarie": ore_ord,
                    "ore_extra": ore_extra,
                    "note": getattr(entry, 'note', "")
                })
            else:
                # Nessuna entry: conta come zero work day (non lavorato)
                detail_list.append({
                    "date": current,
                    "day_type": "",
                    "punches_formatted": "",
                    "ore_ordinarie": 0.0,
                    "ore_extra": 0.0,
                    "note": ""
                })
            from datetime import timedelta
            current = current + timedelta(days=1)
        # Ritorna con formattazione Pydantic-ready (date e floats)
        # Converti date a .isoformat
        for d in detail_list:
            d["date"] = d["date"].isoformat()
        # Arrotonda i totali
        summary["total_ore_ordinarie"] = round(summary["total_ore_ordinarie"], 2)
        summary["total_ore_extra"] = round(summary["total_ore_extra"], 2)
        return {"daily_details": detail_list, "summary": summary}

crud_report = CRUDReport()