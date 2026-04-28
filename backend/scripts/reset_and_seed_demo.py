import random
import sys
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy import inspect

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal, engine
from app.models.session import MatchResult, MatchSession, QuestionAnswer
from app.models.user import IELTSUserProfile, User, UserProfile


MATH_COUNT = 42
IELTS_COUNT = 18


NAMES = [
    "张子墨", "王雨桐", "李星辰", "赵一凡", "陈思远", "刘语涵", "黄嘉宁", "周明轩", "吴若曦", "徐景行",
    "孙可心", "马浩然", "朱清禾", "胡安然", "郭知遥", "何沐阳", "高书宁", "林逸飞", "罗芷晴", "郑博文",
    "梁欣怡", "谢云帆", "宋子衿", "唐梓豪", "许梦琪", "韩嘉禾", "冯泽宇", "邓若彤", "曹晨曦", "彭星宇",
    "曾羽辰", "田乐瑶", "董瑞泽", "袁清妍", "程诺言", "潘子越", "于芮琪", "蒋博雅", "蔡景川", "余知行",
]

MAJORS = [
    "数学与应用数学", "统计学", "计算机科学与技术", "软件工程", "信息与计算科学", "数据科学与大数据技术",
    "自动化", "电子信息工程", "金融工程", "应用物理学", "机械工程", "国际经济与贸易", "英语", "教育学",
]

GRADES = ["大一", "大二", "大三", "大四", "研一", "研二"]
GENDERS = ["男", "女"]
ROLES_MATH = ["建模手", "论文手", "编程手", "无倾向"]
ROLES_IELTS = ["听力", "阅读", "写作", "口语", "无倾向"]


def r_score(lo: float = 2.0, hi: float = 9.8) -> float:
    return round(random.uniform(lo, hi), 2)


def create_math_user(idx: int) -> tuple[User, UserProfile, MatchSession]:
    name = f"{random.choice(NAMES)}{idx:02d}"
    gender = random.choice(GENDERS)
    grade = random.choice(GRADES)
    major = random.choice(MAJORS)
    gender_pref = random.choice(["男", "女", None])
    grade_pref = random.choice(["大一", "大二", "大三", "大四", None])

    user = User(
        name=name,
        gender=gender,
        grade=grade,
        major=major,
        team_goal="数学建模大赛",
        want_long_term=random.choice([True, False]),
        gender_preference=gender_pref,
        grade_preference=grade_pref,
        contact_info=f"math_demo_{idx:03d}@example.com",
        is_active=True,
    )

    profile = UserProfile(
        skill_modeling=r_score(),
        skill_coding=r_score(),
        skill_writing=r_score(),
        personality_leader=r_score(),
        personality_supporter=r_score(),
        personality_executor=r_score(),
        strength_competition_count=random.randint(0, 8),
        strength_award_count=random.randint(0, 4),
        strength_ambition=r_score(1.0, 10.0),
        strength_major_relevant=r_score(2.0, 10.0),
        preferred_role=random.choice(ROLES_MATH),
        raw_answers={
            "seed_group": "math",
            "created_by": "reset_and_seed_demo.py",
            "sample_index": idx,
        },
    )

    status = random.choice(["questioning", "matching", "completed", "completed"])
    session = MatchSession(
        status=status,
        question_count=(10 if status == "completed" else random.randint(0, 7)),
        user_vector=None,
        completed_at=(datetime.now(timezone.utc) if status == "completed" else None),
    )
    return user, profile, session


def create_ielts_user(idx: int) -> tuple[User, IELTSUserProfile, MatchSession]:
    name = f"{random.choice(NAMES)}{idx:02d}"
    gender = random.choice(GENDERS)
    grade = random.choice(GRADES)
    major = random.choice(MAJORS)
    gender_pref = random.choice(["男", "女", None])
    grade_pref = random.choice(["大一", "大二", "大三", "大四", None])

    user = User(
        name=name,
        gender=gender,
        grade=grade,
        major=major,
        team_goal="雅思学习搭子",
        want_long_term=random.choice([True, False]),
        gender_preference=gender_pref,
        grade_preference=grade_pref,
        contact_info=f"ielts_demo_{idx:03d}@example.com",
        is_active=True,
    )

    profile = IELTSUserProfile(
        skill_listening=r_score(),
        skill_reading=r_score(),
        skill_writing=r_score(),
        skill_speaking=r_score(),
        personality_planner=r_score(),
        personality_resourcer=r_score(),
        personality_coordinator=r_score(),
        strength_fluency=r_score(),
        strength_has_ielts_exp=random.choice([True, False]),
        strength_willing_training=random.choice([True, False]),
        strength_weekly_hours=random.randint(1, 25),
        strength_target_score=r_score(5.0, 10.0),
        preferred_role=random.choice(ROLES_IELTS),
        raw_answers={
            "seed_group": "ielts",
            "created_by": "reset_and_seed_demo.py",
            "sample_index": idx,
        },
    )

    status = random.choice(["questioning", "matching", "completed", "completed"])
    session = MatchSession(
        status=status,
        question_count=(10 if status == "completed" else random.randint(0, 7)),
        user_vector=None,
        completed_at=(datetime.now(timezone.utc) if status == "completed" else None),
    )
    return user, profile, session


def main() -> None:
    random.seed()
    db = SessionLocal()
    try:
        inspector = inspect(engine)
        existing_tables = set(inspector.get_table_names())
        has_ielts_table = "ielts_user_profiles" in existing_tables

        db.query(MatchResult).delete(synchronize_session=False)
        db.query(QuestionAnswer).delete(synchronize_session=False)
        db.query(MatchSession).delete(synchronize_session=False)
        if has_ielts_table:
            db.query(IELTSUserProfile).delete(synchronize_session=False)
        db.query(UserProfile).delete(synchronize_session=False)
        db.query(User).delete(synchronize_session=False)
        db.commit()

        for i in range(1, MATH_COUNT + 1):
            user, profile, session = create_math_user(i)
            db.add(user)
            db.flush()
            profile.user_id = user.id
            session.user_id = user.id
            db.add(profile)
            db.add(session)

        if has_ielts_table:
            for i in range(1, IELTS_COUNT + 1):
                user, profile, session = create_ielts_user(i)
                db.add(user)
                db.flush()
                profile.user_id = user.id
                session.user_id = user.id
                db.add(profile)
                db.add(session)

        db.commit()

        total_users = db.query(User).count()
        math_users = db.query(User).filter(User.team_goal != "雅思学习搭子").count()
        ielts_users = db.query(User).filter(User.team_goal == "雅思学习搭子").count()
        total_sessions = db.query(MatchSession).count()
        print(
            f"Seed complete. users={total_users}, math={math_users}, "
            f"ielts={ielts_users}, sessions={total_sessions}, has_ielts_table={has_ielts_table}"
        )
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
