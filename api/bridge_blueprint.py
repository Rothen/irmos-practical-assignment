"""Blueprint for cameras"""
from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import Schema, fields

from bridge_manager import BridgeData, BridgeManager

bridge_data_blueprint = Blueprint(
    "Bridge Data",
    __name__,
    url_prefix="/bridge-data",
    description="Operations on bridge data"
)

class BridgeDataSchema(Schema):
    """Bridge data schema"""
    _time = fields.List(fields.String(), required=True, metadata={"description": "Time"})
    stress_cycle = fields.List(fields.Float(), required=True, metadata={"description": "Stress cycle"})
    pos_na = fields.List(fields.Float(), required=True, metadata={"description": "Position NA"})

@bridge_data_blueprint.route("/")
class BridgeDataDetail(MethodView):
    """Resource for getting bridge data"""

    @bridge_data_blueprint.response(200, BridgeDataSchema)
    def get(self) -> BridgeData:
        """Get bridge data"""
        return BridgeManager().bridge_data()