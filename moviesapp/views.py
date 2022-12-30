import json
import threading
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

from moviesapp.Serializers import CastMovieActors
from moviesapp.columnName import ColumnName
from moviesapp.dBQuery import getAllMovies, getTypeWiseMovies, moviesFinderBYID, moviesDetail, moviesActorData, \
    findMoviesDataByYeasOrGenres, insertUserRatingData, moviesMediaData, moviesDetailByName, finActorInfo, \
    actorMoviesByName
from Movies.serializeAndDeserialize import convertPythonDataIntoJsonData
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

findColumnName = ColumnName()
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def home_1(request):
    limit = request.GET['limit']
    page = request.GET['page']
    movieType = request.GET['type']
    if request.method == 'GET':
        if movieType == 'all':
            moviesData, error = getAllMovies(limit, page)
        else:
            moviesData, error = getTypeWiseMovies(limit, page, movieType)
        if error:
            HttpResponse('home: hi error occurred during fetching data from database')
        columns = [
            'id',
            'movie_name',
            'image_link',
            'movie_description_link',
            'videoTrailerLink',
            'rating_percentage',
            'release_date',
            'created_at'
        ]

        jsonData, error = convertPythonDataIntoJsonData(moviesData, columns)
        # data = {"jsonDAta": jsonData, "Name": [{'name': 'deepak', 'roll': 23}, {'name': 'deepak', 'roll': 23}]}
        print(jsonData)
        if error:
            HttpResponse("home : error occurred during convert python data into json data")
        return HttpResponse(json.dumps(jsonData, default=str))
    return HttpResponse("hi ")


def movieFinderByID(request):
    MovieID = request.GET['id']
    if request.method == 'GET':
        moviesData, error = moviesFinderBYID(MovieID)
        if error:
            HttpResponse('movieFinderByID: hi error occurred during fetching data from database')
        columns = [
            'id',
            'movie_name',
            'image_link',
            'movie_description_link',
            'videoTrailerLink',
            'rating_percentage',
            'poster_image',
            'release_date',
            'created_at'
        ]

        jsonData, error = convertPythonDataIntoJsonData(moviesData, columns)
        print(jsonData)
        if error:
            HttpResponse("movieFinderByID : error occurred during convert python data into json data")
        return HttpResponse(json.dumps(jsonData, default=str))
    return HttpResponse("hi ")


def movieDetail(request):
    MovieID = request.GET['id']
    if cache.get(MovieID):
        print('hi 000000000000000000000000')
        data = cache.get(MovieID)
        return HttpResponse(data, content_type='application/json')

    if request.method == 'GET':
        # ////////////////////////////////////// MoviesDetails //////////////////////////////////
        moviesData, error = moviesDetail(MovieID)
        if error:
            HttpResponse('movieFinderByID: hi error occurred during fetching data from database')
        columns = [
            'id',
            'movie_name',
            'release_date',
            'image_link',
            'rating_percentage',
            'entertainment_type',
            'timePeriod',
            'movieOverView',
            'videoTrailerLink',
            'poster_image',
            'entertainmentType',
            'originalLanguage',
            'releaseOrNot',
            'budget',
            'revenue'
        ]

        jsonData, error = convertPythonDataIntoJsonData(moviesData, columns)
        print(jsonData)
        if error:
            HttpResponse("movieFinderByID : error occurred during convert python data into json data")
        # ////////////////////////////////// End Movies Data ////////////////////////////////////////

        # ///////////////////////////////Movie Cats Actor //////////////////////////////////////////
        moviesCastActor, error = moviesActorData(MovieID)
        if error:
            HttpResponse("CastActorProfile : error occurred during fetching data from DB")
        columns = findColumnName.columnNameForCastMoviePeople()
        jsonDataForCastPeople, error = convertPythonDataIntoJsonData(moviesCastActor, columns)
        if error:
            HttpResponse("CastActorProfile : error occurred during convert python data into json data")
        # /////////////////////////////////////// End Move Cast Actor ///////////////////////////////

        # ////////////////////////////////////// Social Media Link    /////////////////////////////
        socialMediaData, error = moviesMediaData(MovieID)
        if error:
            HttpResponse("CastActorProfile : error occurred during fetching data from DB")
        columns = findColumnName.socialLink()
        socialMediaDataToJson, error = convertPythonDataIntoJsonData(socialMediaData, columns)
        if error:
            HttpResponse("CastActorProfile : error occurred during convert python data into json data")
        # ////////////////////////////////////// End Social Media Link ////////////////////////////
        data = {'movie_details': jsonData,
                "cast_actor_details": jsonDataForCastPeople,
                "social_link": socialMediaDataToJson}
        data = json.dumps(data, default=str)
        try:
            cache.set(MovieID, data)
        except Exception as error:
            print('error in set data in redis cache', error)
        return HttpResponse(data, content_type='application/json')
    return HttpResponse("hi ")


