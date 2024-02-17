class BaseModel:
    def to_dict(self):
        return {key: value for key, value in vars(self).items() if value is not None}
