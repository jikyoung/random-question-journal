# 📝 랜덤 질문 생성기 + 기록 서비스

## 💡 프로젝트 소개
매일 하나의 질문을 제공하고, 사용자는 해당 질문에 대해 답변을 남기며 성찰의 기록을 쌓아가는 서비스입니다. 
FastAPI 기반으로 개발되었으며, 카카오 로그인, 질문 저장, PDF 다운로드, 관리자 질문 관리 기능을 제공합니다.

## ⚙️ 주요 기능
- ✅ 랜덤 질문 제공 (1일 1문)
- ✅ 카카오 로그인/로그아웃
- ✅ 이메일 회원가입 및 로그인
- ✅ 답변 저장 및 질문/답변 함께 보기
- ✅ 답변 PDF 다운로드 기능
- ✅ 관리자 페이지에서 질문 추가/삭제 가능

## 🛠 기술 스택
- Backend: **FastAPI**, **SQLAlchemy**, **SQLite**
- Frontend: **HTML + Tailwind CSS + Jinja2 템플릿**
- 기타: **카카오 소셜 로그인**, **WeasyPrint PDF 변환**

## 📁 디렉토리 구조
```
random-question-journal/
├── .env
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── app/
│   ├── main.py
│   ├── database.py
│   ├── crud.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth_utils.py
│   ├── utils/
│   │   └── pdf.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── answers.html
│   │   ├── admin_questions.html
│   │   └── new_question.html
│   └── routers/
│       ├── pages.py
│       ├── answers.py
│       ├── auth.py
│       ├── questions.py
│       └── admin_questions.py
├── db.sqlite3
├── project_tree.py
├── questions.json
├── requirements.txt
├── run.py
└── seed_questions.py
```

## ✅ 실행 방법
```bash
# 가상환경 활성화 후 아래 명령 실행
uvicorn app.main:app --reload
📌 현재 구현 상태 (2025.04.11 기준)
	• FastAPI 기반 앱 기본 구조 구축 완료
	• Alembic 기반 DB 마이그레이션 적용
	• 질문 DB 설계 및 CRUD 기능 구현
	• 이메일 회원가입 및 로그인 기능 추가
	• 카카오 로그인 연동 구현
	• 질문 UI 출력 및 답변 저장
	• 답변 PDF 저장 기능 및 UI 개선
	• 질문 중복 방지 및 고정 로직 적용
	• "또 다른 질문에 답하기" 기능 구현
	• 답변 조회 페이지에서 질문/답변 함께 표시

✨ 다음 목표
	• 사용자 게시판 기능 (자유롭게 글 등록 및 답변 공유)
	• 질문 추천 알고리즘 도입 (답변 기반 개인화)
	• 출석 기반 보상 시스템 (무료 PDF or 질문 해금)
	• 그림일기 기능 도입 (AI 그림 생성 or 직접 업로드)
	• 친구 초대 기능 (카카오톡 or 사용자 ID 기반)
	• 전체 UI/디자인 개선 (모바일 대응 포함)
	• 자체 회원가입 시 이메일 인증 기능 추가
	• 서비스 배포 및 도메인 연결 (Render, Railway 등)
	• PDF 다운로드 유료화 또는 광고 수익화 모델 도입
🙌 개발자
	• GitHub: @jikyoung
##
