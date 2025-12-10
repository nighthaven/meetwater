from src.models.enums.coach_activity import CoachActivity

COACH_ACTIVITY_FR = {
    "public_lifeguarding": "Surveillance public",
    "school_lifeguarding": "Surveillance scolaire",
    "school_swimming_lessons": "Enseignement scolaire",
    "aqua_fitness": "Aqua Fitness",
    "aqua_training": "Aqua Training",
    "aqua_boxing": "Aqua Boxing",
    "aqua_cycling": "Aqua Bike",
    "gentle_aquafit": "Aqua Gym Douce",
    "aqua_health_training": "Aqua Sport Santé",
    "aquatic_preschool_4_5": "Jardin aquatique 4–5 ans",
    "aquatic_preschool_5_6": "Jardin aquatique 5–6 ans",
}


class TranslationService:
    @staticmethod
    def get_activity_label(activity: CoachActivity) -> str:
        return COACH_ACTIVITY_FR.get(activity.value, activity.value)
