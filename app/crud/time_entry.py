from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.time_entry import TimeEntry, DayType
from app.models.punch import Punch
from app.schemas.time_entry import TimeEntryCreate, PunchCreate, TimeEntryRead
from app.crud.workday_config import crud_workday_config
from app.utils.time_calc import calculate_hours_for_day
from datetime import datetime, date, time
from uuid import UUID
from typing import List, Dict

class CRUDTimeEntry:
    async def get_month_entries(
        self, db: AsyncSession, user_id: str, anno: int, mese: int
    ) -> List[Dict]:
        # Recupera tutte le time entry per il mese specificato
        start_date = date(anno, mese, 1)
        if mese == 12:
            end_date = date(anno + 1, 1, 1)
        else:
            end_date = date(anno, mese + 1, 1)
        result = await db.execute(
            select(TimeEntry)
            .where(
                TimeEntry.user_id == UUID(user_id),
                TimeEntry.date >= start_date,
                TimeEntry.date < end_date
            )
            .options(
                # carica relationship Punch
            )
        )
        entries = result.scalars().all()
        # Costruisci lista di dict con campi e calcoli
        detail_list = []
        # Preleva configurazioni settimanali
        configs = await crud_workday_config.get_by_user(db, user_id)
        cfg_map = {}
        for cfg in configs:
            wd = cfg.weekday
            cfg_map.setdefault(wd, []).append((cfg.start_time_1, cfg.end_time_1, cfg.start_time_2, cfg.end_time_2))
        for entry in entries:
            # Trasforma punches in lista di tuple (timestamp, is_entry)
            punch_list = [(p.timestamp, p.is_entry) for p in entry.punches]
            weekday = entry.date.weekday()  # 0=Mon..6=Sun
            workday_cfgs = cfg_map.get(weekday, [])
            if entry.day_type == DayType.normal:
                ore_ord, ore_extra = calculate_hours_for_day(entry.date, punch_list, workday_cfgs)
            else:
                ore_ord, ore_extra = 0.0, 0.0
            punches_formatted = "; ".join([
                f"{p.timestamp.astimezone().strftime('%H:%M')} {'IN' if p.is_entry else 'OUT'}" for p in sorted(entry.punches, key=lambda x: x.timestamp)
            ])
            detail_list.append({
                "date": entry.date.isoformat(),
                "day_type": entry.day_type.value,
                "punches": [
                    {"timestamp": p.timestamp.isoformat(), "is_entry": p.is_entry} for p in entry.punches
                ],
                "ore_ordinarie": ore_ord,
                "ore_extra": ore_extra,
                "punches_formatted": punches_formatted,
                "note": getattr(entry, 'note', "")
            })
        return detail_list

    async def create_or_update_day(
        self, db: AsyncSession, user_id: str, te_in: TimeEntryCreate
    ) -> Dict:
        # Cerca se esiste record per data
        result = await db.execute(
            select(TimeEntry).where(
                TimeEntry.user_id == UUID(user_id),
                TimeEntry.date == te_in.date
            )
        )
        entry = result.scalars().first()
        if entry:
            # Aggiorna day_type, elimina punches esistenti
            entry.day_type = te_in.day_type
            # Cancella punches passate
            for p in entry.punches:
                await db.delete(p)
            await db.flush()
        else:
            entry = TimeEntry(
                user_id=UUID(user_id),
                date=te_in.date,
                day_type=te_in.day_type
            )
            db.add(entry)
            await db.flush()
        # Se normal, crea punches
        if te_in.day_type == DayType.normal:
            for punch_data in te_in.punches:
                # punch_data ha forma {"in": "HH:MM", "out": "HH:MM"}
                in_time_str = punch_data.in_time
                out_time_str = punch_data.out_time
                in_dt = datetime.combine(te_in.date, time.fromisoformat(in_time_str))
                out_dt = datetime.combine(te_in.date, time.fromisoformat(out_time_str))
                punch_in = Punch(time_entry_id=entry.id, is_entry=True, timestamp=in_dt)
                punch_out = Punch(time_entry_id=entry.id, is_entry=False, timestamp=out_dt)
                db.add(punch_in)
                db.add(punch_out)
        await db.commit()
        await db.refresh(entry)
        # Ricalcola e ritorna come create_month_entries un singolo elemento
        month_entries = await self.get_month_entries(db, user_id, te_in.date.year, te_in.date.month)
        for detail in month_entries:
            if detail['date'] == te_in.date.isoformat():
                return detail
        return {}

    async def delete_day(self, db: AsyncSession, user_id: str, date_str: str) -> None:
        te_date = date.fromisoformat(date_str)
        result = await db.execute(
            select(TimeEntry).where(
                TimeEntry.user_id == UUID(user_id),
                TimeEntry.date == te_date
            )
        )
        entry = result.scalars().first()
        if entry:
            await db.delete(entry)
            await db.commit()

crud_time_entry = CRUDTimeEntry()
