from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.schemas.procedure_schema import (
    ProcedureSchema,
    ProcedureCreateSchema,
    ProcedureUpdateSchema,
)
from app.services.procedure_service import procedure_service


blp = Blueprint("Procedure", __name__, description="Procedure API")


@blp.route("/procedures")
class ProcedureList(MethodView):
    @blp.response(200, ProcedureSchema(many=True))
    def get(self):
        """Get all procedures"""
        return procedure_service.get_all()

    @blp.arguments(ProcedureCreateSchema)
    @blp.response(201, ProcedureSchema)
    def post(self, data):
        """Create a new procedure"""
        return procedure_service.create(data)


@blp.route("/procedures/<int:procedure_id>")
class ProcedureDetail(MethodView):
    @blp.response(200, ProcedureSchema)
    def get(self, procedure_id):
        """Get procedure by id"""
        procedure = procedure_service.get(procedure_id)
        if not procedure:
            abort(404, message=f"Procedure {procedure_id} not found")
        return procedure

    @blp.arguments(ProcedureUpdateSchema)
    @blp.response(200, ProcedureSchema)
    def post(self, data, procedure_id):
        """Update procedure"""
        return procedure_service.update(procedure_id, data)

    @blp.response(204)
    def delete(self, procedure_id):
        """Delete procedure"""
        procedure_service.delete(procedure_id)
        return {}