def CastActorProfile(request):
    MovieID = request.GET['id']
    moviesCastActor, error = moviesActorData(MovieID)
    if error:
        HttpResponse("CastActorProfile : error occurred during fetching data from DB")
    columns = findColumnName.columnNameForCastMoviePeople()
    jsonDataForCastPeople, error = convertPythonDataIntoJsonData(moviesCastActor, columns)
    if error:
        HttpResponse("CastActorProfile : error occurred during convert python data into json data")
    return HttpResponse(json.dumps(jsonDataForCastPeople, default=str))
    # moviesCastActor, error = moviesActorData(2)
    # serializersData = CastMovieActors(moviesCastActor)
    # data = convertPythonDataIntoJsonData()
    # json_data = JSONRenderer().render(serializersData.data)
    # return HttpResponse(json_data, content_type='application/json')


def movieDetailsByYearsOrGenresOrLanguagesOrAll(request):
    url = request.get_full_path()
    print(request.get_full_path())
    # 'years=None&genres=None&topRated=0&limit=10&page=0&type=all&upComing=0'
    years = request.GET['years']
    genres = request.GET['genres']
    topRated = int(request.GET['topRated'])
    limit = request.GET['limit']
    page = request.GET['page']
    movieType = request.GET['type']
    upComing = int(request.GET.get('upComing'))
    flag = False
    if (years == 'None'
            and genres == 'None'
            and topRated == 0
            and movieType == 'all'
            and upComing == 0):
        flag = True
        if cache.get(page):
            data = cache.get(page)
            print('data is coming from redis ')
            return HttpResponse(data)

    print(limit, page, movieType, years, genres, topRated, upComing)
    if request.method == 'GET':
        moviesData, error = findMoviesDataByYeasOrGenres(years, genres, topRated, limit, page, movieType, upComing)
        if error:
            HttpResponse('home: hi error occurred during fetching data from database')
        columns = [
            'id',
            'movie_name',
            'image_link',
            'movie_description_link',
            'videoTrailerLink',
            'rating_percentage',
            'release_date',
            'created_at'
        ]

        jsonData, error = convertPythonDataIntoJsonData(moviesData, columns)
        print(jsonData)
        if error:
            HttpResponse("home : error occurred during convert python data into json data")
        data = json.dumps(jsonData, default=str)
        try:
            if flag:
                cache.set(page, data)
                flag = False
                print('data has been set for home page', flag)
        except Exception as error:
            print('error setting data in redis', error)
        print('data is coming from DB')
        return HttpResponse(data)
    return HttpResponse("hi ")


