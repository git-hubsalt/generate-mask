FROM amazon/aws-lambda-python:3.9

# Lambda 작업 디렉토리로 설정 (기본적으로 /var/task)
WORKDIR /var/task

# pip 업그레이드
RUN /var/lang/bin/python3.9 -m pip install --upgrade pip

# 필요한 시스템 패키지 설치 (OpenGL 라이브러리 포함)
RUN yum install -y \
    mesa-libGL \
    mesa-libGL-devel \
    libXtst \
    libXrender \
    libXext

# 로컬 디렉토리의 모든 파일을 Lambda 작업 디렉토리로 복사
COPY . /var/task

# 필요한 Python 패키지 설치
RUN pip install -r requirements.txt

# CMD 설정 (핸들러 함수 위치)
CMD ["agnostic_mask.handler"]
