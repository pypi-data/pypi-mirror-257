from datetime import datetime

from pydantic import BaseModel, field_validator

from parsec_integration.parsec_integration.dto.validators import guid_validate, long_validate

Guid = str
Object = dict
long = str
default_id = "00000000-0000-0000-0000-000000000000"


class ClaimStatus(BaseModel):
    issued: bool = False
    accepted: bool = False
    declined: bool = False
    active: bool = False
    completed: bool = False


class ParsecConfigDto(BaseModel):
    host: str
    port: int
    login: str
    password: str
    language: str = "ru-RU"
    domain: str = "SYSTEM"


class ParsecSystemInfo(BaseModel):
    version: str = None
    domains: list = None


class Session(BaseModel):
    SessionID: Guid
    RootOrgUnitID: Guid
    RootTerritoryID: Guid


class BaseResult(BaseModel):
    """
    Result:
        Результат выполнения может быть следующим:
        0 – операция выполнена успешно;
        -1 – операция выполнена с ошибкой;
        Значения >0 планируется использовать для кодов специфических ошибок.
    ErrorMessage:
        Описание ошибки, произошедшей при выполнении операции.
    """
    Result: int
    ErrorMessage: str


class GuidResult(BaseResult):
    Value: Guid


class SessionResult(BaseResult):
    Value: Session


class StringResult(BaseResult):
    Value: str


class ObjectResult(BaseResult):
    Value: Object


class BaseObject(BaseModel):
    pass


class BaseOrgUnit:
    class Create(BaseObject):
        ID: Guid = default_id
        NAME: str
        DESC: str = None

    class Update(BaseObject):
        NAME: str = None
        DESC: str = None


class OrgUnit:
    class Create(BaseOrgUnit.Create):
        PARENT_ID: Guid

        @field_validator("PARENT_ID")
        @classmethod
        def validate_guid(cls, v):
            return guid_validate(value=v)

    class Update(BaseOrgUnit.Update):
        PARENT_ID: Guid

        @field_validator("PARENT_ID")
        @classmethod
        def validate_guid(cls, v):
            return guid_validate(value=v)


class BasePerson(BaseObject):
    ID: Guid = default_id
    LAST_NAME: str
    FIRST_NAME: str
    MIDDLE_NAME: str
    TAB_NUM: str = None


class Person(BasePerson):
    ORG_ID: Guid

    @field_validator("ORG_ID")
    @classmethod
    def validate_guid(cls, v):
        return guid_validate(value=v)


class PersonWithPhoto(Person):  # TODO Возможно проёб
    PHOTO: list[bytes]


# class PersonExtraFieldTemplate(BaseModel):  # TODO Возможно тоже проёб
#     ID: Guid
#     TYPE: XmlTypeCode
#     NAME: str


class PersonScheduleFix(BaseModel):
    FIX_ID: Guid
    PERSON_ID: Guid
    TYPE_ID: int
    START: datetime
    END: datetime
    COMMENT: str


class ExtraFieldValue(BaseObject):
    TEMPLATE_ID: Guid
    VALUE: Object


class VisitorRequest:

    class Create(BaseModel):
        ID: Guid = default_id
        NUMBER: int = 0
        DATE: datetime = datetime.now()
        PERSON_ID: Guid
        ORGUNIT_ID: Guid
        PERSON_INFO: str = None
        PURPOSE: str = None
        STATUS: int = 0
        ADMIT_START: datetime
        ADMIT_END: datetime

        @field_validator("PERSON_ID", "ORGUNIT_ID")
        @classmethod
        def validate_guid(cls, v):
            return guid_validate(value=v)

    class Update(BaseModel):
        PERSON_INFO: str = None
        PURPOSE: str = None
        ADMIT_START: datetime = None
        ADMIT_END: datetime = None


class TimeInterval(BaseObject):
    START: datetime
    END: datetime


class WorktimeInterval(TimeInterval):
    TYPE: int


class Holiday(BaseObject):
    NAME: str
    MONTH: bytes
    DAY: bytes


class BaseIdentifier(BaseObject):
    CODE: str
    PERSON_ID: Guid
    IS_PRIMARY: bool


class Identifier(BaseIdentifier):
    ACCGROUP_ID: Guid
    PRIVILEGE_MASK: long | None = None
    IDENTIFTYPE: int
    NAME: str = None

    @field_validator("PRIVILEGE_MASK")
    @classmethod
    def validate_mask(cls, v):
        return long_validate(value=v)


class IdentifierTemp(Identifier):
    VALID_FROM: datetime
    VALID_TO: datetime


class StockIdentifier(IdentifierTemp):
    pass


class IdentifierExData(BaseObject):
    PASSAGE_ROLE_ID: Guid
    ENTRY_LIMIT: int
    OWNED_COMPONENT_ID: Guid


class Schedule(BaseObject):
    ID: Guid
    NAME: str


class AccessSchedule(Schedule):
    DESC: str
    IS_WEEK: bool
    HOLIDAYS_ACTION: int


class WorktimeSchedule(AccessSchedule):
    HOURS_PER_WEEK: int
    HOURS_PER_DAY: int


class ScheduleDay(BaseObject):
    DATE: datetime
    INDEX: int
    INTERVALS: list[TimeInterval]


class ScheduleFix(ScheduleDay):
    ACTION: int


class PassageRole(BaseObject):
    ID: Guid = default_id
    NAME: str
    DESCRIPTION: str = None


class BaseTerritory(BaseModel):
    ID: Guid
    TYPE: bytes
    NAME: str
    DESC: str


class Territory(BaseTerritory):
    PARENT_ID: Guid


class TerritoryWithComponent(Territory):
    FEATURE_MASK: long

    @field_validator("FEATURE_MASK")
    @classmethod
    def validate_mask(cls, v):
        res = long_validate(value=v)
        print(res)
        return res


class AccessGroup(BaseObject):
    ID: Guid
    NAME: str
    IDENTIFTYPE: int


class SubAccessGroup(BaseObject):
    SubGroupID: Guid
    ScheduleID: Guid
    Territories: list[Guid]


class Event(BaseObject):
    EventDate: datetime
    EventType: int
    EventPersonIndex: int
    CODE: str
    EventTerritoryIndex: int


class EventsHistory(BaseModel):
    Events: list[Event]
    Persons: list[Guid]
    PersonFullNames: list[str]
    Territories: list[Guid]
    TerritoryNames: list[str]


class EventObject(BaseObject):
    Values: list[Object]


class EventsHistoryResult(BaseResult):
    Value: EventsHistory


class Domain(BaseObject):
    NAME: str
    DESCRIPTION: str
    VISITOR_CONTROL: bool
    IS_SYSTEM: bool


class EventHistoryQueryParams(BaseModel):  # TODO Доделать
    pass


class EventFilter(BaseModel):  # TODO Доделать
    pass


class AdvancedEventFilter(EventFilter, BaseObject):  # TODO Доделать
    pass


class HardwareState(BaseObject):  # TODO Доделать
    pass


class TransactionClass(BaseObject):  # TODO Доделать
    pass


class TransactionType(BaseObject):  # TODO Доделать
    pass


class QRAdvancedGroup(BaseObject):  # TODO Доделать
    pass


class QRAdvancedData(BaseObject):  # TODO Доделать
    pass


