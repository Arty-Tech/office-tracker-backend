from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.api.deps import get_db, get_current_user
from app import crud
from app import schemas
from app.utils.excel import create_monthly_report_excel

router = APIRouter(tags=["reports"], prefix="/reports")


@router.get("/{anno}/{mese}", response_model=schemas.report.ReportMonth)
async def get_report_month(
    anno: int, mese: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    report_data = await crud.report.generate_month_report(db, current_user.id, anno, mese)
    if not report_data:
        raise HTTPException(status_code=404, detail="Nessun dato trovato per il mese richiesto")
    return report_data


@router.get("/{anno}/{mese}/excel")
async def download_report_excel(
    anno: int, mese: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    report_data = await crud.report.generate_month_report(db, current_user.id, anno, mese)
    if not report_data:
        raise HTTPException(status_code=404, detail="Nessun dato trovato per il mese richiesto")

    excel_io = create_monthly_report_excel(
        username=current_user.email,
        anno=anno,
        mese=mese,
        daily_details=report_data["daily_details"],
        summary=report_data["summary"]
    )
    filename = f"report_{current_user.email}_{anno}_{mese:02d}.xlsx"
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    return StreamingResponse(excel_io, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
