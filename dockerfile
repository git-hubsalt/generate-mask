FROM amazon/aws-lambda-python:3.9

RUN /var/lang/bin/python3.9 -m pip install --upgrade pip

RUN yum install git -y

RUN git clone https://github.com/git-hubsalt/generate-mask.git

RUN pip install -r generate-mask/requirements.txt

RUN cp generate-mask/generate_mask/agnostic_mask.py /var/task/

CMD ["agnostic_mask.handler"]