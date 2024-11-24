from marshmallow import fields
from marshmallow import Schema


class IssueTimeStatisticsSerializer(Schema):
    id = fields.String()
    status = fields.String()
    response_time = fields.Method("calculate_response_time")

    def calculate_response_time(self, obj):
        start_time = obj.created_at
        end_time = obj.updated_at
        if not start_time or not end_time:
            return None
        return round((end_time - start_time).total_seconds() / 3600, 2)
