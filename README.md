Simple Book Recommendation System
This project is a Flask-based web application that provides two types of book recommendations:

Popularity-Based: Displays the top 30 most popular books. Popularity is determined by a combination of the number of ratings and the average rating for each book.

Book-Specific: Recommends books similar to a title provided by the user.

The recommendation engine uses cosine similarity to measure the distance between books. This is achieved by first creating a pivot table where rows are books, columns are users, and the values represent the number of reviews. This converts each book into a vector, allowing the system to find the most similar books to a given input.

Technologies:

Backend: Python (Flask, NumPy, Pandas)

Frontend: HTML, Bootstrap 5
