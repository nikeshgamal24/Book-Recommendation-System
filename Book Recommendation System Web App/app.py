from flask import Flask,render_template,request
import pickle
import numpy as np

# Load the pickled data for the recommendation system
# These files are assumed to be in the same directory as app.py
popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

# Initialize the Flask application
app = Flask(__name__)

# Route for the home page (displays top 50 books)
@app.route('/')
def index():
    # Render the 'index.html' template and pass the data from the popular_df
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values)
                           )

# Route for the recommendation page (displays the search form)
@app.route('/recommend')
def recommend_ui():
    # Render the 'recommend.html' template
    return render_template('recommend.html')

# Route to handle the book recommendation logic (post request)
@app.route('/recommend_books',methods=['post'])
def recommend():
    # Get the user's input from the form
    user_input = request.form.get('user_input')
    
    # Add this line to trim the whitespace from both ends of the user input
    user_input = user_input.strip()

    try:
        # Find the index of the book the user entered in the pivot table (pt)
        index = np.where(pt.index == user_input)[0][0]
    except IndexError:
        # Handle case where the book is not found
        # You could add a flash message here to inform the user
        return render_template('recommend.html', data=None)

    # Get the similarity scores for the user's book
    # Sort the scores in descending order and get the top 5 similar items
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:8]

    data = []
    for i in similar_items:
        # For each similar book, get its title, author, and image
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    # Print the recommended data to the console for debugging
    print(data)

    # Render the 'recommend.html' template with the recommended data
    return render_template('recommend.html',data=data)

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)