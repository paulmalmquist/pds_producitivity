from fastapi import APIRouter, Query

from models.email import EmailSearchResponse

router = APIRouter()


@router.get('/search')
def search_email(q: str = Query(..., description='Search term')) -> list[EmailSearchResponse]:
    return [
        EmailSearchResponse(
            thread_id='abc123',
            subject='Northwind kickoff agenda',
            sender='sponsor@jll.com',
            snippet='Attached is the kickoff agenda for review.'
        ),
        EmailSearchResponse(
            thread_id='def456',
            subject='Variance review notes',
            sender='pm@jll.com',
            snippet='Variance trending 5% above plan, see Tableau view.'
        ),
    ]
