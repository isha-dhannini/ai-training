from uuid import uuid4

from .models import PredictionResponse


class PredictionService:

    def __init__(self):
        self.store = {}

    def predict(self, request):

        prediction = (
            "approved"
            if request.salary >= 50000
            else "rejected"
        )

        result = PredictionResponse(
            id=str(uuid4()),
            prediction=prediction
        )

        self.store[result.id] = result

        return result

    def get(self, prediction_id):

        return self.store.get(prediction_id)