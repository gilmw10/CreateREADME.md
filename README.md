# CreateREADME.md

## 프로젝트 개요

CreateREADME.md는 GitHub 저장소의 메타데이터와 코드를 분석해 자동으로 README 파일을 생성해 주는 풀스택 애플리케이션입니다.  
백엔드는 **FastAPI**로 구현되어 GitHub API와 AI 모델(Groq)을 호출하고, 프론트엔드는 **React + Vite**로 사용자 인터페이스를 제공합니다.  

## 주요 기능

| 기능 | 설명 |
|------|------|
| **레포 분석** | GitHub 저장소의 메타데이터(이름, 설명, 언어, 스타 수 등)를 가져와 JSON 형태로 반환합니다. |
| **README 생성** | 분석 결과를 바탕으로 Groq AI 모델을 호출해 README 마크다운을 생성합니다. |
| **프론트엔드 UI** | 사용자가 저장소 소유자와 이름을 입력하면 분석 결과와 생성된 README를 실시간으로 미리보기합니다. |
| **CORS 지원** | 로컬 개발 환경(`localhost:5173`)에서 API 호출이 가능하도록 CORS 미들웨어를 설정했습니다. |

## 기술 스택

- **백엔드**  
  - FastAPI, Uvicorn  
  - HTTPX (GitHub API 호출)  
  - python-dotenv (환경 변수 관리)  
  - Groq (AI 모델 호출)

- **프론트엔드**  
  - React 19, Vite  
  - react-markdown, remark-gfm (마크다운 렌더링)  
  - react-syntax-highlighter (코드 하이라이트)  
  - react-router-dom (페이지 라우팅)

## 설치 방법

### 1. 백엔드 설치

```bash
# 프로젝트 루트에서
cd Backend
pip install -r requirements.txt
```

### 2. 프론트엔드 설치

```bash
# 프로젝트 루트에서
cd Frontend
npm install
```

## 실행 방법

### 백엔드 실행

```bash
# Backend 디렉터리에서
uvicorn main:app --reload
```

API는 `http://localhost:8000` 에서 접근 가능합니다.

### 프론트엔드 실행

```bash
# Frontend 디렉터리에서
npm run dev
```

프론트엔드는 `http://localhost:5173` 에서 실행됩니다.

## 환경 변수 설정

백엔드에서 필요한 환경 변수는 `.env` 파일에 정의합니다. 예시:

```
GITHUB_TOKEN=ghp_your_github_token
GROQ_API_KEY=sk-your-groq-key
```

- `GITHUB_TOKEN` : GitHub API 호출 시 인증 토큰  
- `GROQ_API_KEY` : Groq AI 모델 호출 시 인증 키  

`.env` 파일은 루트에 두고 Git에 커밋하지 않도록 `.gitignore`에 추가되어 있습니다.

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | API 상태 확인 |
| GET | `/github/{owner}/{repo}` | 저장소 분석 결과 반환 |
| GET | `/readme/{owner}/{repo}` | 분석 결과 기반 README 생성 |

## 프로젝트 구조

```
CreateREADME.md/
├── Backend/
│   ├── ai_service.py
│   ├── analyzer.py
│   ├── github_service.py
│   ├── main.py
│   ├── requirements.txt
│   └── .gitignore
├── Frontend/
│   ├── .gitignore
│   ├── README.md
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── public/
│   │   ├── favicon.svg
│   │   └── icons.svg
│   ├── src/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── assets/
│   │   │   ├── hero.png
│   │   │   ├── react.svg
│   │   │   └── vite.svg
│   │   ├── components/
│   │   │   ├── DocIcon.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Footer.module.css
│   │   │   ├── Header.jsx
│   │   │   ├── Header.module.css
│   │   │   ├── LoadingSpinner.jsx
│   │   │   ├── LoadingSpinner.module.css
│   │   │   ├── MarkdownPreview.jsx
│   │   │   ├── MarkdownPreview.module.css
│   │   │   ├── RepoForm.jsx
│   │   │   └── RepoForm.module.css
│   │   ├── hooks/
│   │   │   └── useReadme.js
│   │   ├── index.css
│   │   ├── main.jsx
│   │   ├── pages/
│   │   │   ├── CreatePage.jsx
│   │   │   ├── CreatePage.module.css
│   │   │   ├── HomePage.jsx
│   │   │   ├── HomePage.module.css
│   │   │   ├── LandingPage.jsx
│   │   │   ├── LandingPage.module.css
│   │   │   ├── ResultPage.jsx
│   │   │   └── ResultPage.module.css
│   │   ├── services/
│   │   │   └── api.js
│   │   └── vite.config.js
│   └── package.json
└── README.md
```

## 기여 방법

1. 이슈를 통해 기능 제안 또는 버그 리포트  
2. 풀 리퀘스트를 통해 코드 기여  
3. `Backend`와 `Frontend` 각각의 `README.md`를 참고하여 개발 진행  

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 확인하세요.
