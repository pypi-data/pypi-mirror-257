import asyncio
from datetime import datetime, timedelta
from random import choice, randint

from zeep import xsd

from parsec_integration.parsec_integration.core import ParsecCore
from parsec_integration.parsec_integration.dto.dto import VisitorRequest, OrgUnit, Person, PassageRole, ParsecConfigDto
from parsec_integration.parsec_integration.main import Parsec
from faker import Faker
from faker_vehicle import VehicleProvider


def create_parsec():
    """Функция для создания и инициализации сессии"""
    config = {}

    # Создаём объект parsec
    parsec = Parsec("http://192.168.4.198:10101/IntegrationService/IntegrationService.asmx?WSDL")

    # Создаём сессию
    session = parsec.open_session("SYSTEM", "parsec", "parsec")
    session_id = session.Value.SessionID
    return parsec, session_id


# 1
def create_organizations_departments():
    """Функция для создания нескольких Департаментов в Системной организации"""
    faker = Faker()

    parsec, session_id = create_parsec()

    root_org = parsec.get_root_org_unit(session_id)

    for i in range(3):
        dto_org_unit = OrgUnit(NAME=faker.company(),
                               DESC="description",
                               PARENT_ID=root_org.ID)
        org = parsec.create_org_unit(session_id, dto_org_unit)

        dto_person = Person(LAST_NAME=f"{faker.last_name()}",
                            FIRST_NAME=f"{faker.first_name()}",
                            MIDDLE_NAME=f"{faker.prefix_nonbinary()}",
                            ORG_ID=org.Value)
        parsec.create_person(session_id, dto_person)

        dto_visitor = Person(LAST_NAME=f"{faker.last_name()}",
                             FIRST_NAME=f"{faker.first_name()}",
                             MIDDLE_NAME=f"{faker.prefix()}",
                             ORG_ID=org.Value)
        parsec.create_visitor(session_id, dto_visitor)

        faker.add_provider(VehicleProvider)
        auto_dict = Person(LAST_NAME=f"{faker.vehicle_make_model()}",
                           FIRST_NAME=f"{faker.vehicle_category()}",
                           MIDDLE_NAME=f"{faker.vehicle_model()}",
                           ORG_ID=org.Value)
        parsec.create_vehicle(session_id, auto_dict)


# 2
def choose_random_visitor():
    parsec, session_id = create_parsec()

    # Выбираем случайную Организацию(Департамент) и случайного Посетителя
    org_visitors = parsec.get_org_units_hierarchy_with_visitors(session_id)
    random_visitor = choice([i for i in org_visitors if hasattr(i, "FIRST_NAME")])
    org = choice([i for i in org_visitors if hasattr(i, "NAME") and i.ID != random_visitor.ORG_ID])
    return org, random_visitor


# 3
def create_claim():
    """Функция для создания Заявки на посещение"""
    parsec, session_id = create_parsec()

    # Выбираем случайную организацию
    org_visitors = parsec.get_org_units_hierarchy_with_visitors(session_id)
    org = choice([i for i in org_visitors if hasattr(i, "NAME") and i.NAME != "SYSTEM"])

    # Создаем чувака
    visitor = Person(LAST_NAME="Chuvakov", FIRST_NAME="Chuvak", MIDDLE_NAME="Chuvakovich",
                     ORG_ID=org.ID)
    visitor = parsec.create_visitor(session_id, visitor)

    # Создаем заявку
    dto = VisitorRequest.Create(
        PERSON_ID=visitor.Value,
        ORGUNIT_ID=org.ID,
        ADMIT_START=datetime.now(),
        ADMIT_END=datetime.now() + timedelta(days=10)
    )
    vr = parsec.create_visitor_request(session_id, dto)

    # Смотрим что заявка создана
    visitor_request = parsec.get_visitor_request(session_id, vr.ID)
    print(visitor_request)

    # Изменяем заявку
    visitor_request.ADMIT_END = datetime.now() + timedelta(days=100)
    visitor_request.PURPOSE = "Хочет посмотреть"
    svr = parsec.save_visitor_request(session_id, visitor_request)
    print(svr)


