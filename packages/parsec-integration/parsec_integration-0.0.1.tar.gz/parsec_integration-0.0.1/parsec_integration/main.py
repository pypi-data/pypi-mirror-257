from datetime import datetime

import zeep

from parsec_integration.parsec_integration.dto.dto import OrgUnit, BaseOrgUnit, ExtraFieldValue, Person, VisitorRequest, Holiday, \
    PassageRole, BaseIdentifier, PersonScheduleFix, IdentifierExData, BasePerson
from parsec_integration.parsec_integration.dto.dto import Guid, long


class Parsec:

    def __init__(self, address):
        self.client = zeep.Client(address)

    def get_version(self):
        """
            Результат: Возвращает версию сервиса интеграции.
            Описание: Функция возвращает версию сервиса интеграции.
        """
        return self.client.service.GetVersion()

    def get_domains(self):
        """
            Результат: Возвращает массив Domain.
            Описание: Возвращает массив организаций.
        """
        return self.client.service.GetDomains()

    def open_session(self, domain: str, username: str, password: str, locale: str = ""):
        """
            domain - Название организации для входа. Для входа в системную организацию можно использовать пустую строку
            username - Имя оператора
            password - Пароль оператора
            locale - С указанием языка интерфейса (Возможны значения «ru-RU», «en-US» или «es-ES»)

            Результат: Возвращает класс.
            Описание: Данная функция используется для аутентификации оператора в
                сервисе интеграции. Полученный ключ сессии используется в дальнейшем для
                выполнения всех операций. Каждая сессия открывается на 5 минут, при
                выполнении любой операции на сервере интеграции время сессии продлевается
        """
        if locale:
            return self.client.service.OpenSessionWithInLocale(domain, username, password, locale)
        return self.client.service.OpenSession(domain, username, password)

    def continue_session(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: В качестве результата возвращается значение: 0 – если операция
                прошла успешно; -1 – если операция выполнена с ошибками.
            Описание: Используется для продления сессии.
        """
        return self.client.service.ContinueSession(session_id)

    def close_session(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: –
            Описание: Используется для закрытия сессии.
        """
        return self.client.service.CloseSession(session_id)

    def check_role(self, session_id: Guid, role_name: str):
        """
            session_id - Уникальный ключ сессии
            role_name - Наименование права на совершение операций

            Результаты: Возвращает BaseResult.
            Описание: Проверяет доступность действий для текущего оператора. В
            интеграционном сервисе используются следующие права:
                "EmployeeReader" - Право получения сведений структуре подразделений.
                "EmployeeWriter" - Право на удаление/изменение сведений персонале и структуре подразделений.о
                "PersonDelete" - Право на удаление субъектов доступа.
                "AccessGroupReader" - Право получения сведений о группах доступа.
                "AccessGroupWriter" - Право на изменение групп доступа.
                "GuestReader" - Право получения сведений о посетителях.
                "VisitorRequestCreator" - Право на создание, редактирование и удаление заявок и посетителей.
                "VisitorRequestCoordinator" - Право на согласование заявок для посетителей.
                "VisitorPassDistributor" - Право на выдачу пропусков для посетителей и закрытие заявок.
                "TimesheetReader" - Право просмотра сведений о расписании.
                "TimesheetWriter" - Право на создание, удаление и изменение расписаний.
                "HardwareControl" - Право на отправку команд управления оборудованием доступа.
                "AlarmHardwareControl" - Право на отправку команд постановки и снятия с охраны.
                "HardwareWriter" - Право «Полный доступ» к Редактору оборудования
                (в части управления ролями группового прохода)
                "MonitorReader" - Право для получения событий системы и статусов оборудования в реальном времени.
                "VideoVerification"Право на подтверждение доступа.
        """
        return self.client.service.CheckRole(session_id, role_name)

    def get_object_name(self, session_id: Guid, object_id: Guid):
        """
            session_id - Уникальный ключ сессии
            object_id - Уникальный ключ объекта

            Результат: Возвращает StringResult.
            Описание: Возвращает наименование любого объекта системы по его ключу.
        """
        return self.client.service.GetObjectName(session_id, object_id)

    # ---------------------------------Hardware--------------------------------------

    def send_hardware_command(self, session_id: Guid, territory_id: Guid, command: int):
        """
            session_id - Уникальный ключ сессии
            territory_id - Уникальный ключ территории
            command - Код посылаемой команды

            Результат: Возвращает BaseResult.
            Описание: Посылает команду устройству, представленному территорией.
            Коды команд и устройства описаны в таблице ниже.
        ----------------------------------------------------------------------------------|
        |            Команды                         | Контрол.  |  Охранная  |  Охранный |
        |____________________________________________| доступа   |  область   |  раздел   |
        | Код |                Описание              | Parsec    |  АС-08     |  Болид    |
        |_________________________________________________________________________________|
        |  1  | Включить реле на вход*               |           |            |           |
        |     | / Открыть дверь                      |    ✓      |            |           |
        |     |______________________________________|____________________________________|
        |  2  | Включить реле на вход*               |           |            |           |
        |     |                                      |    ✓      |            |           |
        |     |______________________________________|____________________________________|
        |  4  | Закрыть дверь                        |           |            |           |
        |     |                                      |    ✓      |            |           |
        |     |______________________________________|____________________________________|
        |  8  | Установить относительную блокировку  |           |            |           |
        |     |                                      |    ✓      |            |           |
        |     |______________________________________|____________________________________|
        |  16 | Снять относительную блокировку       |           |            |           |
        |     |                                      |    ✓      |            |           |
        |     |______________________________________|____________________________________|
        |  32 | Установить абсолютную блокировку     |           |            |           |
        |     |                                      |    ✓      |            |           |
        |     |______________________________________|____________________________________|
        |  64 | Снять абсолютную блокировку          |           |            |           |
        |     |                                      |    ✓      |            |           |
        |     |______________________________________|____________________________________|
        | 128 | Установить на охрану                 |           |            |           |
        |     |                                      |    ✓      |     ✓      |     ✓     |
        |     |______________________________________|____________________________________|
        | 256 | Снять с охраны                       |           |            |           |
        |     |                                      |    ✓      |     ✓      |     ✓     |
        |     |______________________________________|____________________________________|
        | 512 | Включить доп. реле                   |           |            |           |
        |     |                                      |    ✓      |            |           |
        |     |______________________________________|____________________________________|
        | 1024| Выключить доп. реле                  |           |            |           |
        |     |                                      |    ✓      |            |           |
        |     |______________________________________|____________________________________|
        | 2048| Сброс антипассбека                   |           |            |           |
        |     |                                      |    ✓      |            |           |
        |     |______________________________________|____________________________________|
        |     * Команды работают только для контроллеров в режиме турникета.              |
        |_________________________________________________________________________________|
        """
        return self.client.service.SendHardwareCommand(session_id, territory_id, command)

    def send_verification_command(self, session_id: Guid, territory_id: Guid, person_id: Guid, pass_allow: bool):
        """
            session_id - Уникальный ключ сессии
            territory_id - Уникальный ключ территории
            person_id - Уникальный ключ субъекта доступа
            pass_allow - Флаг разрешения/запрещения прохода

            Результат: Возвращает массив BaseResult.
            Описание: Посылает команду устройству, представленному территорией, на
                подтверждение или запрет прохода. В настройках контроллера должно быть
                выбрано программное подтверждение прохода.
        """
        return self.client.service.SendVerificationCommand(session_id, territory_id, person_id, pass_allow)

    def get_hardware_state(self, session_id: Guid, territory_ids: list[Guid]):  # TODO Нужна ли таблица ?
        """
            session_id - Уникальный ключ сессии
            territory_ids - Список ключей территорий

            Результат: Возвращает массив битовых масок HardwareState (каждая маска
                размером 8 байт).
            Описание: Выдает набор состояний для выбранных территорий. Коды
                состояний описаны в таблицах ниже. Функция применима только к территориям,
                порождаемым контроллерами доступа серии NC, охранным контроллером АС-08
                и охранной системой Болид.

            Биты состояния территории для контроллеров серии NC
            Биты состояния территории-охранной области контроллера АС-08 и
                охранной системы Bolid
        """
        return self.client.service.GetHardwareState(session_id, territory_ids)

    # ------------------------------Departments Get------------------------------------

    def get_root_org_unit(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает корневую OrgUnit.
            Описание: данная функция предназначена для получения корневого объекта
                дерева подразделений.
        """
        return self.client.service.GetRootOrgUnit(session_id)

    def get_org_units_hierarchy(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Массив OrgUnit.
            Описание: Возвращает полную иерархию подразделений.
        """
        return self.client.service.GetOrgUnitsHierarhy(session_id)

    def get_org_units_hierarchy_with_persons(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Массив BaseObject, элементы массива могут быть OrgUnit или Person.
            Описание: Возвращает полную иерархию подразделений вместе с сотрудниками.
        """
        return self.client.service.GetOrgUnitsHierarhyWithPersons(session_id)

    def get_org_units_hierarchy_with_visitors(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Массив BaseObject, элементы массива могут быть OrgUnit или Person.
            Описание: Возвращает полную иерархию подразделений вместе с посетителями.
        """
        return self.client.service.GetOrgUnitsHierarhyWithVisitors(session_id)

    def get_org_units_hierarchy_with_vehicle(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Массив BaseObject, элементы массива могут быть OrgUnit или Person.
            Описание: Возвращает полную иерархию подразделений вместе с автомобилями.
        """
        return self.client.service.GetOrgUnitsHierarhyWithVehicle(session_id)

    def get_org_unit_sub_items(self, session_id: Guid, org_unit_id: Guid):
        """
            session_id - Уникальный ключ сессии
            org_unit_id - Уникальный ключ подразделения

            Результат: Массив BaseObject, элементы массива могут быть BaseOrgUnit или BasePerson.
            Описание: Возвращает массив подразделений и сотрудников, принадлежащих
                подразделению с указанным ключом.
        """
        return self.client.service.GetOrgUnitSubItems(session_id, org_unit_id)

    def get_org_unit_sub_items_hierarchy_with_persons(self, session_id: Guid, org_unit_id: Guid):
        """
            session_id - Уникальный ключ сессии
            org_unit_id - Уникальный ключ подразделения

            Результат: Массив BaseObject, элементы массива могут быть OrgUnit или Person.
            Описание: Возвращает полную иерархию подразделений и их сотрудников,
                начиная с подразделения с указанным ключом.
        """
        return self.client.service.GetOrgUnitSubItemsHierarhyWithPersons(session_id, org_unit_id)

    def get_org_unit_sub_items_hierarchy_with_visitors(self, session_id: Guid, org_unit_id: Guid):
        """
            session_id - Уникальный ключ сессии
            org_unit_id - Уникальный ключ подразделения

            Результат: Массив BaseObject, элементы массива могут быть OrgUnit или Person.
            Описание: Возвращает полную иерархию подразделений, начиная
                с подразделения с указанным ключом, и посетителей этих подразделений.
        """
        return self.client.service.GetOrgUnitSubItemsHierarhyWithVisitors(session_id, org_unit_id)

    def get_org_unit_sub_items_hierarchy_with_vehicle(self, session_id: Guid, org_unit_id: Guid):
        """
            session_id - Уникальный ключ сессии
            org_unit_id - Уникальный ключ подразделения

            Результат: Массив BaseObject, элементы массива могут быть OrgUnit или Person.
            Описание: Возвращает полную иерархию подразделений, начиная
                с подразделения с указанным ключом, и транспортных средств этих подразделений.
        """
        return self.client.service.GetOrgUnitSubItemsHierarhyWithVehicle(session_id, org_unit_id)

    def get_org_unit(self, session_id: Guid, org_unit_id: Guid):
        """
            session_id - Уникальный ключ сессии
            org_unit_id - Уникальный ключ подразделения

            Результат: Возвращает OrgUnit для подразделения с указанным ключом или
                null, если указанное подразделение не найдено.
            Описание: Возвращает информацию о подразделении с указанным ключом.
        """

    # ---------------------------Departments Create Patch---------------------------------

    def create_org_unit(self, session_id: Guid, org_unit: BaseOrgUnit.Create | OrgUnit.Create):
        """
            session_id - Уникальный ключ сессии
            org_unit - Параметры подразделения

            Результат: Возвращает GuidResult.
            Описание: Создает подразделение с указанными данными. Возвращает ключ
                вновь созданного подразделения. Если поле ID в структуре OrgUnit равен
                Guid.Empty (00000000-0000-0000-0000-000000000000), то ID генерируется
                автоматически и возвращается. Иначе используется заданное значение ID.
        """
        return self.client.service.CreateOrgUnit(session_id, dict(org_unit))

    def open_org_unit_editing_session(self, session_id: Guid, org_unit_id: Guid):
        """
            session_id - Уникальный ключ сессии
            org_unit_id - Уникальный ключ подразделения

            Результат: Возвращает GuidResult.
            Описание: Открывает сессию редактирования подразделения. Возвращает
                ключ вновь созданной сессии редактирования подразделения.
        """
        return self.client.service.OpenOrgUnitEditingSession(session_id, org_unit_id)

    def close_org_unit_editing_session(self, org_unit_edit_session_id: Guid):
        """
            org_unit_edit_session_id - Уникальный ключ сессии редактирования подразделения

            Результат: –
            Описание: Закрывает сессию редактирования подразделения.
        """
        return self.client.service.CloseOrgUnitEditingSession(org_unit_edit_session_id)

    def save_org_unit(self, org_unit_edit_session_id: Guid, org_unit: BaseOrgUnit):
        """
            org_unit_edit_session_id - Уникальный ключ сессии редактирования подразделения
            org_unit - Параметры подразделения

            Результат: Возвращает BaseResult.
            Описание: Изменяет параметры подразделения. Параметр orgUnit может быть BaseOrgUnit или OrgUnit.
                При передаче в запросе в качестве параметров подразделения структуры OrgUnit необходимо
                в обязательном порядке указывать в элементе orgUnit атрибут xsi:type="OrgUnit".
                После удачного сохранения подразделения сессия редактирования закрывается.

            Пример реализации изменения PARENT_ID у департамента:
            edit = parsec.open_org_unit_editing_session(session_id, "2770b2d4-e278-4b3d-b186-9ba3432440bd")
            print(parsec.client.service.SaveOrgUnit.__doc__)  # узнать тип объекта
            object_type = parsec.client.get_type('ns0:OrgUnit')  # указываем тип объекта, xml атрибут xsi:type
            object_wrap = xsd.Element('OrgUnit', object_type)  # xmlTagName - название xml-тега (parsec.client.service.SavePerson.__doc__)
            value = object_wrap("2770b2d4-e278-4b3d-b186-9ba3432440bd",
                                "Long, Hogan and Kramer",
                                "some description",
                                "1f085a9b-19b3-4a4a-b95b-6fab8b45ceca")
            result = parsec.save_org_unit(edit.Value, value)
        """
        return self.client.service.SaveOrgUnit(org_unit_edit_session_id, org_unit)

    def delete_org_unit(self, org_unit_edit_session_id: Guid, org_unit_id: Guid):
        """
            session_id - Уникальный ключ сессии
            org_unit_id - Уникальный ключ подразделения

            Результат: Возвращает BaseResult.
            Описание: Удаляет подразделение с указанным ключом.
        """

    # ----------------------------------Personal------------------------------------------

    def get_person_extra_field_templates(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив PersonExtraFieldTemplate.
            Описание: Возвращает набор шаблонов дополнительных полей у сотрудников.
        """
        return self.client.service.GetPersonExtraFieldTemplates(session_id)

    def get_visitor_extra_field_templates(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив PersonExtraFieldTemplate.
            Описание: Возвращает набор шаблонов дополнительных полей у посетителей..
        """
        return self.client.service.GetVisitorExtraFieldTemplates(session_id)

    def get_vehicle_extra_field_templates(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив PersonExtraFieldTemplate.
            Описание: Возвращает набор шаблонов дополнительных полей у транспортных средств.
        """
        return self.client.service.GetVehicleExtraFieldTemplates(session_id)

    def find_people(self, session_id: Guid, lastname: str, firstname: str, middlename: str):
        """
            session_id - Уникальный ключ сессии
            lastname - Значение фамилии для поиска
            firstname - Значение имени для поиска
            middlename - Значение отчества для поиска

            Результат: Возвращает массив Person.
            Описание: Выдает набор сотрудников, подходящих под переданные критерии.
                Поиск может производиться как по любому параметру отдельно, так и по всем
                параметрам. Должен быть указан хотя бы один параметр.
        """
        return self.client.service.FindPeople(session_id, lastname, firstname, middlename)

    def find_visitors(self, session_id: Guid, lastname: str = None, firstname: str = None, middlename: str = None):
        """
            session_id - Уникальный ключ сессии
            lastname - Значение фамилии для поиска
            firstname - Значение имени для поиска
            middlename - Значение отчества для поиска

            Результат: Возвращает массив Person.
            Описание: Выдает набор посетителей, подходящих под переданные критерии.
                Поиск может производиться как по любому параметру отдельно, так и по всем
                параметрам. Должен быть указан хотя бы один параметр.
        """
        return self.client.service.FindVisitors(session_id, lastname, firstname, middlename)

    def find_vehicle(self, session_id: Guid, number: str, model: str, color: str):
        """
            session_id - Уникальный ключ сессии
            number - Значение номера автомобиля для поиска
            model - Значение модели автомобиля для поиска
            color - Значение цвета для поиска

            Результат: Возвращает массив Person.
            Описание: Выдает набор автомобилей, подходящих под переданные критерии.
                Поиск может производиться как по любому параметру отдельно, так и по всем
                параметрам. Должен быть указан хотя бы один параметр.
        """
        return self.client.service.FindVisitors(session_id, number, model, color)

    def find_person_by_identifier(self, session_id: Guid, cardcode: str):
        """
            session_id - Уникальный ключ сессии
            cardcode - Код идентификатора карты в 16-ричном формате в верхнем регистре (Например: A12345BCF)

            Результат: Возвращает Person.
            Описание: Возвращает информацию о субъекте доступа с указанным кодом
                идентификатора.
        """
        return self.client.service.FindPersonByIdentifier(session_id, cardcode)

    def person_search(self, session_id: Guid, field_id: Guid, relation: int, value, value1=None):  # TODO не работает
        """
            session_id - Уникальный ключ сессии
            field_id - Уникальный ключ поля, используемого для поиска
            relation - Критерий поиска
            value - Искомое значение или первое значение для критерия поиска «между»
            value1 - Второе значение для критерия поиска «между»

            0de358e0-c91b-4333-b902-000000000003 | Фамилия / Номер авто    | string
            0de358e0-c91b-4333-b902-000000000001 | Имя / Модель авто       | string
            0de358e0-c91b-4333-b902-000000000002 | Отчество / Цвет авто    | string
            0de358e0-c91b-4333-b902-000000000006 | Табель                  | string
            0de358e0-c91b-4333-b902-000000000004 | Подразделение           | string
            0a679144-d5ce-476d-a56e-0a696f079b71 | Описание подразделения  | string
            0de358e0-c91b-4333-b902-00000000000a | Группа доступа          | string
            0de358e0-c91b-4333-b902-000000000005 | Код карты               | string
            644E1B95-E87B-415D-91BF-C3242B6C3AEA | Наименование идентификатора | string
            0de358e0-c91b-4333-b902-000000000007 | Время действия с        | DateTime
            0de358e0-c91b-4333-b902-000000000008 | Время действия по       | DateTime
            6FCFA1BB-9624-4248-A2D5-AA84901C53C8 | Субъект в чёрном списке | bool
            07AF86B3-23FC-44EF-8438-6EE601B2FCB0 | Доступ запрещен         | bool

            Значение Описание
               0     Равно (=)
               1     Меньше или равно (<=)
               2     Меньше (<)
               3     Больше или равно (>=)
               4     Больше (>)
               5     Между
               6     Содержит
               7     Пусто
               8     Не пусто

            Результат: Возвращает массив Person.
            Описание: Возвращает информацию о субъектах доступа, удовлетворяющим
                параметрам поиска.
        """
        return self.client.service.PersonSearch(session_id, field_id, relation, value, value1)

    def get_person(self, session_id: Guid, person_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ субъекта доступа

            Результат: Возвращает PersonWithPhoto.
            Описание: Возвращает информацию о субъекте доступа с указанным ключом.
        """
        return self.client.service.GetPerson(session_id, person_id)

    def get_multiple_persons(self, session_id: Guid, person_ids: list[Guid]):
        """
            session_id - Уникальный ключ сессии
            person_ids - Массив ключей субъектов доступа

            Результат: Возвращает массив PersonWithPhoto.
            Описание: Возвращает информацию о субъектах доступа с указанными
                ключами.
        """
        return self.client.service.GetMultiplePersons(session_id, person_ids)

    def get_persons_changed_after(self, session_id: Guid, org_id: Guid, date_from: datetime, include_sub_org: bool):
        """
            session_id - Уникальный ключ сессии
            org_id - Уникальный ключ подразделения
            date_from - Начальная дата для анализа
            include_sub_org - Признак поиска по вложенным подразделениям

            Результат: Возвращает массив Person.
            Описание: Возвращает набор субъектов доступа (сотрудник, посетитель,
                автомобиль), чьи данные были изменены, начиная с указанной даты. Поиск
                производится либо в указанном подразделении, либо в указанном и во всех
                вложенных.
        """
        return self.client.service.GetPersonsChangedAfter(session_id, org_id, date_from, include_sub_org)

    def get_person_extra_field_value(self, session_id: Guid, person_id: Guid, template_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ субъекта доступа
            template_id - Уникальный ключ шаблона

            Результат: Возвращает ObjectResult.
            Описание: Возвращает значение указанного дополнительного поля субъекта
                доступа. Тип значения определяется типом поля.
        """
        return self.client.service.GetPersonExtraFieldValue(session_id, person_id, template_id)

    def get_person_extra_field_values(self, session_id: Guid, person_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ субъекта доступа

            Результат: Возвращает массив ExtraFieldValue.
            Описание: Возвращает массив значений дополнительных полей субъекта
                доступа.
        """
        return self.client.service.GetPersonExtraFieldValues(session_id, person_id)

    def get_person_extra_field_value_string(self, session_id: Guid, person_id: Guid, template_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ субъекта доступа
            template_id - Уникальный ключ шаблона

            Результат: Возвращает StringResult.
            Описание: Возвращает значение дополнительного поля субъекта доступа в
                виде форматированной строки.
        """

    def validate_extra_field_value(self, session_id: Guid, value: ExtraFieldValue):
        """
            session_id - Уникальный ключ сессии
            value - Значение дополнительного поля

            Результат: Возвращает BaseResult.
            Описание: Проверяет валидность значения дополнительного поля.
                В запросе, в элементе value необходимо указывать тип значения в атрибуте
                xsi:type. Например, xsi:type="xsd:string" (см. пример из описания ф-ии
                SetPersonExtraFieldValue).
        """
        return self.client.service.ValidateExtraFieldValue(session_id, value)

    def get_person_schedule_fixes(self, session_id: Guid, person_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ сотрудника

            Результат: Возвращает массив PersonScheduleFix.
            Описание: Возвращает список существующих поправок к рабочему времени
                сотрудника.
        """
        return self.client.service.GetPersonScheduleFixes(session_id, person_id)

    def add_person_schedule_fix(self, session_id: Guid, fix: PersonScheduleFix):
        """
            session_id - Уникальный ключ сессии
            fix - Параметры поправки рабочего времени

            Результат: Возвращает GuidResult.
            Описание: Добавляет поправку рабочего времени сотрудника.
        """
        return self.client.service.AddPersonScheduleFix(session_id, fix)

    def save_person_schedule_fix(self, session_id: Guid, fix: PersonScheduleFix):
        """
            session_id - Уникальный ключ сессии
            fix - Параметры поправки рабочего времени

            Результат: Возвращает BaseResult.
            Описание: Изменяет параметры существующей поправки рабочего времени сотрудника.
        """
        return self.client.service.SavePersonScheduleFix(session_id, fix)

    def delete_person_schedule_fix(self, session_id: Guid, person_id: Guid, fix_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ сотрудника
            fix_id - Уникальный ключ поправки

            Результат: Возвращает BaseResult.
            Описание: Удаляет поправку к рабочему времени сотрудника.
        """
        return self.client.service.DeletePersonScheduleFix(session_id, person_id, fix_id)

    def get_person_worktime_schedule(self, session_id: Guid, person_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ сотрудника

            Результат: Возвращает GuidResult.
            Описание: Возвращает уникальный ключ расписания рабочего времени,
                назначенного сотруднику. Если расписание не назначено, возвращает
                Guid.Empty.
        """
        return self.client.service.GetPersonWorktimeSchedule(session_id, person_id)

    def set_person_worktime_schedule(self, person_edit_session_id: Guid, schedule_id: Guid):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования сотрудника
            schedule_id - Уникальный ключ расписания рабочего времени

            Результат: Возвращает BaseResult.
            Описание: Задает сотруднику персональное расписание рабочего времени, с
                указанным ключом.
        """
        return self.client.service.SetPersonWorktimeSchedule(person_edit_session_id, schedule_id)

    def get_black_list(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив Person.
            Описание: Выдает набор субъектов доступа, находящихся в черном списке.
        """
        return self.client.service.GetBlackList(session_id)

    def find_in_black_list(self, session_id: Guid, lastname: str, firstname: str, middlename: str):
        """
            session_id - Уникальный ключ сессии
            lastname - Значение фамилии для поиска
            firstname - Значение имени для поиска
            middlename - Значение отчества для поиска

            Результат: Возвращает массив Person.
            Описание: Выдает набор субъектов доступа, подходящих под переданные
                критерии и находящихся в черном списке. Поиск может производиться как по
                любому параметру отдельно, так и по всем параметрам. Должен быть указан хотя
                бы один параметр.
        """
        return self.client.service.FindInBlackList(session_id, lastname, firstname, middlename)

    def add_to_black_list(self, session_id: Guid, person_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ субъекта доступа

            Результат: Возвращает BaseResult.
            Описание: Добавляет субъект доступа с указанным ID в черный список.
        """
        return self.client.service.AddToBlackList(session_id, person_id)

    def remove_from_black_list(self, session_id: Guid, person_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ субъекта доступа

            Результат: Возвращает BaseResult.
            Описание: Удаляет субъект доступа с указанным ID из черного списка.
        """
        return self.client.service.RemoveFromBlackList(session_id, person_id)

    # ---------------------------------Personal Changes----------------------------------------

    def create_person(self, session_id: Guid, person: BasePerson | Person):
        """
            session_id - Уникальный ключ сессии
            person_id - Данные сотрудника

            Результат: Возвращает GuidResult.
            Описание: Создает сотрудника с указанными данными.
            В качестве параметра person может быть Person или PersonWithPhoto.
            Возвращает ключ вновь созданного сотрудника. Если поле ID в структуре person равен
            Guid.Empty (00000000-0000-0000-0000-000000000000), то ID генерируется
            автоматически и возвращается. Иначе используется заданное значение ID.
        """
        return self.client.service.CreatePerson(session_id, dict(person))

    def create_visitor(self, session_id: Guid, person: BasePerson | Person):
        """
            session_id - Уникальный ключ сессии
            person_id - Данные посетителя

            Результат: Возвращает GuidResult.
            Описание: Создает посетителя с указанными данными.
            В качестве параметра person может быть Person или PersonWithPhoto.
            Возвращает ключ вновь созданного посетителя. Если поле ID в структуре person равен
            Guid.Empty (00000000-0000-0000-0000-000000000000), то ID генерируется
            автоматически и возвращается. Иначе используется заданное значение ID.
        """
        return self.client.service.CreateVisitor(session_id, dict(person))

    def create_vehicle(self, session_id: Guid, person: BasePerson | Person):
        """
            session_id - Уникальный ключ сессии
            person_id - Данные автомобиля

            Результат: Возвращает GuidResult.
            Описание: Создает автомобиль с указанными данными.
            В качестве параметра person может быть Person или PersonWithPhoto.
            Возвращает ключ вновь созданного автомобиля. Если поле ID в структуре person равен
            Guid.Empty (00000000-0000-0000-0000-000000000000), то ID генерируется
            автоматически и возвращается. Иначе используется заданное значение ID.
        """
        return self.client.service.CreateVehicle(session_id, dict(person))

    def open_person_editing_session(self, session_id: Guid, person_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ субъекта доступа

            Результат: Возвращает GuidResult.
            Описание: Открывает сессию редактирования субъекта доступа. Возвращает
                ключ вновь созданной сессии.
        """
        return self.client.service.OpenPersonEditingSession(session_id, person_id)

    def close_person_editing_session(self, person_edit_session_id: Guid):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования субъекта доступа

            Результат: –
            Описание: Закрывает сессию редактирования субъекта доступа.
        """
        return self.client.service.ClosePersonEditingSession(person_edit_session_id)

    def save_person(self, person_edit_session_id: Guid, person: Person):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования субъекта доступа
            person - Данные субъекта доступа

            Результат: Возвращает BaseResult.
            Описание: Изменяет данные субъекта доступа. В качестве параметра person
                может служить BasePerson, Person, PersonWithPhoto.
                При передаче в запросе в качестве данных субъекта доступа структуры Person
                или PersonWithPhoto необходимо в обязательном порядке указывать название
                класса в атрибуте xsi:type элемента person.
                В случае удачного сохранения сессия редактирования субъекта доступа закрывается.
        """
        return self.client.service.SavePerson(person_edit_session_id, person)

    def set_person_photo(self, person_edit_session_id: Guid, photo_byte_array: bytes):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования субъекта доступа
            photo_byte_array - Фото субъекта доступа

            Результат: Возвращает BaseResult.
            Описание: Сохраняет фото субъекта доступа. В случае удачного сохранения
                сессия редактирования субъекта доступа закрывается.
        """
        return self.client.service.SetPersonPhoto(person_edit_session_id, photo_byte_array)

    def set_person_org_unit(self, person_edit_session_id: Guid, org_unit_id: Guid):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования субъекта доступа
            org_unit_id - Уникальный ключ подразделения

            Результат: Возвращает BaseResult.
            Описание: Устанавливает подразделение субъекта доступа. В случае удачного
                сохранения сессия редактирования субъекта доступа закрывается.
        """
        return self.client.service.SetPersonOrgUnit(person_edit_session_id, org_unit_id)

    def set_person_extra_field_value(self, person_edit_session_id: Guid, template_id: Guid, value):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования субъекта доступа
            template_id - Уникальный ключ шаблона дополнительного поля
            value - Значение дополнительного поля

            Результат: Возвращает BaseResult.
            Описание: Устанавливает новое значение указанного дополнительного поля
            субъекта доступа.
            В запросе, для элемента value необходимо указывать тип значения в атрибуте
            xsi:type. Например, xsi:type="xsd:string".
        """
        return self.client.service.SetPersonExtraFieldValue(person_edit_session_id, template_id, value)

    def set_person_extra_field_values(self, person_edit_session_id: Guid, values: list[ExtraFieldValue]):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования субъекта доступа
            values - Массив значений дополнительных полей

            Результат: Возвращает BaseResult.
            Описание: Устанавливает значения для дополнительных полей.
                В запросе, в каждом элементе массива values необходимо указывать тип
                значения в атрибуте xsi:type. Например, xsi:type="xsd:string" (см. пример в
                описании ф-ии SetPersonExtraFieldValue).
        """
        return self.client.service.SetPersonExtraFieldValue(person_edit_session_id, values)

    def delete_person(self, session_id: Guid, person_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ субъекта доступа

            Результат: Возвращает BaseResult.
            Описание: Удаляет субъект доступа с указанным ключом.
        """
        return self.client.service.DeletePerson(session_id, person_id)

    def block_person(self, person_edit_session_id: Guid, type_block: int):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования субъекта доступа
            type_block - Тип блокировки (
                1 - Установка привилегии «Выход запрещен».
                2 - Установка привилегии «Вход запрещен».
                3 - Установка привилегии «Вход запрещен» и «Выход запрещен».
            )

            Результат: Возвращает BaseResult.
            Описание: Блокирует субъект доступа в соответствии с указанным типом блокировки.
            В случае удачного выполнения функции сессия редактирования данных субъекта доступа закрывается.
        """
        return self.client.service.BlockPerson(person_edit_session_id, type_block)

    def unblock_person(self, person_edit_session_id: Guid):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования субъекта доступа

            Результат: Возвращает BaseResult.
            Описание: Снимает все блокировки с субъекта доступа, заблокированного ранее.
            В случае удачного выполнения функции сессия редактирования субъекта доступа закрывается.
        """
        return self.client.service.UnblockPerson(person_edit_session_id)

    # -------------------------------------Topology----------------------------------------

    def get_root_territory(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает корневую Territory.
            Описание: Данная функция предназначена для получения корневого объекта
                дерева территорий.
        """
        return self.client.service.GetRootTerritory(session_id)

    def get_territory_hierarchy(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив Territory, значения могут быть TerritoryWithComponent.
            Описание: Возвращает полную иерархию территорий.
        """
        return self.client.service.GetTerritoriesHierarhy(session_id)

    def get_territory_sub_items(self, session_id: Guid, terra_id: Guid):
        """
            session_id - Уникальный ключ сессии
            terra_id - Уникальный ключ территории

            Результат: Возвращает массив BaseTerritory, значения могут быть TerritoryWithComponent.
            Описание: Возвращает список территорий, принадлежащих территории с указанным ключом.
        """
        return self.client.service.GetTerritorySubItems(session_id, terra_id)

    def get_territory(self, session_id: Guid, territory_id: Guid):
        """
            session_id - Уникальный ключ сессии
            territory_id - Уникальный ключ территории

            Результат: Возвращает Territory, значение может быть TerritoryWithComponent.
            Описание: Данная функция предназначена для получения описания территории по ее ключу.
        """
        return self.client.service.GetTerritory(session_id, territory_id)

    # -------------------------------------Identifiers and Access-------------------------------------------

    def get_person_identifiers(self, session_id: Guid, person_id: Guid):
        """
            session_id - Уникальный ключ сессии
            person_id - Уникальный ключ субъекта доступа

            Результат: Массив Identifier, элементы массива могут быть Identifier или IdentifierTemp.
            Описание: Возвращает массив идентификаторов для указанного субъекта доступа.
        """
        return self.client.service.GetPersonIdentifiers(session_id, person_id)

    def delete_identifier(self, session_id: Guid, code: str):
        """
            session_id - Уникальный ключ сессии
            code - Код идентификатора

            Результат: Возвращает BaseResult.
            Описание: Удаляет идентификатор с указанным кодом.
        """
        return self.client.service.DeleteIdentifier(session_id, code)

    def add_person_identifier(self, person_edit_session_id: Guid, identifier):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования субъекта доступа
            identifier - Параметры идентификатора

            Результат: Возвращает BaseResult.
            Описание: Добавляет идентификатор субъекту доступа или изменяет данные
                уже имеющегося идентификатора. В качестве параметра identifier могут служить
                BaseIdentifier, Identifier, IdentifierTemp. Элемент IS_PRIMARY используется
                только в позитивном смысле, т.е. при установке этого признака,
                соответствующий идентификатор становится первичным, а при снятии этого
                признака у первичного идентификатора при сохранении в смысле первичности
                идентификатора ничего не меняется. Элемент PRIVILEGE_MASK игнорируется.
                При передаче в запросе в качестве идентификатора структуры Identifier или
                IdentifierTemp необходимо в обязательном порядке указывать в элементе identifier атрибут
                xsi:type="Identifier" либо xsi:type="IdentifierTemp" соответственно.
        """
        return self.client.service.AddPersonIdentifier(person_edit_session_id, identifier)

    def change_person_identifier(self, person_edit_session_id: Guid, identifier: BaseIdentifier):
        """
            person_edit_session_id - Уникальный ключ сессии редактирования субъекта доступа
            identifier - Параметры идентификатора

            Результат: Возвращает BaseResult.
            Описание: Изменяет параметры существующего идентификатора. В качестве
            параметра identifier могут служить BaseIdentifier, Identifier, IdentifierTemp.
            Элемент IS_PRIMARY используется только в позитивном смысле, т.е. при
            установке этого признака, соответствующий идентификатор становится
            первичным, а при снятии этого признака у первичного идентификатора при
            сохранении в смысле первичности идентификатора ничего не меняется. Элемент
            PRIVILEGE_MASK игнорируется.
            При передаче в запросе в качестве идентификатора структуры Identifier или
            IdentifierTemp необходимо в обязательном порядке указывать в элементе identifier атрибут
            xsi:type="Identifier" либо xsi:type="IdentifierTemp" соответственно.
        """
        return self.client.service.ChangePersonIdentifier(person_edit_session_id, identifier)

    def set_identifier_privileges(self, session_id: Guid, card_code: str, privileges_mask: long):
        """
            session_id - Уникальный ключ сессии
            card_code - Код идентификатора
            privileges_mask - Список чисел (Функция сама рассчитывает битовые маски)

            Результат: Возвращает BaseResult.
            Описание: Функция устанавливает набор привилегий с помощью битовой
                маски. Значения битов маски описаны в таблице:

            Число - Описание
            0 - Выключение звука двери.
            1 - Управление охраной.
            2 - Проход при блокировке.
            3 - Прием тревоги.
            4 - Постановка на охрану.
            5 - Снятие с охраны.
            6 - Проход при антипассбеке.
            7 - Гостевая карта.
            8 - Карта с привилегиями.
            9 - Выход запрещен.
            10 - Выход вне временного профиля разрешен.
            11 - Управление доступом.
            12 - -
            13 - Карта владельца.
            14 - Не использовать счетчик проходов.
            15 - Вход запрещен.
            16 - Проход без сопровождения запрещен.
            17 - Строго контролировать время возврата ключа (ключница)

            Пример: для установки идентификатору привилегий «Проход при блокировке»
            и «Проход при антипассбеке» значение параметра privilegesMask должно быть
            равно 2**2 + 2**6 = 4+64 = 68(десятичная система) = 1000100(двоичная система)

            (В функции уже реализовано)
        """
        return self.client.service.SetIdentifierPrivileges(session_id, card_code, privileges_mask)

    def get_identifier_extra_data(self, session_id: Guid, card_code: str):
        """
            session_id - Уникальный ключ сессии
            card_code - Код идентификатора карты в 16-ричном формате

            Результат: Возвращает IdentifierExData.
            Описание: Выдает сведения о дополнительных свойствах идентификатора.
        """
        return self.client.service.GetIdentifierExtraData(session_id, card_code)

    def set_identifier_extra_data(self, session_id: Guid, card_code: str, ex_data: IdentifierExData):
        """
            session_id - Уникальный ключ сессии
            card_code - Код идентификатора карты в 16-ричном формате
            ex_data - Параметры дополнительных свойств идентификатора

            Результат: Возвращает BaseResult.
            Описание: Устанавливает значения дополнительных свойств идентификатора.
        """
        return self.client.service.SetIdentifierExtraData(session_id, card_code, ex_data)

    def get_passage_roles(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив PassageRole.
            Описание: Выдает список ролей группового прохода.
        """
        return self.client.service.GetPassageRoles(session_id)

    def create_passage_role(self, session_id, role: PassageRole):
        """
            session_id - Уникальный ключ сессии
            role - Параметры создаваемой роли

            Результат: Возвращает GuidResult.
            Описание: Создает роль группового прохода с указанными параметрами.
                Возвращает ключ созданной роли. Если поле ID в структуре PassageRole равен
                Guid.Empty (00000000-0000-0000-0000-000000000000), то ID генерируется
                автоматически и возвращается. Иначе используется заданное значение ID.
        """
        return self.client.service.CreatePassageRole(session_id, dict(role))

    def save_passage_role(self, session_id: Guid, role: PassageRole):
        """
            session_id - Уникальный ключ сессии
            role - Параметры роли

            Результат: Возвращает BaseResult.
            Описание: Изменяет параметры роли.
        """
        return self.client.service.SavePassageRole(session_id, role)

    def delete_passage_role(self, session_id: Guid, role_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает BaseResult.
            Описание: Удаляет роль группового прохода с указанным ключом.
        """
        return self.client.service.DeletePassageRole(session_id, role_id)

    def get_unique_4b_card_code(self, session_id):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает StringResult.
            Описание: Возвращает уникальный неиспользуемый код идентификатора
                длиной 4 байта.
        """
        return self.client.service.GetUnique4bCardCode(session_id)

    def get_card_code_from_uid(self, session_id: Guid, uid: str, reverse_byte_order: bool):
        """
            session_id - Уникальный ключ сессии
            uid - UID карты в 16-ричном формате
            reverse_byte_order - Признак обратного порядка байт в UID

            Результат: Возвращает StringResult.
            Описание: Возвращает код карты Mifare на основе UID. Возвращаемый код
                зависит от значений параметров, задаваемых в разделе «Настройка настольных
                считывателей».
        """
        return self.client.service.GetCardCodeFromUID(session_id, uid, reverse_byte_order)

    def generate_parsec_qr_code(self, session_id: Guid, card_code: str):
        """
            session_id - Уникальный ключ сессии
            card_code - Код идентификатора

            Результат: Возвращает StringResult.
            Описание: Возвращает строку, содержащую зашифрованный код идентификатора,
            предназначенную для генерации QR-кода. Сгенерированный QR-код может
            использоваться считывателями Parsec.
        """
        return self.client.service.GenerateParsecQRCode(session_id, card_code)

    def get_advanced_qr_groups(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив QRAdvancedGroup.
            Описание: Возвращает набор групп контроллеров расширенных QR-кодов.
        """
        return self.client.service.GetAdvancedQRGroups(session_id)

    def generate_advanced_parsec_qr_code(self, session_id: Guid, qr_data: "QRAdvancedData"):
        """
            session_id - Уникальный ключ сессии
            qr_data - Права доступа генерируемого QR-кода

            Результат: Возвращает StringResult.
            Описание: Возвращает строку, предназначенную для генерации QR-кода. В
                строке в зашифрованном виде содержатся заданные права доступа.
                Сгенерированный расширенный QR-код может использоваться считывателями
                Parsec.
        """
        return self.client.service.GenerateAdvancedParsecQRCode(session_id, qr_data)

    # --------------------------------Schedules and Access Groups----------------------------------

    def get_access_schedules(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив Schedule, значение может быть AccessSchedule.
            Описание: Выдает набор расписаний доступа системы
        """
        return self.client.service.GetAccessSchedules(session_id)

    def get_worktime_schedules(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив Schedule, значение можеть быть WorktimeSchedule
            Описание: Выдает набор расписаний рабочего времени.
        """
        return self.client.service.GetWorktimeSchedules(session_id)

    def get_schedule_intervals(self, session_id: Guid, schedule_id: Guid, dt_from: datetime, dt_to: datetime):
        """
            session_id - Уникальный ключ сессии
            schedule_id - Уникальный ключ расписания
            dt_from - Начальная дата для анализа
            dt_to - Конечная дата для анализа

            Результат: Возвращает массив TimeInterval, значения могут быть WorktimeInterval.
            Описание: Выдает набор интервалов указанного расписания, ограниченный
            начальной и конечной датой. Функцией принимается во внимание только DATE
            часть параметров.
        """
        return self.client.service.GetScheduleIntervals(session_id, schedule_id, dt_from, dt_to)

    def create_access_schedule(self, session_id: Guid, schedule: "AccessSchedule", days: list["ScheduleDay"]):
        """
            session_id - Уникальный ключ сессии
            schedule - Параметры расписания
            days - Массив шаблонов дней цикла расписания

            Результат: Возвращает GuidResult.
            Описание: Создает новое расписание доступа в системе с указанными
                параметрами и заданным циклом. Возвращает ключ вновь созданного
                расписания доступа.
            При создании расписания необходимо строго соблюдать следующие условия:
                • Для недельного расписания доступа обязателен тип применения праздников
                    «Применять с заменой».
                • Для недельного расписания рабочего времени не может быть установлен
                    тип применения праздников «Применять со вставкой».
                • Для недельных расписаний массив шаблонов дней days должен содержать 7 элементов.
                • Элементы массива days должны иметь индексы дня в цикле расписания. Индекс
                    первого дня в цикле имеет значение «1». Все элементы цикла должны иметь одинаковую дату.
                • Для недельных расписаний дата начала цикла должна приходиться на
                    понедельник.
                • В цикле недельного расписания доступа не должно быть более трех
                    уникальных шаблонов дней, один из которых – выходной (не содержит
                    временных интервалов).
        """
        return self.client.service.CreateAccessSchedule(session_id, schedule, days)

    def create_worktime_schedule(self, session_id: Guid, schedule: "WorktimeSchedule", days: list["ScheduleDay"]):
        """
            session_id - Уникальный ключ сессии
            schedule - Параметры расписания
            days - Массив шаблонов дней цикла расписания

            Результат: Возвращает GuidResult.
            Описание: Создает новое расписание рабочего времени в системе с
                указанными параметрами и заданным циклом. Возвращает ключ вновь
                созданного расписания рабочего времени. При создании необходимо соблюдать
                правила, описанные в разделе функции CreateAccessSchedule.
        """
        return self.client.service.CreateWorktimeSchedule(session_id, schedule, days)

    def get_schedule(self, session_id: Guid, schedule_id: Guid):
        """
            session_id - Уникальный ключ сессии
            schedule_id - Уникальный ключ расписания

            Результат: Возвращает Schedule, результат может быть AccessSchedule или
                WorktimeSchedule.
            Описание: Возвращает информацию о расписании с указанным ключом.
        """
        return self.client.service.GetSchedule(session_id, schedule_id)

    def save_schedule(self, session_id: Guid, schedule: "Schedule"):
        """
            session_id - Уникальный ключ сессии
            schedule - Параметры расписания

            Результат: Возвращает BaseResult.
            Описание: Изменяет параметры расписания. Параметр schedule может быть
                AccessSchedule или WorktimeSchedule.
            При передаче в запросе в качестве данных расписания структуры
                AccessSchedule или WorktimeSchedule необходимо в обязательном порядке
                указывать название класса в атрибуте xsi:type элемента schedule.
        """
        return self.client.service.SaveSchedule(session_id, schedule)

    def delete_schedule(self, session_id: Guid, schedule_id: Guid):
        """
            session_id - Уникальный ключ сессии
            schedule_id - Уникальный ключ расписания, которое нужно удалить

            Результат: Возвращает BaseResult.
            Описание: Удаляет расписание с указанным ключом.
        """
        return self.client.service.DeleteSchedule(session_id, schedule_id)

    def get_schedule_details(self, session_id: Guid, schedule_id: Guid):
        """
            session_id - Уникальный ключ сессии
            schedule_id - Уникальный ключ расписания

            Результат: Возвращает массив ScheduleDay. Массив может содержать ScheduleFix
            Описание: Возвращает информацию о всех шаблонах дней и днях-поправках,
                содержащихся в расписании с указанным ключом.
        """
        return self.client.service.GetScheduleDetails(session_id, schedule_id)

    def set_schedule_days(self, session_id: Guid, schedule_id: Guid, days: list["ScheduleDay"]):
        """
            session_id - Уникальный ключ сессии
            schedule_id - Уникальный ключ расписания
            days - Массив шаблонов дней цикла расписания

            Результат: Возвращает BaseResult.
            Описание: Добавляет новый или изменяет существующий цикл (при совпадении даты начала цикла)
                расписания с указанным ключом. Параметр days должен соответствовать правилам, описанным
                в разделе функции CreateAccessSchedule.
        """
        return self.client.service.SetScheduleDays(session_id, schedule_id, days)

    def set_schedule_fix(self, session_id: Guid, schedule_id: Guid, fixes: list["ScheduleFix"]):
        """
            session_id - Уникальный ключ сессии
            schedule_id - Уникальный ключ расписания
            fixed - Массив дней-поправок расписания

            Результат: Возвращает BaseResult.
            Описание: Добавляет или изменяет существующие дни-поправки (при
                совпадении даты) в расписании с указанным ключом. Не может быть применена
                для недельного расписания доступа.
        """
        return self.client.service.SetScheduleFix(session_id, schedule_id, fixes)

    def delete_schedule_days(self, session_id: Guid, schedule_id: Guid, days: list[datetime]):
        """
            session_id - Уникальный ключ сессии
            schedule_id - Уникальный ключ расписания
            days - Массив дат

            Результат: Возвращает BaseResult.
            Описание: Удаляет цикл расписания и дни-поправки, если дата в массиве days
                совпадает с датой начала цикла или датой поправки. Недопустимо удаление
                последнего цикла в расписании.
        """
        return self.client.service.DeleteScheduleDays(session_id, schedule_id, days)

    def get_holidays(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив holyday.
            Описание: Выдает список праздников, существующих в системе.
        """
        return self.client.service.GetHolidays(session_id)

    def set_holidays(self, session_id: Guid, holidays: list[Holiday]):
        """
            session_id - Уникальный ключ сессии
            holidays - Массив праздничных дней

            Результат: Возвращает BaseResult.
            Описание: Добавляет или изменяет существующие (при совпадении дат)
                праздничные дни.
        """
        return self.client.service.SetHolidays(session_id, holidays)

    def delete_holidays(self, session_id: Guid, holidays: list[Holiday]):
        """
            session_id - Уникальный ключ сессии
            holidays - Массив праздничных дней

            Результат: Возвращает BaseResult.
            Описание: Удаляет праздничные дни с указанными параметрами.
        """
        return self.client.service.DeleteHolidays(session_id, holidays)

    def get_access_groups(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив AccessGroup.
            Описание: Возвращает массив доступных групп доступа.
        """
        return self.client.service.GetAccessGroups(session_id)

    def create_temp_access_group(self, session_id: Guid, schedule_id: Guid, territories: list[Guid]):
        """
            session_id - Уникальный ключ сессии
            schedule_id - Уникальный ключ расписания
            territories - Массив уникальных ключей территорий

            Результат: Возвращает GuidResult.
            Описание: Создает временную группу доступа типа «Подсистема доступа
                «Parsec» по заданному расписанию для доступа на заданные территории. Группа
                является временной и имеет ограниченное «время жизни». Группа
                недействительна без привязки к идентификатору сотрудника.
        """
        return self.client.service.CreateTempAccessGroup(session_id, schedule_id, territories)

    def create_access_group(self, session_id: Guid, group_name: str, schedule_id: Guid, territories: list[Guid] = None):
        """
            session_id - Уникальный ключ сессии
            group_name - Наименование группы доступа. Должно быть уникальным
            schedule_id - Уникальный ключ расписания
            territories - Массив ключей территорий

            Результат: Возвращает GuidResult.
            Описание: Создает группу доступа типа «Подсистема доступа «Parsec» по
                указанному расписанию для доступа на выбранные территории. Группа доступа
                будет иметь указанное в функции имя.
        """
        return self.client.service.CreateAccessGroup(session_id, group_name, schedule_id, territories)

    def create_vehicle_temp_access_group(self, session_id: Guid, schedule_id: Guid, territories: list[Guid]):
        """
            session_id - Уникальный ключ сессии
            schedule_id - Уникальный ключ расписания
            territories - Массив уникальных ключей территорий

            Результат: Возвращает GuidResult.
            Описание: Создает временную группу доступа типа «Автомобильный номер»
                по заданному расписанию для доступа на заданные территории. Группа является
                временной и имеет ограниченное «время жизни». Группа недействительна без
                привязки к идентификатору сотрудника.
        """
        return self.client.service.CreateVehicleTempAccessGroup(session_id, schedule_id, territories)

    def create_vehicle_access_group(self, session_id: Guid, group_name: str, schedule_id: Guid, territories: list[Guid]):
        """
            session_id - Уникальный ключ сессии
            group_name - Наименование группы доступа. Должно быть уникальным
            schedule_id - Уникальный ключ расписания
            territories - Массив ключей территорий

            Результат: Возвращает GuidResult.
            Описание: Создает группу доступа типа «Автомобильный номер» по
                указанному расписанию для доступа на выбранные территории. Группа доступа
                будет иметь указанное в функции имя.
        """
        return self.client.service.CreateVehicleAccessGroup(session_id, group_name, schedule_id, territories)

    def delete_access_group(self, session_id: Guid, access_group_id: Guid):
        """
            session_id - Уникальный ключ сессии
            access_group_id - Уникальный ключ группы доступа

            Результат: Возвращает BaseResult.
            Описание: Удаляет группу доступа с указанным ключом.
                Для удаления доступны только группы доступа типов «Подсистема доступа
                «Parsec» и «Автомобильный номер».
        """
        return self.client.service.DeleteAccessGroup(session_id, access_group_id)

    def add_sub_access_group(self, session_id: Guid, access_group_id: Guid, schedule_id: Guid, territories: list[Guid]):
        """
            session_id - Уникальный ключ сессии
            access_group_id - Уникальный ключ группы доступа
            schedule_id - Уникальный ключ расписания
            territories - Массив ключей территорий

            Результат: Возвращает GuidResult.
            Описание: Добавляет к существующей группе доступа группу компонент с
                указанным расписанием для доступа на выбранные территории.
            Если указанная территория уже используется в какой-либо группе компонент
                (в пределах одной группы доступа), то она будет удалена из этой группы компонент.
            Для изменения доступны только группы доступа типов «Подсистема доступа
                «Parsec» и «Автомобильный номер».
        """
        return self.client.service.AddSubAccessGroup(session_id, access_group_id, schedule_id, territories)

    def delete_sub_access_group(self, session_id: Guid, access_group_id: Guid, sub_group_id: Guid):
        """
            session_id - Уникальный ключ сессии
            access_group_id - Уникальный ключ группы доступа
            sub_group_id - Уникальный ключ группы компонент

            Результат: Возвращает BaseResult.
            Описание: Удаляет группу компонент с указанным ключом.
            Для изменения доступны только группы доступа типов «Подсистема доступа
            «Parsec» и «Автомобильный номер».
        """
        return self.client.service.DeleteSubAccessGroup(session_id, access_group_id, sub_group_id)

    def get_sub_access_groups(self, session_id: Guid, access_group_id: Guid):
        """
            session_id - Уникальный ключ сессии
            access_group_id - Уникальный ключ группы доступа

            Результат: Возвращает массив SubAccessGroup.
            Описание: Выдает список групп компонент (подгрупп) для указанной группы доступа.
        """
        return self.client.service.GetSubAccessGroups(session_id, access_group_id)

    def get_inherited_access_groups(self, session_id: Guid, access_group_id: Guid):
        """
            session_id - Уникальный ключ сессии
            access_group_id - Уникальный ключ группы доступа

            Результат: Возвращает массив ключей групп доступа.
            Описание: Выдает список ключей групп доступа, вложенных для указанной
                группы доступа. Ключи вложенных групп возвращаются в порядке убывания
                приоритета наследования.
        """
        return self.client.service.GetInheritedAccessGroups(session_id, access_group_id)

    def set_inherited_access_groups(self, session_id: Guid, access_group_id: Guid, inherited_groups: list[Guid]):
        """
            session_id - Уникальный ключ сессии
            access_group_id - Уникальный ключ группы доступа
            inherited_groups - Массив ключей вложенных групп доступа

            Результат: Возвращает BaseResult.
            Описание: Задает вложенные группы доступа для указанной группы.
                Приоритет наследования определяется порядком элементов в массиве.
                Для отмены наследования необходимо передать пустой массив.
                Для изменения доступны только группы доступа типов «Подсистема доступа
                «Parsec» и «Автомобильный номер».
        """
        return self.client.service.SetInheritedAccessGroups(session_id, access_group_id, inherited_groups)

    # -----------------------------Working with Applications from the Pass Office--------------------------

    def get_accepted_visitor_requests(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив VisitorRequest.
            Описание: Выдает набор заявок бюро пропусков со статусом «Одобрены».
        """
        return self.client.service.GetAcceptedVisitorRequests(session_id)

    def find_visitor_request(self, session_id: Guid, request_number: int):
        """
            session_id - Уникальный ключ сессии
            request_number - Номер заявки

            Результат: Возвращает VisitorRequest, либо null, если заявка с указанным
                номером не найдена.
            Описание: Выполняет поиск заявки с указанным номером среди заявок со
                статусом «Одобрена».
        """
        return self.client.service.FindVisitorRequest(session_id, request_number)

    def activate_visitor_request(self, session_id: Guid, request_id: Guid, card_code: str):
        """
            session_id - Уникальный ключ сессии
            request_id - Уникальный ключ заявки
            card_code - Код идентификатора

            Результат: Возвращает BaseResult.
            Описание: Выдает посетителю идентификатор с указанным кодом из пула.
                Данная функция применима только к заявкам со статусом «Одобрена».
                Переводит заявку в состояние «Активная».
        """
        return self.client.service.ActivateVisitorRequest(session_id, request_id, card_code)

    def create_visitor_request(self, session_id: Guid, request: VisitorRequest.Create):
        """
            session_id - Уникальный ключ сессии
            request - Параметры заявки

            Результат: Возвращает VisitorRequest.
            Описание: Создает заявку на посетителя и возвращает информацию о ней. В
                параметре обязательно должны быть заполнены PERSON_ID, ORGUNIT_ID,
                ADMIT_START, ADMIT_END. Все остальные параметры необязательны. Заявка
                создается со статусом «Ожидание согласования».
        """
        return self.client.service.CreateVisitorRequest(session_id, dict(request))

    def get_visitor_request(self, session_id: Guid, request_id: Guid):
        """
            session_id - Уникальный ключ сессии
            request_id - Уникальный ключ заявки

            Результат: Возвращает VisitorRequest.
            Описание: Возвращает информацию о затребованной заявке.
        """
        return self.client.service.GetVisitorRequest(session_id, request_id)

    def save_visitor_request(self, session_id: Guid, request: VisitorRequest.Update):
        """
            session_id - Уникальный ключ сессии
            request - Параметры заявки

            Результат: Возвращает BaseResult.
            Описание: Изменяет параметры в существующей заявке.
        """
        return self.client.service.SaveVisitorRequest(session_id, request)

    def delete_issued_visitor_request(self, session_id: Guid, request_id: Guid):
        """
            session_id - Уникальный ключ сессии
            request_id - Уникальный ключ заявки

            Результат: Возвращает BaseResult.
            Описание: Удаляет заявку на посетителя. Может быть удалена только заявка
                со статусом «Ожидание согласования».
        """
        return self.client.service.DeleteIssuedVisitorRequest(session_id, request_id)

    def get_issued_visitor_requests(self, session_id: Guid):
        """
            session_id - Уникальный ключ сессии

            Результат: Возвращает массив VisitorRequest.
            Описание: Возвращает массив заявок, имеющих статус «Ожидание
                согласования». Если заявок не найдено, то возвращается пустой массив.
        """
        return self.client.service.GetIssuedVisitorRequests(session_id)

    def get_visitor_requests(self, session_id: Guid, org_unit_id: Guid, dt_from: datetime,
                             issued: bool, accepted: bool, declined: bool, active: bool, completed: bool):
        """
            session_id - Уникальный ключ сессии
            org_unit_id - Уникальный ключ подразделения
            dt_from - Начальная дата для отбора заявок
            issued - Заявки со статусом «Ожидание согласования»
            accepted - Заявки со статусом «Одобрена»
            declined - Заявки со статусом «Отклонена»
            active - Заявки со статусом «Выдан пропуск»
            completed - Заявки со статусом «Закрыта»

            Результат: Массив VisitorRequest.
            Описание: Выдает все заявки в указанном подразделении, отобранные по дате
                и статусам. Функцией принимается во внимание только DATE часть параметра from.
        """
        return self.client.service.GetVisitorRequests(session_id, org_unit_id, dt_from, issued, accepted, declined,
                                                      active, completed)

    def close_all_active_visitor_requests(self, session_id: Guid, visitor_id: Guid):
        """
            session_id - Уникальный ключ сессии
            visitor_id - Уникальный ключ посетителя

            Результат: Возвращает BaseResult.
            Описание: Ищет и закрывает все активные заявки, связанные с указанным
                посетителем, идентификатор после закрытия заявки отвязывается от посетителя
                и возвращается в пул карт бюро пропусков.
        """
        return self.client.service.CloseAllActiveVisitorRequests(session_id, visitor_id)

    def close_visitor_request(self, session_id: Guid, request_id: Guid):
        """
            session_id - Уникальный ключ сессии
            request_id - Уникальный ключ заявки

            Результат: Возвращает BaseResult.
            Описание: Закрывает заявку с указанным кодом. Закрытие выполняется
                только для активных заявок (статус «Пропуск выдан»). Связанный
                идентификатор после закрытия заявки отвязывается от посетителя и
                возвращается в пул карт бюро пропусков.
        """
        return self.client.service.CloseVisitorRequest(session_id, request_id)

    def get_person_visitor_requests(self, session_id: Guid, visitor_id: Guid,
                                    issued: bool, accepted: bool,
                                    declined: bool, active: bool,
                                    completed: bool):
        """
            session_id - Уникальный ключ сессии
            visitor_id - Уникальный ключ посетителя
            issued - Заявки со статусом «Ожидание согласования»
            accepted - Заявки со статусом «Одобрена»
            declined - Заявки со статусом «Отклонена»
            active - Заявки со статусом «Выдан пропуск»
            completed - Заявки со статусом «Закрыта»

            Результат: Возвращает массив VisitorRequest.
            Описание: Возвращает массив всех заявок, доступных по области видимости,
                оформлявшихся на указанного посетителя, с возможностью отбора/фильтрации
                по всем типам статусов заявок. Если заявок не найдено, то возвращается пустой
                массив.
        """
        return self.client.service.GetPersonVisitorRequests(session_id, visitor_id, issued, accepted,
                                                            declined, active, completed)

    # --------------------------------------System events------------------------------------------------

