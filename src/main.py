import logging
import uuid
from functools import wraps
import datetime

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from src.models.role import RoleModel
from src.components.subject.schemas import SubjectSchema
from src.components.module.schemas import ModuleSchema
from src.components.question.schemas import QuestionSchema
from src.components.user.schemas import UserSecure, UserLogin, UserSchema
from src.components.subject.methods import get_subjects, get_subject, create_subject
from src.components.module.methods import get_modules_by_subject_id, create_module, get_module
from src.components.question.methods import get_questions_by_module_id, create_question
from src.components.user.methods import login_user, create_user
from src.components.role.methods import get_role
from src.components.ticket.methods import get_ticket_by_subject_id, gen_pdf_file, create_ticket
from src.models.base import get_async_session


router = APIRouter()

templates = Jinja2Templates(directory="./src/frontend/templates")

current_user: UserSecure = None


def user_signed(func):
    @wraps(func)
    async def wrap(request: Request, *args, **kwargs):
        logging.warning(1)
        global current_user
        if not current_user:
            return templates.TemplateResponse("login.html", {"request": request})
        return await func(request, *args, **kwargs)
    return wrap


@router.route("/")
@user_signed
async def get_all_subjects(request: Request):
    subjects = (await get_subjects()).subjects
    global current_user
    return templates.TemplateResponse("index.html", {"request": request, "subjects": subjects, "current_user": current_user})


@router.get("/detail/{subject_id}")
@user_signed
async def get_subject_(request: Request, subject_id: uuid.UUID):
    subject = (await get_subject(subject_id)).subject
    modules = (await get_modules_by_subject_id(subject_id)).modules
    tickets = (await get_ticket_by_subject_id(subject_id)).tickets
    global current_user
    return templates.TemplateResponse("detail.html", {
        "request": request, 
        "subject": subject, 
        "modules": modules,
        "tickets": tickets,
        "current_user": current_user
    })


@router.post("/create_subject")
@user_signed
async def create_subject_(request: Request):
    request_form = await request.form()
    subject_title = request_form["inputTitle"]
    subject_description = request_form["inputDescription"]

    await create_subject(
        SubjectSchema(
            name=subject_title,
            description=subject_description
        )
    )

    return await get_all_subjects(request)


@router.post("/create_module")
@user_signed
async def create_module_(request: Request):
    request_form = await request.form()
    logging.warning(request_form)
    module_title = request_form["inputTitle"]
    module_description = request_form["inputDescription"]
    subject_id = request_form["SubjectID"]

    await create_module(
        ModuleSchema(
            name=module_title,
            description=module_description,
            subject_id=subject_id,
        )
    )

    return await get_subject_(request, subject_id)

@router.get("/detail/module/{module_id}")
@user_signed
async def get_module_(request: Request, module_id: uuid.UUID):
    module = (await get_module(module_id)).module
    questions = (await get_questions_by_module_id(module_id)).questions
    global current_user
    return templates.TemplateResponse("module.html", {
        "request": request, 
        "module": module, 
        "questions": questions,
        "current_user": current_user
    })


@router.post("/create_question")
@user_signed
async def create_question_(request: Request):
    request_form = await request.form()
    question_text = request_form["inputTitle"]
    module_id = request_form["ModuleID"]

    await create_question(
        QuestionSchema(
            text=question_text,
            module_id=module_id,
            user_id=current_user.id,
        )
    )

    return await get_module_(request, module_id)

@router.post("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request, 
    }) 

@router.post("/user/login")
async def login_user_edpoint(request: Request):
    
    request_form = await request.form()

    data = {
        "username": request_form["inputUsername"],
        "password": request_form["inputPassword"]
    }

    global current_user
    user = UserLogin.parse_obj(data)
    current_user = (await login_user(user))[0].user.dict()

    return await get_all_subjects(request)


@router.get("/register")
def get_signin_request_edpoint(request: Request):

    return templates.TemplateResponse("register.html", {
        "request": request, 
    })

@router.post("/register_submit")
async def get_signin_request_edpoint(request: Request):
    request_form = await request.form()

    user = {
        "username": request_form["inputUsername"],
        "first_name": request_form["inputFirstName"],
        "last_name": request_form["inputLastName"],
        "patronymic": request_form["inputPatronymic"],
        "password": request_form["inputPassword"],
        "role_id": (await get_role()).role.id
    }

    await create_user(UserSchema(**user))

    global current_user
    current_user = user

    return await get_all_subjects(request)
    

@router.get("/logout")
async def logout(request: Request):

    global current_user
    current_user = None

    return await login_page(request)


@router.get("/download_file/{ticket_id}")
async def download_file(request: Request, ticket_id: uuid.UUID):

    file_name = str(datetime.datetime.now())

    await gen_pdf_file(ticket_id, file_name)

    return FileResponse(f"pdf/{file_name}.pdf", media_type='application/octet-stream',filename=f"{file_name}.pdf")

@router.post("/generate_ticket/{subject_id}")
async def logout(request: Request, subject_id: uuid.UUID):

    request_form = await request.form()
    limit = int(request_form["countInput"])
    await create_ticket(limit, current_user["id"], subject_id)

    return await get_subject_(request, subject_id)
