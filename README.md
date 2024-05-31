
# 실시간 주문 처리 시스템 구축

이 프로젝트는 Kafka를 중심으로 실시간 데이터 파이프라인을 구축하여 대용량 메시지를 처리하고, 이를 기반으로 주문 처리를 하는 시스템을 개발합니다. 이 시스템은 전자상거래 플랫폼의 주문 데이터를 실시간으로 처리하고, 모니터링하며 분석하는 데 중점을 둡니다.

## 주요 구성 요소

1. **Kafka 클러스터 구축 및 운영**
2. **Kafka Connect를 통한 데이터 수집**
3. **Kafka Streams를 통한 실시간 데이터 처리**
4. **데이터베이스 변경 데이터 캡처 (CDC)**
5. **모니터링 및 알림 시스템**

## 사용된 기술

- Docker
- Kafka
- Zookeeper
- MySQL
- Kafka Connect
- Debezium
- Prometheus
- Grafana

## 설치 및 실행

### 1. Docker 및 Docker Compose 설치

프로젝트를 실행하기 전에 Docker와 Docker Compose가 설치되어 있어야 합니다. 설치 방법은 [Docker 공식 문서](https://docs.docker.com/get-docker/)를 참고하세요.

### 2. 프로젝트 클론

프로젝트를 클론합니다:
```bash
git clone https://github.com/your-repository/your-project.git
cd your-project
```





### 프로젝트 구조와 데이터 플로우

#### 1. 데이터 소스 (MySQL)
- **역할**: 주문 데이터를 저장합니다.
- **데이터 플로우**: MySQL 데이터베이스에서 주문 데이터가 생성되면 Kafka Connect를 통해 Kafka로 스트리밍됩니다.

#### 2. Kafka Connect
- **역할**: MySQL과 Kafka 간의 데이터 통합을 관리합니다.
- **데이터 플로우**: MySQL의 데이터를 읽어 Kafka 토픽에 게시합니다.
- **커넥터 설정**: `connectors/mysql-source-connector.json` 파일을 사용하여 설정합니다.

#### 3. Kafka
- **역할**: 메시지 브로커로, 데이터 스트리밍을 처리합니다.
- **데이터 플로우**: Kafka 토픽에 게시된 메시지를 스트리밍 처리 애플리케이션이 소비합니다.

#### 4. Kafka Streams
- **역할**: 실시간 데이터 처리를 수행합니다.
- **데이터 플로우**: Kafka 토픽에서 데이터를 소비하여 실시간으로 처리하고, 결과를 다른 Kafka 토픽에 게시합니다.
- **스트림 애플리케이션**: `src/streaming_app.py` 또는 `src/StreamingApp.java` 파일에 구현합니다.

#### 5. Debezium
- **역할**: MySQL 데이터베이스의 변경 사항을 Kafka로 스트리밍합니다.
- **데이터 플로우**: MySQL에서 발생하는 변경 사항을 실시간으로 캡처하여 Kafka 토픽에 게시합니다.

#### 6. Prometheus와 Grafana
- **역할**: 모니터링과 시각화를 제공합니다.
- **데이터 플로우**: Prometheus가 Kafka와 Kafka Connect의 메트릭을 수집하고, Grafana가 이를 시각화합니다.

### 전체 데이터 플로우

1. **MySQL**: 주문 데이터가 생성됩니다.
2. **Kafka Connect**: MySQL에서 데이터를 읽어 `mysql-orders` Kafka 토픽에 게시합니다.
3. **Kafka**: `mysql-orders` 토픽에 데이터가 게시됩니다.
4. **Kafka Streams**: `mysql-orders` 토픽에서 데이터를 소비하여 처리한 후, `processed-orders` 토픽에 게시합니다.
5. **Debezium**: MySQL 데이터베이스의 변경 사항을 캡처하여 Kafka 토픽에 게시합니다.
6. **Prometheus**: Kafka와 Kafka Connect의 메트릭을 수집합니다.
7. **Grafana**: Prometheus에서 수집된 메트릭을 시각화하여 모니터링합니다.

### 프로젝트 실행 방법

#### 1. 프로젝트 클론 및 디렉토리 이동
```bash
git clone https://github.com/your-repository/your-project.git
cd your-project
```

#### 2. Docker Compose 파일 준비
`docker-compose.yml` 파일과 `prometheus.yml` 파일을 준비합니다.

#### 3. Docker Compose 실행
아래 명령어를 실행하여 모든 서비스를 시작합니다:
```bash
docker-compose up -d
```

#### 4. MySQL 초기화
MySQL 컨테이너가 실행된 후, MySQL 초기화 스크립트를 실행하여 데이터베이스와 테이블을 생성합니다:
```bash
docker exec -i mysql mysql -u root -pmyrootpass < mysql-init/init.sql
```

#### 5. Kafka Connect 및 Debezium 설정
Kafka Connect REST API를 사용하여 커넥터를 등록합니다:
```bash
curl -X POST -H "Content-Type: application/json" --data @connectors/mysql-source-connector.json http://localhost:8083/connectors
curl -X POST -H "Content-Type: application/json" --data @connectors/debezium-mysql-connector.json http://localhost:8084/connectors
```

#### 6. Kafka Streams 애플리케이션 실행
Kafka Streams 애플리케이션을 실행합니다. (Python 예시):
```bash
python src/streaming_app.py
```
(Java 예시의 경우 Java 프로젝트로 실행합니다)

#### 7. Prometheus 및 Grafana 설정
Prometheus와 Grafana가 실행된 후, Grafana 웹 인터페이스 (`http://localhost:3000`)에 접속하여 데이터 소스를 Prometheus로 설정하고 대시보드를 생성합니다.

### 디렉토리 구조

```bash
.
├── README.md
├── docker-compose.yml
├── prometheus.yml
├── connectors/
│   ├── mysql-source-connector.json
│   └── debezium-mysql-connector.json
├── src/
│   └── streaming_app.py
├── env/
│   └── kafka.env
├── mysql-init/
│   └── init.sql
└── scripts/
    └── start.sh
```

### 각 파일 설명

- `README.md`: 프로젝트 설명서.
- `docker-compose.yml`: Docker Compose 설정 파일.
- `prometheus.yml`: Prometheus 설정 파일.
- `connectors/mysql-source-connector.json`: Kafka Connect MySQL 소스 커넥터 설정 파일.
- `connectors/debezium-mysql-connector.json`: Debezium MySQL 커넥터 설정 파일.
- `src/streaming_app.py`: Kafka Streams 애플리케이션 코드 (Python 예시).
- `env/kafka.env`: Kafka 환경 변수 파일.
- `mysql-init/init.sql`: MySQL 초기화 스크립트.
- `scripts/start.sh`: 프로젝트 시작 스크립트.
