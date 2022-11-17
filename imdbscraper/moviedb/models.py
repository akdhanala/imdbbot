from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT


Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"
    movieId = Column("id", String(10), primary_key=True, nullable=False)
    title = Column("title", String(100), nullable=False)
    year = Column("year", Integer, nullable=False)
    director = Column("director", String(100), nullable=False)
    poster = Column("poster", TEXT, nullable=True)

    def __repr__(self):
        return f"<Movie(title={self.title}, year={self.year}, director={self.director}>"