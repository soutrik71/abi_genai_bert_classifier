def dummy_prediction(user_query):
    """Dummy prediction function"""
    return {
        "prediction_label": "SIMPLE",
        "prediction_probability": 0.5,
        "user_query": user_query,
        "prediction_class": 0,
    }
