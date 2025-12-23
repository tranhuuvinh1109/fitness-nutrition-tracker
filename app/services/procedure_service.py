from app.models.procedure_model import ProcedureModel as Procedure
from app.db import db
from datetime import datetime

class ProcedureService:
    def get_all(self):
        return Procedure.query.filter(Procedure.deleted_at.is_(None)).order_by(Procedure.updated_at.desc()).all()

    def get(self, procedure_id):
        return Procedure.query.filter(Procedure.id == procedure_id, Procedure.deleted_at.is_(None)).first()

    def create(self, data):
        procedure = Procedure(**data)
        db.session.add(procedure)
        db.session.commit()
        return procedure

    def update(self, procedure_id, data):
        procedure = self.get(procedure_id)
        if not procedure:
            raise ValueError("Procedure not found")
        for field in [
            "category",
            "title",
            "description",
            "process_time",
            "authority_level",
            "fee_text",
            "process_steps",
            "required_documents",
            "important_notes",
            "creator",
        ]:
            if field in data:
                setattr(procedure, field, data[field])
        db.session.commit()
        return procedure

    def delete(self, procedure_id):
        procedure = self.get(procedure_id)
        if not procedure or procedure.deleted_at is not None:
            raise ValueError("Procedure not found")

        procedure.deleted_at = datetime.utcnow()
        db.session.commit()
        return procedure

procedure_service = ProcedureService()
