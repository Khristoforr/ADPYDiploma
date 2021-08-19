from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


def database(user_finds_a_pair, matched_user):
    dsn = 'postgresql://postgres:password@localhost:5432/VKinder'
    metadata = MetaData()
    engine = create_engine(dsn)
    con = engine.connect()

    # для каждого пользователя, которому ищем пару будет создаваться своя таблица.
    links = Table(f'FoundedPeopleForUser{user_finds_a_pair}', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('user_finds_a_pair', String),
                  Column('matched_user', String)
                  )
    metadata.create_all(engine)
    return con.execute(links.insert().values(user_finds_a_pair=user_finds_a_pair, matched_user=matched_user))
