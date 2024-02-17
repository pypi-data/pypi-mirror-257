django-demian_parts
==========

django-demian_parts is a Django app to use for demiansoft. 
(현재 analytics와 popup 구현)

Quick start
------------

1. Add "demian_parts" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'demian_parts',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
# 팝업 모듈을 넣기 위해
{% load popup_tags %}
{% show_popup %}

# analytics 모듈을 넣기 위해
{% load analytics_tags %}
{% make_analytics %}
```

3. 데이터 베이스를 생성한다.
```commandline
python manage.py makemigrations demian_parts
python manage.py migrate
python manage.py createsuperuser
```

4. 프로젝트의 urls.py에 summernote를 추가하고 media 경로를 추가한다.
```python
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

5. settings.py에 필요한 설정을 추가한다.
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
X_FRAME_OPTIONS = 'SAMEORIGIN'
```

6. http://your_url/admin/에 접속하여 popup을 생성한다.

* context example (analytics 예시)
```python
context = {
    'analytics': {
        'google_id': "UA-16872449-1",
        'naver_id': "feadf9e1b55868",
        'ads_id': "AW-1018052709",
        'ads_conversion': {
            'cta': "HdrUCNiXsd8DEOWAueUD",
            'naver': "91WCCPvk6fEBEOWAueUD",
            'call': "pThXCJXpsN8DEOWAueUD",
        },
    },
}
```

* 팝업창을 올바르게 보여주기 위해서는 bootstrap5와 bootstrap-icon이 필요하다.
* css 변수로 폰트와 색상이 설정되어 있어야한다.
- font_link에 family=Gugi 를 추가해야 한다. "family=Gugi&" 
```css
:root {
  --font-default: ...;
  --font-primary: ...;
  --font-secondary: ...;
}

:root {
  --color-default: #364d59;
  --color-primary: #feb900;
  --color-secondary: #52565e;
} 
```
