# Common Style Library - 공통 스타일 라이브러리

## 📋 개요

이 라이브러리는 최신 웹 트렌드(2024-2025)를 반영한 현대적인 CSS 스타일 시스템입니다. Glassmorphism, 마이크로 인터랙션, 부드러운 애니메이션, 그리고 향상된 접근성을 제공합니다.

## 🎨 주요 특징

### ✨ 최신 웹 트렌드 반영
- **Glassmorphism 효과**: 블러와 투명도를 활용한 현대적인 디자인
- **마이크로 인터랙션**: 부드럽고 자연스러운 사용자 경험
- **그라디언트와 블러**: 시각적으로 매력적인 배경과 효과
- **현대적인 색상 팔레트**: 2025년 트렌드를 반영한 색상 체계

### 🌙 다크모드 지원
- 시스템 다크모드 자동 감지
- 일관된 색상 전환
- 향상된 가독성

### ♿ 접근성 우선
- 고대비 모드 지원
- 모션 감소 설정 준수
- 키보드 네비게이션 지원
- 스크린 리더 최적화

### 📱 반응형 디자인
- 모바일 우선 접근법
- 유연한 그리드 시스템
- 터치 친화적 인터페이스

## 📁 파일 구조

```
common_style/
├── global.css          # 전역 스타일 및 CSS 변수
├── layout.css          # 레이아웃 컴포넌트
├── components.css      # 현대적인 UI 컴포넌트
├── animations.css      # 애니메이션 및 인터랙션
├── button.css          # 버튼 스타일
├── card.css           # 카드 컴포넌트
├── form.css           # 폼 요소
├── modal.css          # 모달 및 다이얼로그
├── navigation.css     # 네비게이션 요소
├── table.css          # 테이블 스타일
├── utility.css        # 유틸리티 클래스
├── loading-spinner.css # 로딩 스피너
└── README.md          # 이 파일
```

## 🎯 주요 컴포넌트

### Glassmorphism 컴포넌트
```css
.modern-card {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-3xl);
}
```

### 현대적인 버튼
```css
.btn-glass {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  transition: all var(--transition-bounce);
}
```

### 애니메이션 클래스
```css
.animate-fade-in-up { /* 페이드인 업 애니메이션 */ }
.hover-float:hover { /* 호버 시 플로팅 효과 */ }
.scroll-trigger { /* 스크롤 트리거 애니메이션 */ }
```

## 🎨 색상 시스템

### 주요 색상
- **Primary**: `#6366f1` (인디고)
- **Secondary**: `#8b5cf6` (바이올렛)
- **Success**: `#10b981` (에메랄드)
- **Warning**: `#f59e0b` (앰버)
- **Danger**: `#ef4444` (레드)
- **Info**: `#06b6d4` (사이안)

### 그레이 스케일
- **Gray-50**: `#fafafa`
- **Gray-100**: `#f5f5f5`
- **Gray-900**: `#171717`
- **Gray-950**: `#0a0a0a`

## 📐 타이포그래피

### 폰트 스택
```css
--font-family-base: 'Inter', 'Segoe UI', 'Malgun Gothic', sans-serif;
--font-family-mono: 'JetBrains Mono', 'Fira Code', monospace;
--font-family-display: 'Poppins', 'Inter', sans-serif;
```

### 폰트 크기
- **xs**: 0.75rem (12px)
- **sm**: 0.875rem (14px)
- **base**: 1rem (16px)
- **lg**: 1.125rem (18px)
- **xl**: 1.25rem (20px)
- **2xl**: 1.5rem (24px)
- **3xl**: 1.875rem (30px)
- **4xl**: 2.25rem (36px)
- **5xl**: 3rem (48px)

## 🎭 애니메이션

### 진입 애니메이션
- `animate-fade-in-up`: 아래에서 위로 페이드인
- `animate-fade-in-down`: 위에서 아래로 페이드인
- `animate-scale-in`: 스케일 인 애니메이션
- `animate-slide-in-left`: 왼쪽에서 슬라이드인

### 호버 애니메이션
- `hover-float`: 플로팅 효과
- `hover-pulse`: 펄스 효과
- `hover-bounce`: 바운스 효과
- `hover-glow`: 글로우 효과

### 로딩 애니메이션
- `animate-spin`: 회전 애니메이션
- `animate-shimmer`: 시머 효과
- `animate-dots`: 점 애니메이션

