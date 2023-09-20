import attr


@attr.dataclass
class StudyGroup:
    """
    Учебная группа
    """
    name: str
    course: int
