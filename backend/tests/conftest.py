import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.models.models import User, UserProfile
from app.core.security import get_password_hash

# Create an isolated temporary SQLite database for testing
temp_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
TEST_DATABASE_URL = f"sqlite:///{temp_db_file.name}"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    
    # Seed baseline test users into isolated test DB
    db = TestingSessionLocal()
    demo_user = User(
        email="demo@codepilot.dev",
        hashed_password=get_password_hash("Demo1234!"),
        full_name="Arjun Sharma",
        role="USER",
        is_active=True
    )
    admin_user = User(
        email="admin@codepilot.dev",
        hashed_password=get_password_hash("Admin1234!"),
        full_name="System Administrator",
        role="ADMIN",
        is_active=True
    )
    db.add(demo_user)
    db.add(admin_user)
    db.commit()
    
    # Add profile for demo user
    profile = UserProfile(
        user_id=demo_user.id,
        target_role="Backend Software Engineer",
        experience_level="Intermediate",
        learning_goals="Build mastery over complex DSA and distributed architectures.",
        weekly_hours=8,
        onboarding_completed=True
    )
    db.add(profile)
    db.commit()
    db.close()
    
    yield
    
    # Teardown
    Base.metadata.drop_all(bind=engine)
    try:
        os.unlink(temp_db_file.name)
    except Exception:
        pass

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)
