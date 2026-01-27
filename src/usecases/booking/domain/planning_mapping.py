from src.models.enums.coach_activity import CoachActivity
from src.models.enums.swimmer_level import SwimmerLevel

PLANNING_MAPPING = {
    (True, SwimmerLevel.AQUAPHOBIC): CoachActivity.ADULT_AQUAPHOBIC,
    (True, SwimmerLevel.BEGINNER): CoachActivity.ADULT_BEGINNER,
    (True, SwimmerLevel.INTERMEDIATE): CoachActivity.ADULT_INTERMEDIATE,
    (True, SwimmerLevel.CONFIRMED): CoachActivity.ADULT_CONFIRMED,
    (False, SwimmerLevel.AQUAPHOBIC): CoachActivity.CHILD_AQUAPHOBIC,
    (False, SwimmerLevel.BEGINNER): CoachActivity.CHILD_BEGINNER,
    (False, SwimmerLevel.INTERMEDIATE): CoachActivity.CHILD_INTERMEDIATE,
    (False, SwimmerLevel.CONFIRMED): CoachActivity.CHILD_CONFIRMED,
}
