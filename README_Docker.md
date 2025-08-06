# Docker 배포 가이드

이 프로젝트는 Docker를 사용하여 컨테이너화된 환경에서 실행할 수 있습니다.

## 사전 요구사항

- Docker Desktop 설치
- Docker Compose 설치 (Docker Desktop에 포함됨)

## 배포 방법

### 1. Docker Compose를 사용한 배포 (권장)

```bash
# 프로젝트 디렉토리에서 실행
docker-compose up -d
```

### 2. Docker 명령어를 사용한 배포

```bash
# 이미지 빌드
docker build -t prompt-manager .

# 컨테이너 실행
docker run -d \
  --name prompt-manager-app \
  -p 5000:5000 \
  -v $(pwd)/prompts.db:/app/prompts.db \
  -v $(pwd)/common_style:/app/common_style \
  prompt-manager
```

## 접속 방법

배포가 완료되면 다음 URL로 접속할 수 있습니다:

- **로컬 접속**: http://localhost:5000
- **네트워크 접속**: http://[서버IP]:5000

## 데이터 관리

### 데이터베이스 백업
```bash
# 데이터베이스 파일 백업
cp prompts.db prompts_backup.db
```

### 데이터베이스 복원
```bash
# 백업 파일을 현재 데이터베이스로 복원
cp prompts_backup.db prompts.db
```

## 컨테이너 관리

### 컨테이너 상태 확인
```bash
docker-compose ps
```

### 로그 확인
```bash
docker-compose logs -f prompt-manager
```

### 컨테이너 중지
```bash
docker-compose down
```

### 컨테이너 재시작
```bash
docker-compose restart
```

## 환경 변수 설정

`docker-compose.yml` 파일에서 환경 변수를 수정할 수 있습니다:

```yaml
environment:
  - FLASK_APP=prompt_manager.py
  - FLASK_ENV=production  # development로 변경하면 디버그 모드 활성화
  - COMMON_STYLE_PATH=/app/common_style
```

## 볼륨 마운트

- `./prompts.db:/app/prompts.db`: 데이터베이스 파일을 호스트와 공유
- `./common_style:/app/common_style`: CSS 파일을 컨테이너 내부로 마운트

## 문제 해결

### 1. 포트 충돌
다른 애플리케이션이 5000번 포트를 사용하는 경우:
```yaml
# docker-compose.yml에서 포트 변경
ports:
  - "8080:5000"  # 호스트 포트를 8080으로 변경
```

### 2. 권한 문제
Windows에서 볼륨 마운트 시 권한 문제가 발생하는 경우:
```bash
# PowerShell에서 실행
docker-compose up -d --force-recreate
```

### 3. CSS 파일 로드 실패
CSS 파일이 로드되지 않는 경우:
```bash
# common_style 폴더가 올바른 위치에 있는지 확인
ls -la common_style/
```

## 프로덕션 배포

프로덕션 환경에서는 다음 사항을 고려하세요:

1. **보안**: `app.secret_key`를 강력한 랜덤 키로 변경
2. **HTTPS**: 리버스 프록시(Nginx)를 사용하여 HTTPS 설정
3. **로깅**: 로그 파일을 호스트 시스템에 마운트
4. **백업**: 정기적인 데이터베이스 백업 설정 