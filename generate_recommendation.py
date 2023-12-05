import difflib
import random

def get_book_id(book_title, metadata):
    
    """
    Gets the book ID for a book title based on the closest match in the metadata dataframe.
    """
    
    existing_titles = list(metadata['title'].values)
    closest_titles = difflib.get_close_matches(book_title, existing_titles)
    book_id = metadata[metadata['title'] == closest_titles[0]]['id'].values[0]
    return book_id

def get_book_info(book_id, metadata):
    
    """
    Returns some basic information about a book given the book id and the metadata dataframe.
    """
    
    book_info = metadata[metadata['id'] == book_id][['id', 'isbn', 
                                                    'authors', 'title', 'original_title']]
    return book_info.to_dict(orient='records')

def predict_review(user_id, book_title, model, metadata):
    
    """
    Predicts the review (on a scale of 1-5) that a user would assign to a specific book. 
    """
    
    book_id = get_book_id(book_title, metadata)
    review_prediction = model.predict(uid=user_id, iid=book_id)
    return review_prediction.est

def generate_recommendation(user_id, model, metadata, thresh=4):
    
    """
    Generates a book recommendation for a user based on a rating threshold. Only
    books with a predicted rating at or above the threshold will be recommended
    """
    
    book_titles = list(metadata['title'].values)
    random.shuffle(book_titles)
    
    for book_title in book_titles:
        rating = predict_review(user_id, book_title, model, metadata)
        if rating >= thresh:
            book_id = get_book_id(book_title, metadata)
            return get_book_info(book_id, metadata)