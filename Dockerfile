FROM python:3.12-alpine AS builder

RUN apk add --no-cache libgcc mariadb-connector-c pkgconf mariadb-dev postgresql-dev linux-headers

WORKDIR /opt/ovpn-generator
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /opt/ovpn-generator/
COPY manage.py /opt/ovpn-generator/
COPY django_ovpn_generator /opt/ovpn-generator/django_ovpn_generator/
COPY django_vpn_manager /opt/ovpn-generator/django_vpn_manager/

FROM builder AS install
WORKDIR /opt/ovpn-generator
ENV VIRTUAL_ENV=/opt/ovpn-generator/venv

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir -r /opt/ovpn-generator/requirements.txt

FROM install as run

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "--noreload", "0.0.0.0:8000"]