## 🎪 마이크로 인터랙션

### 호버 효과
```css
.micro-hover:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

### 스케일 효과
```css
.micro-scale:hover {
  transform: scale(1.05);
}
```

### 회전 효과
```css
.micro-rotate:hover {
  transform: rotate(5deg);
}
```

## 📱 반응형 브레이크포인트

```css
/* 모바일 */
@media (max-width: 480px) { }

/* 태블릿 */
@media (max-width: 768px) { }

/* 데스크톱 */
@media (max-width: 1200px) { }
```

## 🌙 다크모드

시스템 다크모드 자동 감지 및 지원:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-primary: var(--color-gray-900);
    --color-text-primary: var(--color-gray-100);
  }
}
```

## ♿ 접근성

### 고대비 모드
```css
@media (prefers-contrast: high) {
  /* 고대비 색상 설정 */
}
```

### 모션 감소
```css
@media (prefers-reduced-motion: reduce) {
  /* 애니메이션 비활성화 */
}
```

## 🚀 사용법

### 1. CSS 파일 임포트
```html
<link rel="stylesheet" href="common_style/global.css">
<link rel="stylesheet" href="common_style/layout.css">
<link rel="stylesheet" href="common_style/components.css">
<link rel="stylesheet" href="common_style/animations.css">
```

### 2. 기본 레이아웃 구조
```html
<div class="main-layout">
  <header class="main-header">
    <div class="header-content">
      <h1 class="header-title">제목</h1>
      <nav class="header-nav">
        <button class="nav-btn">메뉴</button>
      </nav>
    </div>
  </header>
  
  <main class="main-content">
    <div class="left-panel">
      <!-- 콘텐츠 -->
    </div>
    <div class="right-panel">
      <!-- 콘텐츠 -->
    </div>
  </main>
  
  <footer class="status-bar">
    <div class="status-content">
      <span class="status-text">상태</span>
    </div>
  </footer>
</div>
```

### 3. 컴포넌트 사용
```html
<!-- 현대적인 카드 -->
<div class="modern-card animate-fade-in-up">
  <div class="modern-card-header">
    <h3 class="modern-card-title">카드 제목</h3>
    <span class="modern-card-badge">뱃지</span>
  </div>
  <p>카드 내용</p>
</div>

<!-- 글래스모피즘 버튼 -->
<button class="btn-glass btn-glass-primary micro-hover">
  버튼
</button>

<!-- 현대적인 입력 필드 -->
<div class="input-group">
  <input type="text" class="input-glass" placeholder="입력하세요">
  <span class="input-group-icon">🔍</span>
</div>
```

## 🎨 커스터마이징

### CSS 변수 재정의
```css
:root {
  --color-primary: #your-color;
  --font-family-base: 'Your Font', sans-serif;
  --spacing-4: 1.5rem;
}
```

### 컴포넌트 확장
```css
.custom-card {
  @extend .modern-card;
  background: linear-gradient(135deg, #your-gradient);
}
```

## 📊 성능 최적화

### CSS 최적화
- CSS 변수 활용으로 일관성 유지
- 불필요한 중첩 제거
- 효율적인 선택자 사용

### 애니메이션 최적화
- `transform`과 `opacity` 활용
- `will-change` 속성 적절히 사용
- GPU 가속 활용

## 🔧 개발 도구

### 브라우저 지원
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### 개발 환경
- CSS Grid 지원
- Flexbox 지원
- CSS 변수 지원
- backdrop-filter 지원

## 📝 업데이트 로그

### v2.0.0 (2025-01-10)
- 최신 웹 트렌드 반영
- Glassmorphism 효과 추가
- 마이크로 인터랙션 강화
- 애니메이션 시스템 개선
- 다크모드 지원 향상
- 접근성 개선

### v1.0.0 (2024-12-01)
- 초기 버전 릴리즈
- 기본 컴포넌트 제공
- 반응형 디자인 구현

## 🤝 기여하기

1. 이슈 등록
2. 브랜치 생성
3. 변경사항 커밋
4. 풀 리퀘스트 생성

## 📄 라이선스

MIT License - 자유롭게 사용 가능

## 📞 문의

프로젝트 관련 문의사항이 있으시면 이슈를 등록해 주세요.

---

**참고**: 이 라이브러리는 최신 웹 표준과 접근성 가이드라인을 준수하여 개발되었습니다. 