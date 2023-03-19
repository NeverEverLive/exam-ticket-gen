import logging
import uuid
from fastapi import APIRouter, Query, Depends, Request

from src.components.ticket.schemas import TicketSchema, TicketResponse, TicketsResponse
from src.components.ticket.methods import create_ticket#, get_ticket, get_tickets, update_ticket, delete_ticket
from src.components.authentication.jwt import JWTBearer


router = APIRouter(prefix="/ticket")


@router.post("/", response_model=TicketResponse, status_code=201, dependencies=[Depends(JWTBearer())])
async def create_ticket_endpoint(request: Request, limit: int = Query(default=0), subject_id: uuid.UUID = Query(default=0)):
    return await create_ticket(limit, request.state.user_id, subject_id)

# @router.get("/", response_model=TicketResponse, status_code=200, dependencies=[Depends(JWTBearer())])
# async def get_tickets_endpoint():
#     return await get_tickets()


# @router.get("/detail", response_model=TicketResponse, status_code=200, dependencies=[Depends(JWTBearer())])
# async def get_ticket_endpoint(ticket_id: str = Query(alias="id", default=None)):
#     return await get_ticket(ticket_id)


# @router.put("/", response_model=TicketResponse, status_code=200, dependencies=[Depends(JWTBearer())])
# async def get_ticket_endpoint(ticket: TicketSchema):
#     return await update_ticket(ticket)


# @router.delete("/", response_model=TicketResponse, status_code=202, dependencies=[Depends(JWTBearer())])
# async def get_ticket_endpoint(ticket_id: str = Query(alias="id")):
#     return await delete_ticket(ticket_id)
