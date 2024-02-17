from datetime import datetime
from random import randint

from zeep import xsd

from parsec_integration.parsec_integration.dto.dto import ParsecConfigDto, ParsecSystemInfo, OrgUnit, Person, VisitorRequest, Guid, \
    ClaimStatus, Identifier, BasePerson, BaseOrgUnit
from parsec_integration.parsec_integration.errors import ParsecIntegrationError
from parsec_integration.parsec_integration.main import Parsec


class ParsecCore:

    async def init(self, config: ParsecConfigDto, locale=False):
        self.system_info: ParsecSystemInfo = ParsecSystemInfo()
        self.config = config
        self.core = Parsec(f"http://{self.config.host}:{self.config.port}"
                           f"/IntegrationService/IntegrationService.asmx?WSDL")
        self.session = None
        self.session_id = None
        await self._get_version()
        await self._get_domains()
        await self._open_session(locale)

    async def _get_version(self):
        self.system_info.version = self.core.get_version()

    async def _get_domains(self):
        self.system_info.domains = self.core.get_domains()

    async def _open_session(self, locale):
        if locale:
            result = (self.core.open_session(self.config.domain, self.config.login, self.config.password,
                                             self.config.language)).Value
            if not result:
                raise Exception("OpenSessionWithInLocale error")
        result = (self.core.open_session(self.config.domain, self.config.login, self.config.password)).Value
        self.session = result
        self.session_id = self.session.SessionID

    # ---------------------Department, Employer, Visitor, Vehicle-----------------------

    async def create_department(self, dto: BaseOrgUnit.Create, organization_name: str):
        all_org = [org for org in self.core.get_org_units_hierarchy(self.session_id) if org.PARENT_ID is None]
        for org in all_org:
            if org.NAME == organization_name:
                org_dto = OrgUnit.Create(NAME=dto.NAME,
                                         DESC=dto.DESC,
                                         PARENT_ID=org.ID)
                return self.core.create_org_unit(self.session_id, org_dto)
        else:
            raise ParsecIntegrationError(f"Organization with name: {organization_name} not found")

    async def update_department(self, department_name: str, dto: BaseOrgUnit.Update):
        try:
            dep = next(org for org in self.core.get_org_units_hierarchy(self.session_id) if org.NAME == department_name)
            edit_session_id = (self.core.open_org_unit_editing_session(self.session_id, dep.ID)).Value
            if dto.NAME:
                dep.NAME = dto.NAME
            if dto.DESC:
                dep.DESC = dto.DESC
            return self.core.save_org_unit(edit_session_id, dep)
        except StopIteration:
            print(f"Department with name: {department_name} not found")

    async def delete_department(self, department_name: str):  # TODO Какого то хрена не работает
        for org in self.core.get_org_units_hierarchy(self.session_id):
            if org.NAME == department_name:
                return self.core.delete_org_unit(self.session_id, org.ID)
        else:
            raise ParsecIntegrationError(f"Department with name: {department_name} not found")

    async def create_employer(self, dto: BasePerson, department_name: str):
        all_org = self.core.get_org_units_hierarchy(self.session_id)
        for org in all_org:
            if org.NAME == department_name:
                person_dto = Person(
                    LAST_NAME=dto.LAST_NAME,
                    FIRST_NAME=dto.FIRST_NAME,
                    MIDDLE_NAME=dto.MIDDLE_NAME,
                    TAB_NUM=dto.TAB_NUM,
                    ORG_ID=org.ID
                )
                return self.core.create_person(self.session_id, person_dto)
        else:
            raise ParsecIntegrationError(f"Department with name: {department_name} not found")

    async def delete_employer(self, last_name: str = None, first_name: str = None, middle_name: str = None):
        employers = [i for i in self.core.get_org_units_hierarchy_with_persons(self.session_id)
                     if hasattr(i, "FIRST_NAME")]
        for employer in employers:
            if employer.FIRST_NAME == first_name and employer.LAST_NAME == last_name \
                    and employer.MIDDLE_NAME == middle_name:
                return self.core.delete_person(self.session_id, employer.ID)
        else:
            raise ParsecIntegrationError(f"Employer with last_name: {last_name}, "
                                         f"first_name: {first_name}, "
                                         f"middle_name: {middle_name} not found")

    async def create_visitor(self, dto: BasePerson, department_name: str):
        all_org = self.core.get_org_units_hierarchy(self.session_id)
        for org in all_org:
            if org.NAME == department_name:
                person_dto = Person(
                    LAST_NAME=dto.LAST_NAME,
                    FIRST_NAME=dto.FIRST_NAME,
                    MIDDLE_NAME=dto.MIDDLE_NAME,
                    TAB_NUM=dto.TAB_NUM,
                    ORG_ID=org.ID
                )
                return self.core.create_visitor(self.session_id, person_dto)
        else:
            raise ParsecIntegrationError(f"Department with name: {department_name} not found")

    async def delete_visitor(self, last_name: str = None, first_name: str = None, middle_name: str = None):
        visitors = [i for i in self.core.get_org_units_hierarchy_with_visitors(self.session_id)
                    if hasattr(i, "FIRST_NAME")]
        for visitor in visitors:
            if visitor.FIRST_NAME == first_name and visitor.LAST_NAME == last_name \
                    and visitor.MIDDLE_NAME == middle_name:
                return self.core.delete_person(self.session_id, visitor.ID)
        else:
            raise ParsecIntegrationError(f"Visitor with last_name: {last_name}, "
                                         f"first_name: {first_name}, "
                                         f"middle_name: {middle_name} not found")

    async def create_vehicle(self, dto: BasePerson, department_name: str):
        all_org = self.core.get_org_units_hierarchy(self.session_id)
        for org in all_org:
            if org.NAME == department_name:
                person_dto = Person(
                    LAST_NAME=dto.LAST_NAME,
                    FIRST_NAME=dto.FIRST_NAME,
                    MIDDLE_NAME=dto.MIDDLE_NAME,
                    TAB_NUM=dto.TAB_NUM,
                    ORG_ID=org.ID
                )
                return self.core.create_vehicle(self.session_id, person_dto)
        else:
            raise ParsecIntegrationError(f"Department with name: {department_name} not found")

    async def delete_vehicle(self, number: str = None, model: str = None, color: str = None):
        vehicles = [i for i in self.core.get_org_units_hierarchy_with_vehicle(self.session_id)
                    if hasattr(i, "FIRST_NAME")]
        for vehicle in vehicles:
            if vehicle.FIRST_NAME == model and vehicle.LAST_NAME == number \
                    and vehicle.MIDDLE_NAME == color:
                return self.core.delete_person(self.session_id, vehicle.ID)
        else:
            raise ParsecIntegrationError(f"Vehicle with number: {number}, "
                                         f"model: {model}, "
                                         f"color: {color} not found")

    # -------------------------Claims-------------------------------

    async def get_claim_accepted(self, claim_id: int):
        return self.core.find_visitor_request(self.session_id, claim_id)

    async def get_claims(self, accepted: bool):
        if accepted:
            return self.core.get_accepted_visitor_requests(self.session_id)
        return self.core.get_issued_visitor_requests(self.session_id)

    async def get_claims_in_department(self, department_name: str, date_time_from: datetime, status: ClaimStatus):
        all_org_units = self.core.get_org_units_hierarchy(self.session_id)
        org_unit_id: Guid = ""
        for org in all_org_units:
            if org.NAME == department_name:
                org_unit_id = org.ID
        if not org_unit_id:
            raise ParsecIntegrationError(f"Department with name {department_name} not found")
        return self.core.get_visitor_requests(self.session_id, org_unit_id, date_time_from, **dict(status))

    async def create_claim(self, dto: VisitorRequest.Create):
        return self.core.create_visitor_request(self.session_id, dto)

    async def update_not_approved_claim(self, claim_id: int, dto: VisitorRequest.Update):
        claims_not_approved = self.core.get_issued_visitor_requests(self.session_id)
        for claim in claims_not_approved:
            if claim.NUMBER == claim_id and claim.STATUS == 0:
                if dto.PERSON_INFO:
                    claim.PERSON_INFO = dto.PERSON_INFO
                if dto.PURPOSE:
                    claim.PURPOSE = dto.PURPOSE
                if dto.ADMIT_START:
                    claim.ADMIT_START = dto.ADMIT_START
                if dto.ADMIT_END:
                    claim.ADMIT_END = dto.ADMIT_END
                return self.core.save_visitor_request(self.session_id, claim)
        else:
            raise ParsecIntegrationError(f"Claim with id: {claim_id} not found")

    async def update_approved_claim(self, claim_id: int, dto: VisitorRequest.Update):
        claims_approved = self.core.get_accepted_visitor_requests(self.session_id)
        for claim in claims_approved:
            if claim.NUMBER == claim_id and claim.STATUS == 1:
                if dto.PERSON_INFO:
                    claim.PERSON_INFO = dto.PERSON_INFO
                if dto.PURPOSE:
                    claim.PURPOSE = dto.PURPOSE
                if dto.ADMIT_START:
                    claim.ADMIT_START = dto.ADMIT_START
                if dto.ADMIT_END:
                    claim.ADMIT_END = dto.ADMIT_END
                return self.core.save_visitor_request(self.session_id, claim)
        else:
            raise ParsecIntegrationError(f"Claim with id: {claim_id} not found")

    async def approve_claim(self, claim_id: int, access_group_name: str, privileges: list[int]):
        claims_not_approved = self.core.get_issued_visitor_requests(self.session_id)
        for claim in claims_not_approved:
            if claim.NUMBER == claim_id and claim.STATUS == 0:
                # approve claim
                claim.STATUS = 1
                self.core.save_visitor_request(self.session_id, claim)
                # create pass
                person_edit_session = self.core.open_person_editing_session(self.session_id, claim.PERSON_ID)
                # Добываем расписание, по умолчанию есть Круглосуточное
                schedule = next(i for i in self.core.get_access_schedules(self.session_id)
                                if i.NAME == "Круглосуточное")
                # Создаём RFID
                rfid = hex(randint(900_000_000, 999_999_999))[2:]
                acc_group_id = None
                access_groups = self.core.get_access_groups(self.session_id)
                for group in access_groups:
                    if group.NAME == access_group_name:
                        acc_group_id = group.ID
                if not acc_group_id:
                    # Создаём группу доступа
                    acc_group_id = (self.core.create_access_group(self.session_id,
                                                                  access_group_name,
                                                                  schedule.ID)).Value
                mask = None
                if privileges:
                    # Создаем маску привелегий
                    result = 0
                    for i in privileges:  # Пример прохода 2 - проход при блокировке и 6 - Проход при антипассбеке
                        result += 2 ** i  # Вычисляем
                    mask = bin(result)[2:]
                # Устанавливаем привилегии идентификатору
                self.core.set_identifier_privileges(self.session_id, rfid, mask)
                # Формируем ДТО
                dto = Identifier(CODE=rfid, PERSON_ID=claim.PERSON_ID, IS_PRIMARY=True,
                                 ACCGROUP_ID=acc_group_id, PRIVILEGE_MASK=mask, IDENTIFTYPE=0)
                # Ебемся с изменениями идентификатора (Так как по умолчанию стоит BaseIdentifier)
                object_type = self.core.client.get_type('ns0:Identifier')
                object_wrap = xsd.Element('Identifier', object_type)
                identifier_dto = object_wrap(**dict(dto))
                self.core.add_person_identifier(person_edit_session.Value, identifier_dto)
                self.core.activate_visitor_request(self.session_id, claim.ID, rfid)
                return claim
            if claim.NUMBER == claim_id and claim.STATUS == 1:
                raise ParsecIntegrationError(f"Claim with id: {claim_id} already approved")
        else:
            raise ParsecIntegrationError(f"Claim with id: {claim_id} not found")
