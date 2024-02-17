from django.template import Library
from ..models import Type5, Type4, Type3, Type2, Type1, Calendar, CalDate
from datetime import datetime, timedelta

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.inclusion_tag(f"popup/popup.html")
def show_popup():
    active_type5s = Type5.objects.filter(activate__exact=True)
    active_type4s = Type4.objects.filter(activate__exact=True)
    active_type3s = Type3.objects.filter(activate__exact=True)
    active_type2s = Type2.objects.filter(activate__exact=True)
    active_type1s = Type1.objects.filter(activate__exact=True)
    active_calendar = Calendar.objects.filter(activate__exact=True)
    if active_calendar:
        print(f"Activated {Calendar.__name__} objects : {active_calendar}")
        mydates = CalDate.objects.filter(calendar__exact=active_calendar[0])
    else:
        mydates = None
    print(f"Activated {Type5.__name__} objects : {active_type5s}")
    print(f"Activated {Type4.__name__} objects : {active_type4s}")
    print(f"Activated {Type3.__name__} objects : {active_type3s}")
    print(f"Activated {Type2.__name__} objects : {active_type2s}")
    print(f"Activated {Type1.__name__} objects : {active_type1s}")

    try:
        type5 = active_type5s[0]
    except IndexError:
        type5 = None
    try:
        type4 = active_type4s[0]
    except IndexError:
        type4 = None
    try:
        type3 = active_type3s[0]
    except IndexError:
        type3 = None
    try:
        type2 = active_type2s[0]
    except IndexError:
        type2 = None
    try:
        type1 = active_type1s[0]
    except IndexError:
        type1 = None
    try:
        calendar = active_calendar[0]
    except IndexError:
        calendar = None

    if type5 is not None:
        obj = type5
    elif type4 is not None:
        obj = type4
    elif type3 is not None:
        obj = type3
    elif type2 is not None:
        obj = type2
    elif type1 is not None:
        obj = type1
    elif calendar is not None:
        obj = calendar
    else:
        obj = None

    # print(obj.__class__.__name__)
    print(mydates)
    context = {
        "dont_show_again": "다시보지않기",
        "type": obj.__class__.__name__,
        "obj": obj,
    }
    if active_calendar:
        context.update(
            {
                "mydates": mydates,
                "default_date": set_default_date().strftime("%Y-%m-%d"),
            }
        )
    logger.info(context)
    return context


def set_default_date(date=25) -> datetime:
    """
    full calendar의 defaultDate를 설정하는 함수
    date 인자 이후의 날짜는 다음달을 표시하도록 default day를 다음달로 반환한다.
    """
    today = datetime.today()
    if today.day >= date:
        return today + timedelta(days=7)
    else:
        return today
