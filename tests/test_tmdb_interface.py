import unittest
from unittest.mock import patch, MagicMock
from src.tmdb_interface import get_recommendations, search_movie, get_movies_by_genre, create_full_movie_model
from src.tmdb_models.movie_model import MovieModel, GenreModel

class TestCreateFullMovieModel(unittest.TestCase):

    def test_create_full_movie_model(self):
        movie_data = {
            "id": 1,
            "title": "Test Movie",
            "poster_path": "test_path.jpg",
            "release_date": "2022-01-01",
            "genres": [
                {"id": 28, "name": "Action"},
                {"id": 12, "name": "Adventure"}
            ]
        }

        movie = create_full_movie_model(movie_data)

        self.assertIsInstance(movie, MovieModel)
        self.assertEqual(movie.id, 1)
        self.assertEqual(movie.title, "Test Movie")
        self.assertEqual(movie.poster, "https://image.tmdb.org/t/p/w185/test_path.jpg")
        self.assertEqual(movie.release_date, "2022-01-01")
        self.assertEqual(len(movie.genres), 2)
        self.assertIsInstance(movie.genres[0], GenreModel)
        self.assertEqual(movie.genres[0].id, 28)
        self.assertEqual(movie.genres[0].name, "Action")
        self.assertIsInstance(movie.genres[1], GenreModel)
        self.assertEqual(movie.genres[1].id, 12)
        self.assertEqual(movie.genres[1].name, "Adventure")

class TestGetRecommendations(unittest.TestCase):

    @patch('src.tmdb_interface.requests.get')
    def test_get_recommendations(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "page": 1,
            "results": [
                {
                    "id": 1,
                    "title": "Test Movie 1",
                    "poster_path": "/test_path_1.jpg",
                    "release_date": "2022-01-01"
                },
                {
                    "id": 2,
                    "title": "Test Movie 2",
                    "poster_path": "/test_path_2.jpg",
                    "release_date": "2022-01-02"
                }
            ]
        }
        mock_get.return_value = mock_response

        recommendations = get_recommendations(123)

        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0].id, 1)
        self.assertEqual(recommendations[0].title, "Test Movie 1")
        self.assertEqual(recommendations[1].id, 2)
        self.assertEqual(recommendations[1].title, "Test Movie 2")

class TestTmdbInterface(unittest.TestCase):

    @patch('src.tmdb_interface.requests.get')
    def test_search_movie(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "page": 1,
            "results": [
                {
                    "id": 1,
                    "title": "Test Movie 1",
                    "poster_path": "/test_path_1.jpg",
                    "release_date": "2022-01-01"
                },
                {
                    "id": 2,
                    "title": "Test Movie 2",
                    "poster_path": "/test_path_2.jpg",
                    "release_date": "2022-01-02"
                }
            ]
        }
        mock_get.return_value = mock_response

        movies = search_movie("test_query")

        self.assertEqual(len(movies), 2)
        self.assertEqual(movies[0].id, 1)
        self.assertEqual(movies[0].title, "Test Movie 1")
        self.assertEqual(movies[1].id, 2)
        self.assertEqual(movies[1].title, "Test Movie 2")

class TestGetMoviesByGenre(unittest.TestCase):

    @patch('src.tmdb_interface.requests.get')
    def test_get_movies_by_genre(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "page": 1,
            "results": [
                {
                    "id": 1,
                    "title": "Test Movie 1",
                    "poster_path": "/test_path_1.jpg",
                    "release_date": "2022-01-01"
                },
                {
                    "id": 2,
                    "title": "Test Movie 2",
                    "poster_path": "/test_path_2.jpg",
                    "release_date": "2022-01-02"
                }
            ]
        }
        mock_get.return_value = mock_response

        movies = get_movies_by_genre(28)

        self.assertEqual(len(movies), 2)
        self.assertIsInstance(movies[0], MovieModel)
        self.assertEqual(movies[0].id, 1)
        self.assertEqual(movies[0].title, "Test Movie 1")
        self.assertEqual(movies[1].id, 2)
        self.assertEqual(movies[1].title, "Test Movie 2")

if __name__ == '__main__':
    unittest.main()
