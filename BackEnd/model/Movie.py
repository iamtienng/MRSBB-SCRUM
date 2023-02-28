from bson.objectid import ObjectId


class Movie:
    movieId = 0
    movieTitle = ""
    movieGenre = ""
    moviePoster = ""

    def get_info(self):
        return {
            "movieId": self.movieId,
            "movieTitle": self.movieTitle,
            "movieGenre": self.movieGenre,
            "moviePoster": self.moviePoster,
        }

    def get_info_from_db(self, mongoDatabase, idObj):
        movieCollection = mongoDatabase["movie"]
        movieDoc = movieCollection.find({"_id": ObjectId(idObj)})
        if (movieDoc.count() > 0):
            self.movieId = movieDoc[0]['movieId']
            self.movieTitle = movieDoc[0]['movieTitle']
            self.movieGenre = movieDoc[0]['movieGenre']
            self.moviePoster = movieDoc[0]['moviePoster']
            return True
        return False
