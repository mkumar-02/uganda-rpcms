from enum import Enum


class G2PTargetModelMapping:
    MODEL_MAPPING = {
        "refugee": "g2p.register.refugees",
        "household": "g2p.register.households",
    }

    @classmethod
    def get_target_model_name(cls, key):
        return cls.MODEL_MAPPING.get(key)


class G2PRegistryType(Enum):
    REFUGEE = "refugee"
    HOUSEHOLD = "household"

    @classmethod
    def selection(cls):
        return [(member.value, member.name.replace("_", " ").title()) for member in cls]
