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

    @staticmethod
    def actorInfoColumn():
        column = ['id',
                  'adult',
                  'also_known_as',
                  'biography',
                  'birthday',
                  'death_day',
                  'gender',
                  'home_page',
                  'imdb_id',
                  'tmdb_id',
                  'known_for_department',
                  'name',
                  'place_of_birth',
                  'popularity',
                  'profile_path',
                  'archived_at'
                  ]
        return column

    @staticmethod
    def actorInfoRelatedMoviesColumn():
        column = [
            'movieID',
            'movie_name',
            'image_link'

        ]
        return column
