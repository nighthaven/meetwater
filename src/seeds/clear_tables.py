from sqlalchemy import text


def clear_tables(session):
    session.execute(text("TRUNCATE TABLE representatives RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE admin RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE swimmers RESTART IDENTITY CASCADE;"))
    session.execute(
        text("TRUNCATE TABLE swimmers_representatives RESTART IDENTITY CASCADE;")
    )
    session.execute(text("TRUNCATE TABLE swimming_coaches RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE coaches_schedules RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE swimming_pools RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE bookings RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE swimmers_bookings RESTART IDENTITY CASCADE;"))
    session.execute(
        text("TRUNCATE TABLE swimming_pool_schedules RESTART IDENTITY CASCADE;")
    )
    session.execute(text("TRUNCATE TABLE coach_pack restart IDENTITY CASCADE;"))

    session.commit()
