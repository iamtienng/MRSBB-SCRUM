from datetime import datetime


class Rating:
    userId = 0
    movieId = 0
    rating = 0
    timestamp = 0

    def __init__(self, userId, movieId):
        self.userId = userId
        self.movieId = movieId

    def create(self, mongoDatabase, rating):
        ratingCollection = mongoDatabase["rating"]
        ratingDoc = ratingCollection.find(
            {"userId": self.userId, "movieId": self.movieId})
        if (ratingDoc.count() > 0):
            return False
        self.rating = rating
        self.timestamp = datetime.now().timestamp().__int__()
        ratingCollection.insert_one(self.get_info())
        return True

    def update(self, mongoDatabase, rating):
        ratingCollection = mongoDatabase["rating"]
        ratingDoc = ratingCollection.find(
            {"userId": self.userId, "movieId": self.movieId})
        if (ratingDoc.count() > 0):
            ratingCollection.update_one({"userId": self.userId, "movieId": self.movieId}, {
                                        "$set": {"rating": rating}})
            return True
        return False

    def delete(self, mongoDatabase):
        ratingCollection = mongoDatabase["rating"]
        ratingDoc = ratingCollection.find(
            {"userId": self.userId, "movieId": self.movieId})
        if (ratingDoc.count() > 0):
            ratingCollection.delete_one(
                {"userId": self.userId, "movieId": self.movieId})
            return True
        return False

    def get_info(self):
        return {
            "userId": self.userId,
            "movieId": self.movieId,
            "rating": self.rating,
            "timestamp": self.timestamp,
        }

    def get_info_from_db(self, mongoDatabase):
        ratingCollection = mongoDatabase["rating"]
        ratingDoc = ratingCollection.find(
            {"userId": self.userId, "movieId": self.movieId})
        if (ratingDoc.count() > 0):
            self.userId = ratingDoc[0]['userId']
            self.movieId = ratingDoc[0]['movieId']
            self.rating = ratingDoc[0]['rating']
            self.timestamp = ratingDoc[0]['timestamp']
            return True
        return False