@csrf_exempt
def ratedMovieByUsers(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        movieID = int(body['movieID'])
        rated = int(body['rated'])
        user_name = body['user_name']
        print(movieID, user_name, rated)
        error = insertUserRatingData(movieID, rated, user_name)
        if error:
            return HttpResponse(json.dumps({'error': error}))
        return HttpResponse(json.dumps({"message": 'successfully submitted data'}))
    else:
        HttpResponse("error in method type")


def testData(request):
    data = {
        "name": 'Deepak saini',
        "car": [{'name': 'deepak', 'roll': 23}, {'name': 'deepak', 'roll': 23}]
    }
    return HttpResponse(json.dumps(data))


@csrf_exempt
def searchMovies(request):
    searchMovieName = json.loads(request.body)
    searchMovieName = searchMovieName['searchMovie']
    print(searchMovieName)
    if cache.get(searchMovieName):
        print('hi 000000000000000000000000')
        data = cache.get(searchMovieName)
        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        # ////////////////////////////////////// MoviesDetails //////////////////////////////////
        moviesData, error = moviesDetailByName(searchMovieName)
        if error:
            HttpResponse('movieFinderByID: hi error occurred during fetching data from database')
        columns = [
            'id',
            'movie_name',
            'release_date',
            'image_link',
            'rating_percentage',
            'entertainment_type',
            'timePeriod',
            'movieOverView',
            'videoTrailerLink',
            'poster_image',
            'entertainmentType',
            'originalLanguage',
            'releaseOrNot',
            'budget',
            'revenue'
        ]

        jsonData, error = convertPythonDataIntoJsonData(moviesData, columns)
        print(jsonData)
        if error:
            HttpResponse("movieFinderByID : error occurred during convert python data into json data")
        # ////////////////////////////////// End Movies Data ////////////////////////////////////////

        # ///////////////////////////////Movie Cats Actor //////////////////////////////////////////
        # moviesCastActor, error = moviesActorData(MovieID)
        # if error:
        #     HttpResponse("CastActorProfile : error occurred during fetching data from DB")
        # columns = findColumnName.columnNameForCastMoviePeople()
        # jsonDataForCastPeople, error = convertPythonDataIntoJsonData(moviesCastActor, columns)
        # if error:
        #     HttpResponse("CastActorProfile : error occurred during convert python data into json data")
        # # /////////////////////////////////////// End Move Cast Actor ///////////////////////////////
        #
        # # ////////////////////////////////////// Social Media Link    /////////////////////////////
        # socialMediaData, error = moviesMediaData(MovieID)
        # if error:
        #     HttpResponse("CastActorProfile : error occurred during fetching data from DB")
        # columns = findColumnName.socialLink()
        # socialMediaDataToJson, error = convertPythonDataIntoJsonData(socialMediaData, columns)
        # if error:
        #     HttpResponse("CastActorProfile : error occurred during convert python data into json data")
        # # ////////////////////////////////////// End Social Media Link ////////////////////////////
        data = {'movie_details': jsonData}
        data = json.dumps(data, default=str)
        try:
            cache.set(searchMovieName, data)
        except Exception as error:
            print('error in set data in redis cache', error)
        return HttpResponse(data, content_type='application/json')
    return HttpResponse("hi ")


@csrf_exempt
def actorInfo(request):
    # body = json.loads(request.body)
    actorName = request.GET['actorName']
    ############################################## 1 ###############################################
    actorColumnsData = findColumnName.actorInfoColumn()
    actorData, error = finActorInfo(actorName)
    actorJasonData, error = convertPythonDataIntoJsonData(actorData, actorColumnsData)
    ################################################ 2 #######################
    actorMoviesColumnsData = findColumnName.actorInfoRelatedMoviesColumn()
    actorMoviesData, error = actorMoviesByName(actorName)
    actorMoviesJasonData, error = convertPythonDataIntoJsonData(actorMoviesData, actorMoviesColumnsData)
    ##################################################################
    data = {'peopleInfo': actorJasonData, 'movies': actorMoviesJasonData}
    data = json.dumps(data, default=str)
    print('complete threading')
    return HttpResponse(data, content_type='application/json')
