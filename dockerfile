FROM amazon/aws-lambda-python:3.9

WORKDIR /app

RUN /var/lang/bin/python3.9 -m pip install --upgrade pip

COPY . /app

RUN pip install -r requirements.txt

RUN cp generate_mask/agnostic_mask.py /var/task/

CMD ["agnostic_mask.handler"]