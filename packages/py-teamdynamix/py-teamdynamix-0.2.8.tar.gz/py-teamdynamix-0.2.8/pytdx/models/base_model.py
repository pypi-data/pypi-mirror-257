class BaseModel:
    def to_dict(self):
        def convert_to_dict(obj):
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            elif isinstance(obj, list):
                return [convert_to_dict(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_to_dict(value) for key, value in obj.items()}
            else:
                return obj

        return {
            key: convert_to_dict(value)
            for key, value in vars(self).items()
            if value is not None
        }
