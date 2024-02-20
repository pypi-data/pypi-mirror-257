from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, create_engine, DateTime, and_, text, Integer, desc
from sqlalchemy.orm import declarative_base

import config
from domains.issue import Issue

#Definir dans le main ou on appel ces fonctions, creer une session dans le prod et une autre dans le test
engine = create_engine(config.database_file)
Base = declarative_base()
session_bd = sessionmaker(bind=engine, expire_on_commit=False)


class IssueImplementationS1(Base, Issue):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    summary = Column(String)
    description = Column(String)
    updated = Column(DateTime)
    status = Column(String)
    miror = None

    def __new__(cls,summary, description, updated, status):
        if config.s1_class == "S1":
            return IssueImplementationS1(summary, description, updated, status)
        # else:
        #     return IssueImplementationS3(summary, description, updated, status)
    @staticmethod
    def create_all_tables():
        Base.metadata.create_all(engine)

    @staticmethod
    def delete_all_data_table(session=session_bd):
        with session() as session_maker:
            session_maker.execute(text("DELETE FROM issues"))
            session_maker.commit()

    @staticmethod
    def all(session=session_bd):
        with session() as session_maker:
            issues = session_maker.query(IssueImplementationS1).all()
            return issues

    @staticmethod
    def all_filtre_id_et_updated(session=session_bd):
        with session() as session_maker:
            issues = session_maker.query(IssueImplementationS1.id, IssueImplementationS1.updated).all()
            return issues

    def save(self, session=session_bd):
        try:
            with session() as session_maker:
                session_maker.add(self)
                session_maker.commit()
                return self
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def find_by_id(id):
        with session_bd() as session_maker:
            return session_maker.query(IssueImplementationS1).filter(
                and_(IssueImplementationS1.id == id)).first()

    def get(self, session=session_bd):
        with session() as session_maker:
            return session_maker.query(IssueImplementationS1).filter(
                and_(IssueImplementationS1.id == self.id)).first()


    @staticmethod
    def get_last_record():
        with session_bd() as session_maker:
            return session_maker.query(IssueImplementationS1).order_by(desc(IssueImplementationS1.id)).first()

    @staticmethod
    def get_(issue, session=session_bd):
        with session() as session_maker:
            return session_maker.query(IssueImplementationS1).filter(
                and_(IssueImplementationS1.id == issue.id)).first()

    def delete(self, session=session_bd):
        with session() as session_maker:
            session_maker.delete(self)
            session_maker.commit()

    def update(self, session=session_bd):
        with session() as session_maker:
            self.updated = datetime.now()
            session_maker.merge(self)
            session_maker.commit()

    def change_issue_status(self, new_status):
        session = session_bd()
        self.status = new_status
        self.update()


if __name__ == '__main__':
    IssueImplementationS1.create_all_tables()
