FROM python:3

WORKDIR /code


COPY ./ /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "application:coupon_issurance_application", "--host", "0.0.0.0", "--port", "8000"]