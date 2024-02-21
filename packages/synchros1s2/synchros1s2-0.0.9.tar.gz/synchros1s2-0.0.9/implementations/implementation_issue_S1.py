from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, create_engine, DateTime, and_, text, Integer, desc
from sqlalchemy.orm import declarative_base

import config
from domains.issue import Issue

Base = declarative_base()
engine = create_engine(config.database_file)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


class IssueImplementationS1(Base, Issue):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    summary = Column(String)
    description = Column(String)
    updated = Column(DateTime)
    status = Column(String)
    miror = None

    # def __repr__(self):
    #     return f"Issue(id={self.id}, summary={self.summary}, description={self.description}, updated={self.updated}, status={self.status})"

    @staticmethod
    def create(**kwargs):  # avec les argument on creee un objet et on le save
        issue = IssueImplementationS1(**kwargs)
        session.add(issue)
        session.commit()
        return issue

    # @staticmethod
    # def new(**kwargs):  # avec les argument on creee un objet sans le save
    #     return IssueImplementationS1(**kwargs)

    @staticmethod
    def all():
        return session.query(IssueImplementationS1).all()

    @staticmethod
    def first():
        return session.query(IssueImplementationS1).first()

    @staticmethod
    def last():
        return session.query(IssueImplementationS1).order_by(desc(IssueImplementationS1.id)).first()

    @staticmethod
    def find_by(**kwargs):
        return session.query(IssueImplementationS1).filter_by(**kwargs).all()

    @staticmethod
    def find_by_id(id):
        return session.query(IssueImplementationS1).filter_by(id=id).first()

    @staticmethod
    def update(instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        session.commit()

    @staticmethod
    def update_all(**kwargs):
        session.query(IssueImplementationS1).update(kwargs)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def create_all_tables():
        Base.metadata.create_all(engine)

    @staticmethod
    def delete_all():
        session.execute(text("DELETE FROM issues"))
        session.commit()

    @staticmethod
    def all_filtre_id_et_updated():
        return session.query(IssueImplementationS1.id, IssueImplementationS1.updated).all()

    def save(self):
        session.add(self)
        session.commit()
        return self

    def get(self):
        return session.query(IssueImplementationS1).filter(
            and_(IssueImplementationS1.id == self.id)).first()

    def update(self):
        self.updated = datetime.now()
        session.merge(self)
        session.commit()

    def change_issue_status(self, new_status):
        self.status = new_status
        self.update()


if __name__ == '__main__':
    IssueImplementationS1.create_all_tables()