# 4
def accept_visitor_request():
    parsec, session_id = create_parsec()

    givr = parsec.get_issued_visitor_requests(session_id)

    givr[0].STATUS = 1
    svr = parsec.save_visitor_request(session_id, givr[0])
    print(svr)


async def test_save_vr():
    config = ParsecConfigDto(
        host="192.168.4.198",
        port=10101,
        login="parsec",
        password="parsec",
        language="ru-RU",
        domain="SYSTEM"
    )
    parsec_core = ParsecCore()
    await parsec_core.init(config)

    upd = await parsec_core.approve_claim(68, "fgffgh", [2, 6])
    print(upd)


async def test_dep():
    config = ParsecConfigDto(
        host="192.168.4.198",
        port=10101,
        login="parsec",
        password="parsec",
        language="ru-RU",
        domain="SYSTEM"
    )
    parsec_core = ParsecCore()
    await parsec_core.init(config)


    de = await parsec_core.delete_department("Church and Sons1")
    print(de)
    # delete_emp = await parsec_core.delete_vehicle("Ford Windstar Cargo", "SUV", "Silverado 1500 HD Crew Cab")
    # print(delete_emp)


# 5
def final():
    parsec, session_id = create_parsec()
    fake = Faker()
    root_org = parsec.get_root_org_unit(session_id)

    # Находим все заявки Главной организации (SYSTEM) и его подразделений со статусом «Согласовано»
    gvr = parsec.get_visitor_requests(session_id, root_org.ID, datetime.now() - timedelta(days=1),
                                      issued=True, accepted=True, declined=False, active=False, completed=False)
    vr = choice(gvr)

    # Находим Расписание (по умолчанию выставлено как Круглосуточное)
    schedule = next(i for i in parsec.get_access_schedules(session_id) if i.NAME == "Круглосуточное")
    # Создаём группу доступа

    ag = parsec.create_access_group(session_id, fake.job(), schedule.ID)

    # Выдаем идентификатор
    # Открываем сессию для редактирования Посетителя
    person_edit_session = parsec.open_person_editing_session(session_id, vr.PERSON_ID)
    print(person_edit_session)

    # Генерим код
    code = hex(randint(900_000_000, 999_999_999))[2:]
    # Создаем маску привелегий
    result = 0
    for i in [2, 6]:  # Пример прохода 2 - роход при блокировке и 6 - Проход при антипассбеке
        result += 2 ** i  # Вычисляем
    mask = str(int(bin(result)[2:]))

    # Наделяем привилегиями данный идентификатор
    sip = parsec.set_identifier_privileges(session_id,
                                           code,
                                           privileges_mask=mask)

    # Ебемся с изменениями идентификатора
    object_type = parsec.client.get_type('ns0:IdentifierTemp')
    object_wrap = xsd.Element('IdentifierTemp', object_type)
    value = object_wrap(CODE=code,
                        PERSON_ID=vr.PERSON_ID,
                        IS_PRIMARY=True,
                        ACCGROUP_ID=ag.Value,
                        PRIVILEGE_MASK=mask,
                        IDENTIFTYPE=0,
                        NAME="FIRST_IDENTIFY")

    add_person_ident = parsec.add_person_identifier(person_edit_session.Value, value)

    gavr = parsec.get_accepted_visitor_requests(session_id)[0]
    print(gavr)

    cvr = parsec.activate_visitor_request(session_id, gavr.ID, code)
    print(cvr)


def create_passage_role():
    """Функция для создания РОЛИ группового прохода"""
    parsec, session_id = create_parsec()

    # Создаём роль прохождения
    dto_role = PassageRole(NAME="Passage role", DESCRIPTION="desc")
    print(parsec.create_passage_role(session_id, dto_role))

    # Смотрим все роли прохождения
    print(parsec.get_passage_roles(session_id))


def test():
    parsec, session_id = create_parsec()
    fake = Faker()
    ag = parsec.get_person_identifiers(session_id, "94b28ffb-83c8-4cc5-97b0-94d9ae16b96a")
    print(ag)
    print(parsec.get_identifier_extra_data(session_id, "36F890EE"))


if __name__ == '__main__':
    # test()

    # create_organizations_departments()
    # create_claim()
    # asyncio.run(test_save_vr())
    asyncio.run(test_dep())
    # accept_visitor_request()
    # final()
