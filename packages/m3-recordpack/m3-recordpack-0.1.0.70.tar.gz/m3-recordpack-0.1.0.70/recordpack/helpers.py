import collections

from m3.actions import (
    Action,
)


def make_action(
    url,
    run_method,
    shortname='',
    acd=None,
    classname='SimpleAction',
    bind_run=False,
    bind_acd=False,
    need_atomic=None,
    category=None,
    need_authorize=True,
):
    """Конструктор Action'ов.

    Позволяет создать экшен без непосредственного объявления его класса.
    Пример:

    .. code-block:: python

        from m3.actions import ACD

        def run_implementation(action, request, context):
            pass

        def acd_implementation():
            return (
                ACD(name="int_param", type=int, required=True),
            )

        action = make_action(
            '/action_url',
            run_implementation,
            acd=acd_implementation,
            bind_run=True)

    Args:
        url: URL action'а.
        run_method: Аналог метода run в action.
        shortname: Уникальное имя action, по которому к нему можно получить быстрый доступ.
        acd: Метод объявляющий список правил извлечения параметров (ActionContextDeclaration).
        classname: Имя класса, которое примет созданный экшн, по-умолчанию: `SimpleAction`.
        bind_run: Флаг, указывающий на необходимость передачи методу в `run_method` ссылки на сам action (self).
        bind_acd: Флаг, указывающий на необходимость передачи методу в `acd` ссылки на сам action (self).
        need_atomic: Флаг, указывающий на необходимость оборачивания в atomic.
        category: Категория поведения, может использоваться для разделения acion на "читающие" и "пишущие", чтобы
            роутить запросы к разным БД.
        need_authorize: Флаг, указывающий на необходимость авторизации для доступа к action.

    Returns:
        Дочерний класс от :class:`Action`
    """

    # Генерация класса экшена
    cls = type(
        classname,
        (Action,),
        dict(
            url=url,
            shortname=shortname,
        )
    )
    action = cls()
    # Привязка функций реализующих логику экшена
    action.run = bind_run and run_method.__get__(action) or run_method
    action.need_authorize = need_authorize

    if acd is not None:
        action.context_declaration = bind_acd and acd.__get__(action) or acd

    if need_atomic is not None:
        action.need_atomic = need_atomic

    if category is not None:
        action.category = category

    return action


def init_component(instance, **kwargs):
    """Инициализация атрибутов экземпляра.

    Используется для удобной инициализации атрибутов через конструктор
    по средством kwargs.

    Args:
        instance: Объект класса.
    """

    for attr, val in kwargs.items():
        instance.__setattr__(attr, val)


def sequenceable(item):
    """Преобразование в последовательность.

    Если элемент поддерживает интерфейс Sequence (за исключением строк),
    то он преобразуется к кортежу, в ином случае элемент обертвается в
    кортеж.

    .. note::
        Если передан None, то вернется пустой кортеж.

    Args:
        item: Изначальный объект.

    Returns:
        Сфомированная последовательность.
    """

    if isinstance(item, str):
        seq = (item,)
    elif item is None:
        seq = ()
    elif isinstance(item, collections.Iterable):
        seq = tuple(item)
    else:
        seq = (item,)

    return seq


class AttributedDict(dict):
    """Словарь, позволяющий обращаться к своим элементам как к атрибутам объекта."""

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, key, value):
        self[key] = value
