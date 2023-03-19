import datetime
import logging
import itertools as it
import random
import uuid
from pydantic import parse_obj_as
from sqlalchemy import select, update, delete, distinct, func
import pdfkit
import jinja2

from src.models.base import get_async_session
from src.models.ticket import TicketModel
from src.models.module import ModuleModel
from src.models.subject import SubjectModel
from src.models.question import QuestionModel
from src.models.ticket_question import TicketQuestionModel
from src.components.ticket.schemas import TicketSchema, TicketQuestionSchema, TicketResponse, TicketsResponse


async def create_ticket(limit: int, user_id: uuid.UUID, subject_id: uuid.UUID) -> TicketResponse:
    question_state = select(
        QuestionModel
    ).join(
        ModuleModel,
        ModuleModel.id == QuestionModel.module_id
    ).join(
        SubjectModel,
        SubjectModel.id == ModuleModel.subject_id
    ).where(
        QuestionModel.user_id == user_id,
        SubjectModel.id == subject_id
    )

    logging.warning(user_id)


    async with get_async_session() as session:
        logging.warning(list(it.chain(*await session.execute(question_state))))
        questions: list[QuestionModel] = it.chain(*await session.execute(question_state))
        questions_id = []
        questions_probability = []
        for question in  questions:
            questions_id.append(question.id)
            questions_probability.append(question.probability)

    if len(questions_id) < limit:
        limit = len(questions_id)

    choices_questions = []
    changed_probability = []
    questions_id_copy = questions_id.copy()
    questions_probability_copy = questions_probability.copy()
    while len(choices_questions) < limit:
        choices_questions.extend(random.choices(questions_id_copy, weights=questions_probability_copy, k=1))
        index = questions_id_copy.index(choices_questions[-1])
        changed_probability.append(questions_probability_copy[index] * 0.95)
        del questions_id_copy[index]
        del questions_probability_copy[index]

    logging.warning(changed_probability)

    ticket = TicketSchema(
        user_id=user_id,
        title=str(datetime.datetime.now())
    )

    ticket_state = TicketModel().fill(**ticket.dict())

    ticket_question_states = []
    for question_id in choices_questions:
        ticket_question_states.append(
            TicketQuestionModel().fill(
                **TicketQuestionSchema(
                    ticket_id=ticket.id,
                    question_id=question_id,
                ).dict()
            )
        )

    async with get_async_session() as session:
        session.add(ticket_state)
        for index, state in enumerate(ticket_question_states):
            session.add(state)
            await session.execute(
                update(
                    QuestionModel
                ).where(
                    QuestionModel.id.in_(questions_id)
                ).values(
                    probability=changed_probability[index] 
                )
            )
        await session.commit()

    return TicketResponse(
        ticket=ticket,
        message="Ticket successfully created",
        success=True
    )


async def get_ticket_by_subject_id(subject_id: uuid.UUID):
    ticket_state = select(
        TicketModel
    ).join(
        TicketQuestionModel,
        TicketQuestionModel.ticket_id == TicketModel.id
    ).join(
        QuestionModel,
        QuestionModel.id == TicketQuestionModel.question_id
    ).join(
        ModuleModel,
        ModuleModel.id == QuestionModel.module_id
    ).join(
        SubjectModel,
        SubjectModel.id == ModuleModel.subject_id
    ).where(
        SubjectModel.id == subject_id
    )

    async with get_async_session() as session:
        return TicketsResponse(
            tickets=parse_obj_as(list[TicketSchema], set((await session.execute(ticket_state)).scalars())),
            message="Tickets collected",
            success=True
        )


async def gen_pdf_file(ticket_id, file_name):
    template_loader = jinja2.FileSystemLoader("./src")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("base_pdf.html")
    ticket_state = select(
        TicketModel.title,
        SubjectModel.name,
        func.array_agg(QuestionModel.text.distinct()),
    ).join(
        TicketQuestionModel,
        TicketQuestionModel.ticket_id == TicketModel.id
    ).join(
        QuestionModel,
        QuestionModel.id == TicketQuestionModel.question_id
    ).join(
        ModuleModel,
        ModuleModel.id == QuestionModel.module_id
    ).join(
        SubjectModel,
        SubjectModel.id == ModuleModel.subject_id
    ).where(
        TicketModel.id == ticket_id
    ).group_by(
        TicketModel.title,
        SubjectModel.name
    )

    async with get_async_session() as session:
        logging.warning((await session.execute(ticket_state)).fetchone())
        title, name, questions = (await session.execute(ticket_state)).fetchone()
    question_string = "\n".join([f'<li style="text-align: left;">{question}</li>' for question in questions])

    context = {
        "ticket_title": title,
        "subject_title": name,
        "question_string": question_string,
    }

    # <li style="text-align: left;">{{item3}}</li>
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_string(output_text, f'pdf/{file_name}.pdf', configuration=config, css='style.css')
