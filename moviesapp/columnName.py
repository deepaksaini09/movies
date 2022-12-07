class ColumnName:
    def __init__(self):
        pass

    @staticmethod
    def columnNameForCastMoviePeople():
        column = [
            'id',
            'characterName',
            'realName',
            'peopleProfileLink',
            'takingPartInEpisode',
            'created_at',
            'archived_at',
            'imageOfCastPerson'
        ]
        return column

    @staticmethod
    def socialLink():
        column = [
            'id',
            'facebook_link',
            'twitter_link',
            'instagram_link',
            'home_page'
        ]
        return column

