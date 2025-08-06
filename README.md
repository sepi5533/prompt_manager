# 프롬프트 관리 시스템

SQLite3 데이터베이스 기반의 프롬프트 관리 웹 애플리케이션입니다. 프롬프트를 카테고리별로 관리하고, 클립보드 복사 기능을 제공합니다.

## 🚀 주요 기능

### ✨ 프롬프트 관리
- **프롬프트 등록/수정/삭제**: 완전한 CRUD 기능
- **카테고리별 분류**: 프롬프트를 카테고리별로 관리
- **태그 시스템**: 쉼표로 구분된 태그 지원
- **검색 및 필터링**: 제목, 내용, 설명으로 검색 가능

### 📋 클립보드 통합
- **원클릭 복사**: 프롬프트 내용을 클립보드에 복사
- **실시간 피드백**: 복사 성공/실패 알림
- **Cursor AI 연동**: 복사된 프롬프트를 Cursor AI에 붙여넣기

### 🎨 현대적인 UI
- **Glassmorphism 디자인**: 최신 웹 트렌드 반영
- **반응형 레이아웃**: 모바일/데스크톱 지원
- **애니메이션 효과**: 부드러운 사용자 경험
- **다크모드 지원**: 시스템 설정에 따른 자동 전환

## 📦 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 애플리케이션 실행
```bash
python prompt_manager.py
```

### 3. 웹 브라우저에서 접속
```
http://localhost:5000
```

## 🗄️ 데이터베이스 구조

### prompts 테이블
- `id`: 프롬프트 고유 ID
- `title`: 프롬프트 제목
- `content`: 프롬프트 내용
- `category`: 카테고리명
- `description`: 프롬프트 설명 (선택사항)
- `tags`: 태그 (쉼표로 구분)
- `created_at`: 생성일시
- `updated_at`: 수정일시

### categories 테이블
- `id`: 카테고리 고유 ID
- `name`: 카테고리명
- `color`: 카테고리 색상
- `created_at`: 생성일시

## 🎯 사용법

### 프롬프트 등록
1. "새 프롬프트" 버튼 클릭
2. 제목, 카테고리, 내용 입력
3. 설명과 태그는 선택사항
4. "프롬프트 등록" 버튼 클릭

### 프롬프트 복사
1. 프롬프트 카드의 "복사" 버튼 클릭
2. 프롬프트 내용이 클립보드에 복사됨
3. Cursor AI에서 Ctrl+V로 붙여넣기

### 카테고리 관리
1. "카테고리" 메뉴 클릭
2. 새 카테고리 추가 또는 기존 카테고리 삭제
3. 색상 선택으로 시각적 구분

## 🔧 기술 스택

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with Glassmorphism
- **Icons**: Font Awesome
- **Clipboard**: pyperclip

## 📁 프로젝트 구조

```
autoClipboard/
├── prompt_manager.py      # 메인 애플리케이션
├── requirements.txt       # Python 의존성
├── README.md             # 프로젝트 문서
├── templates/            # HTML 템플릿
│   ├── base.html
│   ├── index.html
│   ├── new_prompt.html
│   ├── view_prompt.html
│   ├── edit_prompt.html
│   └── categories.html
├── common_style/         # CSS 스타일 파일
│   ├── global.css
│   ├── layout.css
│   ├── components.css
│   └── animations.css
└── prompts.db           # SQLite 데이터베이스 (자동 생성)
```

## 🎨 CSS 스타일 시스템

### 디자인 토큰
- **색상 팔레트**: 2025년 트렌드 반영
- **타이포그래피**: Inter, Poppins 폰트 스택
- **간격 시스템**: 8px 그리드 기반
- **그림자**: 현대적인 그림자 시스템

### 주요 컴포넌트
- **Glassmorphism 카드**: 블러 효과와 투명도
- **모던 버튼**: 호버 애니메이션 포함
- **입력 필드**: 포커스 효과와 유효성 검사
- **배지**: 카테고리와 태그 표시

## 🔄 업데이트 로그

### v1.0.0 (2025-01-10)
- 초기 버전 릴리즈
- 기본 CRUD 기능 구현
- 클립보드 복사 기능
- 카테고리 관리 시스템
- 현대적인 UI/UX 디자인

## 🤝 기여하기

1. 이슈를 생성하여 버그나 기능 요청
2. Fork 후 Pull Request 제출
3. 코드 스타일 가이드 준수

## 📄 라이선스

MIT License

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해 주세요. 