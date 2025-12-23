from enum import Enum


class GenderEnum(Enum):
    male = "male"
    female = "female"
    other = "other"


class ActivityLevelEnum(Enum):
    low = "low"
    medium = "medium"
    high = "high"


class GoalTypeEnum(Enum):
    lose_weight = "lose_weight"
    gain_muscle = "gain_muscle"
    maintain = "maintain"


class WorkoutTypeEnum(Enum):
    cardio = "cardio"
    strength = "strength"
    flexibility = "flexibility"


class AIRoleEnum(Enum):
    user = "user"
    ai = "ai"
