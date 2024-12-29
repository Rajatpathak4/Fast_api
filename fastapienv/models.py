from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary,BLOB
from database import Base
from sqlalchemy.orm import relationship



class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    body = Column(String(70))
    password= Column(String(200))

    user_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="blog")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(200))
    blog = relationship('Blog', back_populates="creator")


class JWTuser(Base):
    __tablename__ = 'jwt_user'
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String(50))
    email=Column(String(100))
    password=Column(String(255))


class uploadedFile(Base):
    __tablename__ = 'uploaded_file'
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    content_type=Column(String(255))
    data=Column(LargeBinary)