from django.db import connection


def getAllMovies(limit, page):
    try:
        offset = int(page) * int(limit)
        print("ppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
        cursor = connection.cursor()
        #  SQL
        SQL = """
                 select cm.id,
                       cm.movie_name,
                       cm.image_link,
                       cm.movie_description_link,
                       replace(m.videoTrailerLink,'watch?v=','embed/') videoTrailerLink,
                       cm.rating_percentage,
                       cm.release_date,
                       cm.created_at
                from crawling_pagination_table_entertainment cm
                         join moviedetails m on cm.id = m.movieID limit %s  offset %s;                   
     
              """
        cursor.execute(SQL, (int(limit), offset))
        list_data = cursor.fetchall()
        return list_data, None
    except Exception as error:
        return None, error


def getTypeWiseMovies(limit, page, movieTypes):
    try:
        offset = int(page) * int(limit)
        print("ppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
        cursor = connection.cursor()
        #  SQL
        SQL = """
                 select cm.id,
                       cm.movie_name,
                       cm.image_link,
                       cm.movie_description_link,
                       replace(m.videoTrailerLink,'watch?v=','embed/') videoTrailerLink,
                       cm.rating_percentage,
                       cm.release_date,
                       cm.created_at
                from crawling_pagination_table_entertainment cm
                         join moviedetails m on cm.id = m.movieID 
                         join moviefacts m2 on cm.id = m2.movieID where m2.originalLanguage=%s limit %s  offset %s;                   

              """
        cursor.execute(SQL, (movieTypes, int(limit), offset))
        list_data = cursor.fetchall()
        return list_data, None
    except Exception as error:
        return None, error


def moviesFinderBYID(movieID):
    try:

        print("ppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
        cursor = connection.cursor()
        #  SQL
        SQL = """
                 select cm.id,
                       cm.movie_name,
                       cm.image_link,
                       cm.movie_description_link,
                       replace(m.videoTrailerLink,'watch?v=','embed/') videoTrailerLink,
                       cm.rating_percentage,
                       m.poster_image,
                       cm.release_date,
                       cm.created_at
                from crawling_pagination_table_entertainment cm
                         join moviedetails m on cm.id = m.movieID 
                         join moviefacts m2 on cm.id = m2.movieID where m2.movieID=%s;                   

              """
        cursor.execute(SQL, (int(movieID),))
        list_data = cursor.fetchall()
        return list_data, None
    except Exception as error:
        return None, error


def moviesDetail(movieID):
    try:
        cursor = connection.cursor()
        #  SQL
        SQL = """
            select cpte.id,
                   cpte.movie_name,
                   cpte.release_date,
                   cpte.image_link,
                   cpte.rating_percentage,
                   cpte.entertainment_type,
                   m.timePeriod,
                   m.movieOverView,
                   replace(m.videoTrailerLink,'watch?v=','embed/') videoTrailerLink,
                   m.poster_image,
                   m.entertainmentType,
                   m2.originalLanguage,
                   m2.releaseOrNot,
                   m2.budget,
                   m2.revenue
            from crawling_pagination_table_entertainment cpte
                     join moviedetails m on cpte.id =  m.movieID
                     join moviefacts m2 on cpte.id = m2.movieID
                     where m.movieID = %s;                 
              """
        cursor.execute(SQL, (int(movieID),))
        list_data = cursor.fetchall()
        return list_data, None
    except Exception as error:
        return None, error


def moviesActorData(moviesID):
    try:
        cursor = connection.cursor()
        # SQL
        SQL = """
                select id,
                       characterName,
                       realName,
                       peopleProfileLink,
                       takingPartInEpisode,
                       created_at,
                       archived_at,
                       imageOfCastPerson
                from moviecastpeople
                where movieID = %s;
        
              """
        cursor.execute(SQL, (int(moviesID),))
        list_data = cursor.fetchall()
        return list_data, None
    except Exception as error:
        return None, error


def findMoviesDataByYeasOrGenres(years, genres, topRated, limit, page, movieType, upComing):
    offset = int(page) * int(limit)
    cursor = connection.cursor()
    flag = False
    flagAnd = 0
    try:
        # SQL
        SQL = """
                select cm.id,
                       cm.movie_name,
                       cm.image_link,
                       cm.movie_description_link,
                       replace(m.videoTrailerLink, 'watch?v=', 'embed/') videoTrailerLink,
                       cm.rating_percentage,
                       cm.release_date,
                       cm.created_at
                from crawling_pagination_table_entertainment cm
                         join moviedetails m on cm.id = m.movieID
                         join moviefacts m2 on cm.id = m2.movieID             
             """
        if years != 'None':
            flag = True
            flagAnd = 1
            SQL += """ where cm.release_date like '%""" + str(years) + """%'"""

        if genres != 'None':
            if not flag:
                flag = True
                SQL += """ where """
            if flagAnd == 1:
                SQL += """ and """
            flagAnd = 1
            SQL += """  m.entertainmentType like '%""" + str(genres) + """%'"""

        if movieType != 'all':
            if not flag:
                flag = True
                SQL += """ where """
            if flagAnd == 1:
                SQL += """ and """
            flagAnd = 1
            SQL += """ m2.originalLanguage = '""" + str(movieType) + """'"""
        if int(upComing):
            if not flag:
                flag = True
                print(flag)
                SQL += """ where """
            if flagAnd == 1:
                SQL += """ and """
            SQL += """ cast(now() as date)<=cast(str_to_date(release_date,'%M %d,%YY') as date ) """
        if int(topRated):
            SQL += """ order by rating_percentage desc """
        SQL += """ limit %s  offset %s """
        print(SQL)
        cursor.execute(SQL, (int(limit), int(offset)))
        list_data = cursor.fetchall()
        return list_data, None
    except Exception as error:
        print(error)
        return None, error


def insertUserRatingData(movieID, rated, user_name):
    try:
        cursor = connection.cursor()
        # SQL
        SQL = """
                insert into user_rating_movie(movieID, rated, user_name)
                values (%s, %s, %s);            
              """
        cursor.execute(SQL, (movieID, rated, user_name))

        return None
    except Exception as error:
        return error


def moviesMediaData(movieID):
    try:
        cursor = connection.cursor()
        # SQL
        SQL = """
                    select id, facebook_link, twitter_link, instagram_link, home_page
                    from movie_socila_link where movieID = %s;               
              """
        cursor.execute(SQL, (movieID,))
        list_data = cursor.fetchall()
        return list_data, None
    except Exception as error:
        return None, error


def moviesDetailByName(searchMovie):
    try:
        cursor = connection.cursor()
        #  SQL
        SQL = """
            select cpte.id,
                   cpte.movie_name,
                   cpte.release_date,
                   cpte.image_link,
                   cpte.rating_percentage,
                   cpte.entertainment_type,
                   m.timePeriod,
                   m.movieOverView,
                   replace(m.videoTrailerLink,'watch?v=','embed/') videoTrailerLink,
                   m.poster_image,
                   m.entertainmentType,
                   m2.originalLanguage,
                   m2.releaseOrNot,
                   m2.budget,
                   m2.revenue
            from crawling_pagination_table_entertainment cpte
                     join moviedetails m on cpte.id =  m.movieID
                     join moviefacts m2 on cpte.id = m2.movieID
                    """
        SQL += """  where cpte.movie_name like '%""" + str(searchMovie) + """%'"""
        print(SQL)
        cursor.execute(SQL)
        list_data = cursor.fetchall()
        return list_data, None
    except Exception as error:
        return None, error


def finActorInfo(actorName):
    try:
        cursor = connection.cursor()
        # SQL
        SQL = """     
        select id,
           adult,
           also_known_as,
           biography,
           birthday,
           death_day,
           gender,
           home_page,
           imdb_id,
           tmdb_id,
           known_for_department,
           name,
           place_of_birth,
           popularity,
           profile_path,
           archived_at
        from actor_info
        where name = %s;    
              """
        cursor.execute(SQL, (actorName,))
        list_data = cursor.fetchall()
        print(list_data)
        return list_data, None
    except Exception as error:
        return None, error


def actorMoviesByName(actorName):
    try:
        cursor = connection.cursor()
        # SQL
        SQL = """
               select movieID,movie_name,image_link
                from moviecastpeople
                         join crawling_pagination_table_entertainment cpte on cpte.id = moviecastpeople.movieID
                where realName = %s;
    
              """
        cursor.execute(SQL, (actorName,))
        list_data = cursor.fetchall()
        print(list_data)
        return list_data, None
    except Exception as error:
        return None, error
