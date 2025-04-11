from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.database import Base  # ✅ 데이터베이스 Base
from app import models         # ✅ 모델 임포트

# ✅ Alembic이 자동으로 테이블을 감지하도록 설정
target_metadata = Base.metadata

# Alembic 설정 객체 불러오기
config = context.config

# 로그 설정 로딩
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """오프라인 모드로 마이그레이션 수행 (SQL 스크립트 생성용)"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """온라인 모드로 마이그레이션 수행 (DB에 직접 반영)"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# 실행 모드에 따라 마이그레이션 실행
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
