# CreateREADME.md

## 프로젝트 소개

`CreateREADME.md`는 개발자가 GitHub 저장소의 README.md 파일을 쉽고 빠르게 생성할 수 있도록 돕는 웹 기반 애플리케이션입니다. 저장소 URL을 입력하면, 애플리케이션이 해당 저장소의 코드, 파일 구조, 의존성 등을 분석하고, Google Gemini AI 모델의 강력한 기능을 활용하여 전문적이고 구조화된 README.md 초안을 자동으로 생성해 줍니다. 이 프로젝트는 문서화 작업을 간소화하고, 모든 개발자가 양질의 README 파일을 가질 수 있도록 지원하는 것을 목표로 합니다.

## 주요 기능

*   **GitHub 저장소 분석:** 입력된 GitHub 저장소 URL을 통해 저장소의 파일 구조, 사용된 언어, 주요 의존성 등을 심층적으로 분석합니다.
*   **AI 기반 README 생성:** Google Gemini AI 모델을 사용하여 분석된 데이터를 기반으로 `프로젝트 소개`, `주요 기능`, `기술 스택`, `설치 및 실행 방법`, `프로젝트 구조` 등 표준 README 섹션을 포함한 초안을 지능적으로 생성합니다.
*   **실시간 마크다운 미리보기:** 생성된 README.md 콘텐츠를 실시간으로 마크다운 형식으로 렌더링하여 최종 결과물을 즉시 확인할 수 있습니다.
*   **사용자 친화적인 웹 인터페이스:** React로 구축된 직관적인 UI를 통해 저장소 URL 입력, 결과 확인 및 복사/다운로드까지 원활한 사용자 경험을 제공합니다.
*   **다양한 마크다운 기능 지원:** `react-markdown`, `remark-gfm`, `react-syntax-highlighter` 라이브러리를 활용하여 코드 블록 하이라이팅, 표, 체크리스트 등 GitHub Flavored Markdown (GFM)을 풍부하게 표현합니다.

## 기술 스택

이 프로젝트는 다음과 같은 기술 스택으로 구성된 풀스택 애플리케이션입니다.

### 백엔드 (Backend)

*   **언어:** Python
*   **프레임워크:** FastAPI
*   **웹 서버:** Uvicorn
*   **AI 통합:** Google Gemini API (with `google-genai` 라이브러리)
*   **HTTP 클라이언트:** `httpx` (GitHub API 통신 등)
*   **환경 변수 관리:** `python-dotenv`

### 프론트엔드 (Frontend)

*   **언어:** JavaScript
*   **프레임워크:** React.js
*   **빌드 도구:** Vite
*   **라우팅:** `react-router-dom`
*   **마크다운 렌더링:** `react-markdown`
*   **코드 하이라이팅:** `react-syntax-highlighter`
*   **GFM 확장:** `remark-gfm`

## 설치 방법

프로젝트를 로컬 환경에 설치하고 실행하기 위한 단계별 지침입니다.

### 전제 조건

*   Git
*   Python 3.8+
*   Node.js 18+ 및 npm (또는 Yarn)
*   Google Gemini API Key: [Google AI Studio](https://aistudio.google.com/app/apikey)에서 발급받아야 합니다.

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/CreateREADME.md.git
cd CreateREADME.md
```

### 2. 백엔드 설정

```bash
cd Backend
```

가상 환경을 생성하고 활성화합니다.

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

의존성을 설치합니다.

```bash
pip install -r requirements.txt
```

`.env` 파일을 생성하고 Google Gemini API 키를 추가합니다.

```
# Backend/.env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

`YOUR_GEMINI_API_KEY` 부분을 발급받은 실제 API 키로 교체해야 합니다.

### 3. 프론트엔드 설정

```bash
cd ../Frontend
```

의존성을 설치합니다.

```bash
npm install
# 또는 yarn install
```

프론트엔드 `.env` 파일을 생성하고 백엔드 API 주소를 설정합니다.

```
# Frontend/.env
VITE_API_URL="http://localhost:8000" # 백엔드가 실행될 주소
```

## 실행 방법

백엔드와 프론트엔드를 각각 실행해야 합니다.

### 1. 백엔드 실행

`Backend` 디렉토리에서 다음 명령어를 실행합니다. 가상 환경이 활성화되어 있는지 확인하세요.

```bash
cd Backend
# 가상 환경이 활성화되지 않았다면:
# Windows: .\venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

백엔드 서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

### 2. 프론트엔드 실행

새로운 터미널을 열고 `Frontend` 디렉토리에서 다음 명령어를 실행합니다.

```bash
cd Frontend
npm run dev
# 또는 yarn dev
```

프론트엔드 개발 서버는 일반적으로 `http://localhost:5173`에서 실행됩니다. 브라우저를 열어 이 주소로 접속하면 애플리케이션을 사용할 수 있습니다.

## 프로젝트 구조

프로젝트의 주요 디렉토리 및 파일 구조는 다음과 같습니다.

```
CreateREADME.md/
├── Backend/
│   ├── analyzer.py                 # GitHub 저장소 분석 로직
│   ├── gemini_service.py           # Google Gemini API 호출 및 응답 처리
│   ├── github_service.py           # GitHub API 호출 및 데이터 가져오기
│   ├── main.py                     # FastAPI 애플리케이션 엔트리 포인트 (API 라우트 정의)
│   ├── requirements.txt            # Python 의존성 목록
│   └── .env.example                # 환경 변수 예시
├── Frontend/
│   ├── public/
│   │   ├── favicon.svg             # 파비콘 아이콘
│   │   └── icons.svg               # SVG 아이콘 컬렉션
│   ├── src/
│   │   ├── assets/                 # 이미지, 로고 등 정적 자산
│   │   ├── components/             # 재사용 가능한 React UI 컴포넌트
│   │   │   ├── DocIcon.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── LoadingSpinner.jsx  # 로딩 스피너
│   │   │   ├── MarkdownPreview.jsx # 마크다운 미리보기 컴포넌트
│   │   │   └── RepoForm.jsx        # 저장소 URL 입력 폼
│   │   ├── hooks/
│   │   │   └── useReadme.js        # README 데이터 관리를 위한 커스텀 훅
│   │   ├── pages/                  # 애플리케이션의 각 페이지 컴포넌트
│   │   │   ├── CreatePage.jsx      # README 생성 페이지
│   │   │   ├── HomePage.jsx        # 메인/시작 페이지
│   │   │   ├── LandingPage.jsx     # 랜딩 페이지
│   │   │   └── ResultPage.jsx      # 생성된 README 결과 페이지
│   │   ├── services/
│   │   │   └── api.js              # 백엔드 API와의 통신 로직
│   │   ├── App.css
│   │   ├── App.jsx                 # 메인 애플리케이션 컴포넌트
│   │   ├── index.css               # 전역 스타일
│   │   └── main.jsx                # React 애플리케이션 엔트리 포인트
│   ├── .gitignore                  # Git 무시 파일
│   ├── eslint.config.js            # ESLint 설정
│   ├── index.html                  # HTML 템플릿
│   ├── package-lock.json           # npm 의존성 잠금 파일
│   ├── package.json                # Node.js 의존성 및 스크립트
│   └── vite.config.js              # Vite 빌드 설정
└── .gitignore                      # Git 무시 파일
```
