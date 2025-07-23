from datetime import datetime, timedelta
from decimal import Decimal
from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload

from ..core import security
from ..db import database, models
from ..models import schemas

router = APIRouter()

@router.get(
    "/profile/comprehensive",
    # O response_model pode ser complexo, vamos montá-lo manualmente por enquanto
    # para incluir o 'activity_calendar', mas o ideal seria ter um schema completo.
    tags=["Profile"],
)
def get_comprehensive_profile(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    """
    Busca e calcula um perfil de dados abrangente para o usuário autenticado,
    incluindo estatísticas de todos os tempos, performance mensal, conquistas e mais.
    """
    # 1. Buscar todos os dados relevantes do usuário de uma vez para otimizar
    all_transactions = (
        db.query(models.Transaction)
        .options(selectinload(models.Transaction.category)) # Otimiza o carregamento da categoria
        .filter(models.Transaction.user_id == current_user.id)
        .all()
    )
    all_work_sessions = (
        db.query(models.WorkSession)
        .filter(models.WorkSession.user_id == current_user.id)
        .all()
    )

    # 2. Calcular Estatísticas Gerais
    income_transactions = [t for t in all_transactions if t.type == "income"]
    expense_transactions = [t for t in all_transactions if t.type == "expense"]

    total_earnings = sum(t.amount for t in income_transactions)
    total_expenses = sum(t.amount for t in expense_transactions)
    total_trips = len(income_transactions)
    total_minutes = sum(ws.total_minutes or 0 for ws in all_work_sessions)
    total_hours = round(total_minutes / 60)

    # 3. Calcular Performance Mensal (últimos 12 meses)
    monthly_stats = []
    now = datetime.utcnow()
    for i in range(12):
        month_start = (now.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        month_end_year = month_start.year
        month_end_month = month_start.month
        if month_end_month == 12:
            month_end_year += 1
            month_end_month = 1
        else:
            month_end_month += 1
        month_end = datetime(month_end_year, month_end_month, 1) - timedelta(seconds=1)

        month_tx = [
            t for t in all_transactions if month_start <= t.date <= month_end
        ]
        month_income = sum(t.amount for t in month_tx if t.type == "income")
        month_expenses = sum(t.amount for t in month_tx if t.type == "expense")
        month_trips = len([t for t in month_tx if t.type == "income"])

        monthly_stats.append(
            schemas.MonthlyPerformance(
                month=month_start.strftime("%b/%Y"),
                income=month_income,
                expenses=month_expenses,
                profit=month_income - month_expenses,
                trips=month_trips,
            )
        )
    monthly_stats.reverse() # para mostrar do mais antigo ao mais recente
    
    best_month = max(monthly_stats, key=lambda m: m.income, default=None)
    monthly_average = sum(m.income for m in monthly_stats) / len(monthly_stats) if monthly_stats else Decimal(0)

    # 4. Detalhamento por Plataforma
    platform_stats = defaultdict(lambda: {"earnings": Decimal(0), "trips": 0})
    for t in income_transactions:
        platform_name = t.category.name if t.category else "Outros"
        platform_stats[platform_name]["earnings"] += t.amount
        platform_stats[platform_name]["trips"] += 1

    platform_breakdown = [
        schemas.PlatformBreakdown(
            name=name,
            earnings=stats["earnings"],
            trips=stats["trips"],
            percentage=round((stats["earnings"] / total_earnings) * 100, 2) if total_earnings > 0 else 0,
        )
        for name, stats in platform_stats.items()
    ]
    
    # 5. Calcular Conquistas
    achievements_data = [
        {"id": 1, "title": "Primeira Centena", "desc": "Complete 100 corridas", "goal": 100, "value": total_trips},
        {"id": 2, "title": "Estrela de Ouro", "desc": "Alcance R$ 1.000 em ganhos", "goal": 1000, "value": total_earnings},
        {"id": 3, "title": "Maratonista", "desc": "Trabalhe 100+ horas", "goal": 100, "value": total_hours},
        {"id": 4, "title": "Especialista", "desc": "Complete 500 corridas", "goal": 500, "value": total_trips},
    ]
    achievements = [
        schemas.Achievement(
            id=a["id"],
            title=a["title"],
            description=a["desc"],
            achieved=a["value"] >= a["goal"],
            progress=min((float(a["value"]) / a["goal"]) * 100, 100),
            goal=a["goal"]
        ) for a in achievements_data
    ]

    # 6. Montar a resposta final
    final_stats = schemas.ProfileStats(
        total_trips=total_trips,
        total_earnings=total_earnings,
        total_expenses=total_expenses,
        net_profit=total_earnings - total_expenses,
        total_hours=total_hours,
        average_per_trip=total_earnings / total_trips if total_trips > 0 else Decimal(0),
        average_per_hour=total_earnings / (total_minutes / 60) if total_minutes > 0 else Decimal(0),
        best_month_earnings=best_month.income if best_month else Decimal(0),
        monthly_average_earnings=monthly_average,
    )

    # O 'personal_info' é o schema User que já definimos
    personal_info = schemas.User.model_validate(current_user)
    # Simulação do status do plano
    personal_info.plan_status = "active" if current_user.is_paid else "inactive"


    return {
        "personal_info": personal_info,
        "stats": final_stats,
        "monthly_performance": monthly_stats,
        "platform_breakdown": platform_breakdown,
        "achievements": achievements,
        # Adicione aqui outros dados mockados como no original, se necessário
        # "preferences": {...},
        # "security": {...},
    }