from sqlalchemy import text


def clear_tables(session):
    session.execute(text("TRUNCATE TABLE representatives RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE admin RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE swimmers RESTART IDENTITY CASCADE;"))

    session.commit()
