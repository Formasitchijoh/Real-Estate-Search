import os
import csv
from django.http import HttpResponse
from listings.models import ProcessedListings, Listing,Image,Query
from django.conf import settings
import pandas as pd
import numpy as np
import json
import csv
import ast

def load_processed_data(**kwargs):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/processed_data.csv')
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            listing_id = int(row['listing'])
            listing = Listing.objects.get(pk=listing_id)
            ProcessedListings.objects.create(
                query=row['query'],
                listing=listing,
                title=row['title'],
                link=row['link'],
                listing_type=row['listing_type'],
                bedroom=row['bedroom'],
                bathrooms=row['bathrooms'],
                location=row['location'],
                town=row['town'],
                price=row['price'],
                pricepermonth=row['pricepermonth'],
                views=row['views'],
                reactions=row['reactions']
            )

def load_cleaned_data(file_path,**kwargs):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            listing = Listing.objects.create(
                title=row['title'],
                link=row['link'],
                listing_type=row['listing_type'],
                bedroom=row['bedroom'],
                bathrooms=row['bathrooms'],
                location=row['location'],
                town=row['town'],
                price=row['price'],
                pricepermonth=row['pricepermonth'],
                views=row['views'],
                reactions=row['reactions']
            )

            # Convert the 'images' field from string to list
            image_urls = ast.literal_eval(row['images'])

            # Create Image instances for the Listing
            for image_url in image_urls:
                Image.objects.create(
                    image=image_url,
                    listing=listing
                )

def export_to_csv(**kwargs):
    listings = Listing.objects.all()
    # Construct the file path
    app_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(app_dir, 'data/updated_listings.csv')

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['id', 'title', 'link', 'listing_type', 'bedroom', 'bathrooms', 'location', 'town', 'price', 'pricepermonth', 'views', 'reactions'])

        for listing in listings:
            writer.writerow([listing.id, listing.title, listing.link, listing.listing_type, listing.bedroom, listing.bathrooms, listing.location, listing.town, listing.price, listing.pricepermonth, listing.views, listing.reactions])

    return HttpResponse("CSV file exported successfully.")

def clean_data():
    input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/listings.csv')
    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/cleaned_data.csv')

    data = pd.read_csv(input_file_path)
    #Get statistical information of the numeric data in out dataset ie np.number
    data.describe(include=[np.number], percentiles=[.5]) \
        .transpose().drop("count", axis=1)

    # get the unique values and occurence of the non numeric objects in out dataset and their occurence
    data.describe(include=[object]).transpose().drop("count", axis=1)


    ## Determining the missing values in our dataset
    num_missing = data.isna().sum()
    num_missing = num_missing[num_missing > 0] # Excluding columns that contains 0 missing values
    percent_missing = num_missing * 100 / data.shape[0]
    pd.concat([num_missing, percent_missing], axis=1, 
            keys=['Missing Values', 'Percentage']).\
            sort_values(by="Missing Values", ascending=False)

    ############################
    #Data cleaning proper

    ###########################
  
    data['bedroom'] = data['bedroom'].fillna(1.0)

    data.loc[(data['bedroom'] == 0.0) & (data['price'] <= 65000.0), 'bedroom'] = 1.0

    data['bathrooms'] = np.where(data['bathrooms'] > 50, 1.0, data['bathrooms'])

    mask = (data['listing_type'].isin(['Studio', 'Store', 'Single Room', 'Guest house'])) & (data['bedroom'] == 0.0)
    data.loc[mask, 'bedroom'] = 1.0

    data['listing_type'] = np.where((data['listing_type'] == 'Guest hous') | (data['listing_type'] == 'house') | (data['listing_type'] == 'House') | (data['listing_type'] == 'Mega guest'), 'Guest house', data['listing_type'])

    # Fill bathrooms for Guest House and Studio
    mask = (data['listing_type'].isin(['Guest house', 'Base house'])) & (data['bedroom'] == 1.0)
    data.loc[mask, 'bathrooms'] = 1.0
    data.loc[data['listing_type'] == 'Studio', 'bathrooms'] = 1.0

    # Update the title
    data['title'] = data.apply(lambda row: f"{str(int(row['bedroom']))} bedroom{' ' + ' '.join(row['title'].split('|')[0].split(' ')[1:]) if row['title'].split('|')[0].split(' ')[1:] else ''} | {row['title'].split('|')[1]}" if '|' in row['title'] else row['title'], axis=1)
    data['views'] = data['views'].fillna(0).astype('int64')

    #filling out the missing price by using the mean of the prices
    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(strategy='mean')
    data['price'] = imputer.fit_transform(data[['price']]).astype('float64')
    data['pricepermonth'] = data['pricepermonth'].fillna('per month').astype(str)
    data = data.astype({
        'price': 'float64',
        'bedroom': 'float64',
        'bathrooms': 'float64',
        'reactions': 'int64',
        'views': 'int64'
    })
    print('here')
    data.to_csv(output_file_path, index=False)
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/cleaned_data.csv')
    if file_path:
        load_cleaned_data(file_path)

    print(f"Updated data has been written to '{output_file_path}'.")

def match_listings_to_query():
    input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/updated_listings.csv')
    # Load the dataset
    df = pd.read_csv(input_file_path)
    # Defining the search queries
    search_queries = [
        "houses in {town}",
        "{n} bedroom house in {location}{town}",
        "cheap house in {town}",
        "studio in  {location} {town}",
        "apartment in {town} {location}",
        "guest house in {town} {location}",
        "affordable houses in {town} {location}",
        "family houses in {town} {location}",
        "student rooms in {location} {town}",
        "single rooms in {town} {location}"
    ]
    #This function specifically match each listings to all possible search queries that can be passed by the user to return that particular listings
    def listing_to_queries(row):
        matched_queries = []
        if row['listing_type'] in ['Studio', 'Apartment', 'Guest house']:
            matched_queries.append(search_queries[0].format(town=row['town'], location=row['location']))

        bedroom_query = search_queries[1].format(n=int(row['bedroom']), town=row['town'], location=row['location'])
        matched_queries.append(bedroom_query)

        if 10000 <= row['price'] <= 50000:
            matched_queries.append(search_queries[2].format(town=row['town'], location=row['location']))

        if row['listing_type'] == 'Studio' and row['bedroom'] == 1 and 'toilet' in str(row['bathrooms']):
            matched_queries.append(search_queries[3].format(town=row['town'], location=row['location']))

        if row['listing_type'] == 'Apartment' and 1 <= row['bedroom'] <= 3:
            matched_queries.append(search_queries[4].format(town=row['town'], location=row['location']))

        if row['listing_type'] == 'Guest house':
            matched_queries.append(search_queries[5].format(town=row['town'], location=row['location']))

        if 10000 <= row['price'] <= 50000:
            matched_queries.append(search_queries[6].format(town=row['town'], location=row['location']))

        if row['listing_type'] in ['Studio', 'Apartment'] and 1 <= row['bedroom'] <= 3:
            matched_queries.append(search_queries[7].format(town=row['town'], location=row['location']))

        if (10000 <= row['price'] <= 50000) or (row['listing_type'] == 'Studio' and row['bedroom'] == 1 and 'toilet' in str(row['bathrooms'])):
            matched_queries.append(search_queries[8].format(town=row['town'], location=row['location']))

        if row['listing_type'] == 'Studio' and row['bedroom'] == 1 and len(str(row['bathrooms'])) == 1:
            matched_queries.append(search_queries[9].format(town=row['town'], location=row['location']))

        return matched_queries

    # Apply the function to each row in the DataFrame
    df['matched_queries'] = df.apply(listing_to_queries, axis=1)
    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict('records')
    app_dir = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(app_dir, 'data/output.json')
    # Save the data to a JSON file
    with open(output_file_path, 'w') as f:
        json.dump(data, f, indent=4)



def generate_queries():
    # Load the data from the JSON file
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/output.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    # Extract the matched_queries from each listing
    all_matched_queries = []
    for listing in data:
        all_matched_queries.extend(listing['matched_queries'])
    # Construct the file path
    app_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(app_dir, 'data/matched_queries.txt')
    # Save the matched_queries to a new file
    with open(file_path, 'w') as f:
        for query in set(all_matched_queries):
            f.write(query + '\n')
            Query.objects.create(
                query=query
            )

def match_query_to_listings():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/output.json')
    query_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/matched_queries.txt')
    processed_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/processed_data.csv')
    # Load the data from the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Create a dictionary to store the listings for each search query
    query_listings = {}

    # Read the search queries from the matched_queries_last.txt file
    with open(query_path, 'r') as f:
        search_queries = [line.strip() for line in f]

    # Iterate through the search queries and find the matching listings
    for query in search_queries:
        matching_listings = []
        for listing in data:
            if query in listing['matched_queries']:
                matching_listings.append(listing)
        query_listings[query] = matching_listings

    # Save the query-listings pairs to a CSV file
    print('saving')
    with open(processed_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'query', 'listing', 'title','link', 'listing_type', 'bedroom', 'bathrooms', 'location', 'town', 'price', 'pricepermonth', 'views', 'reactions'])
        id = 1
        for query, listings in query_listings.items():
            for listing in listings:
                row = [id]
                row.extend([
                    query,
                    listing['id'],
                    listing['title'],
                    listing['link'],
                    listing['listing_type'],
                    listing['bedroom'],
                    listing['bathrooms'],
                    listing['location'],
                    listing['town'],
                    listing['price'],
                    listing['pricepermonth'],
                    listing['views'],
                    listing['reactions']
                ])
                writer.writerow(row)
                id += 1


def match_query_to_listingss():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/matched_queries.txt')
    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/output.json' )
     # Construct the file path
    app_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(app_dir, 'data/query_listings.csv')
    # Load the data from the JSON file
    with open(output_file_path, 'r') as f:
        data = json.load(f)

    # Create a dictionary to store the listings for each search query
    query_listings = {}

    # Read the search queries from the matched_queries_last.txt file
    with open(file_path, 'r') as f:
        search_queries = [line.strip() for line in f]

    # Iterate through the search queries and find the matching listings
    for query in search_queries:
        matching_listings = []
        for listing in data:
            if query in listing['matched_queries']:
                matching_listings.append(listing)
        query_listings[query] = matching_listings

    # Save the query-listings pairs to a CSV file
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['query', 'listings'])
        for query, listings in query_listings.items():
            writer.writerow([query, json.dumps(listings)])




import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def Scrapper():

    current_page = 1
    proceed = True
    data = []

    def getHttp(url):

        while 1:
            try:
                page = requests.get(url, timeout = (3, 5))
                break
            except requests.exceptions.Timeout:
                print("The request timed out")
            except requests.exceptions.RequestException as e:
                print("An error occurred:", e)
            time.sleep(1)

        return page

    while(proceed):
        print("Currently Scrapping page:"+str(current_page))
        url = "https://digitalrenter.com/en/search?page="+str(current_page)

        page = getHttp(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        if(current_page == 3):
            proceed = False
        else:
            all_listings = soup.find_all('div', class_="listing-item")
            for listing in all_listings:
                item = {}
                item['title'] = listing.find('img').attrs['alt'].strip()
                item['link'] = listing.find('a').attrs['href'].strip()
                if listing:
                    try:
                        url = listing.find('a').attrs['href'].strip()
                        response = getHttp(url)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        item['images'] = []
                        listing_details = soup.find('ul', class_='listing-img-slider bg-black d-flex align-items-center')
                        if listing_details:
                            print('in here found')
                            image_tags = listing_details.find_all('img')
                            if image_tags.__len__:
                                print('in here')
                                for image_tag in image_tags:
                                    image_url = image_tag.get('src')
                                    item['images'].append(image_url)
                            else:
                                pass
                        else:
                            pass
                    except:
                        pass
                #item['image'] = listing.find('img').attrs['src'].strip()
            # Extract the listing type
                listing_type_element = listing.find('div', class_="col-lg-7 col-md-8 col-sm-7 col-7 pl-2 pr-2 type-loc")
                if listing_type_element:
                    listing_type_text = listing_type_element.text.strip()
                    item['listing_type'] = listing_type_text.split('\n')[0].strip().split('-')[0].strip()
                else:
                    item['listing_type'] = None            # Extract the number of beds
                bed_bath = listing.find('div', class_="col-lg-5 col-md-4 col-sm-5 col-5 pl-2 pr-2 bed-bath")
                if bed_bath:
                    bed_bath_span = bed_bath.find('span')
                    if bed_bath_span:
                        bed_bath_text = bed_bath_span.text
                        # Use a regular expression to extract the numeric value
                        match = re.search(r'\d+', bed_bath_text)
                        if match:
                            item['bedroom'] = int(match.group())
                        else:
                            item['bedroom'] = None
                    else:
                        item['bedroom'] = None
                else:
                    item['bedroom'] = None
                bath_rooms = listing.find('span', class_="pl-2 i-block")
                if bath_rooms:
                    bath_room_text = bath_rooms.text.strip()
                    match = re.search(r'\d+', bath_room_text)

                    if match:
                        item['bathrooms'] = int(match.group())
                    else:
                        item['bathrooms'] = None

                location_text =listing.find('span', class_='txt-caps').text.strip()
                location_parts = location_text.split(',')

                item['location'] = location_parts[0]
                if location_parts[1]:
                    item['town'] = location_parts[1]
                else:
                    item['town'] = None
                
                price_per = listing.find('div', class_="col-md-12 col-sm-12 col-xs-12 pl-2 pr-2 price_views_img")
                if price_per:
                    price_per_span = price_per.find('span')
                    if(price_per_span):
                        price_value = price_per_span.text
                        match = re.search(r'(\d+(?:,\d{3})*)', price_value)
                        if match:
                            item['price'] = int(match.group().replace(',', ''))
                        else:
                            item['price'] = None

                        price_per_month = price_per_span.findChild('span')
                        if price_per_month:
                            item['price_per_month'] = price_per_month.text.strip()
                        else:
                            item['price_per_month'] = None
                    else:
                        item['price'] = None

                else:
                    item['price'] = None
                
                price_views = listing.find('div', class_="col-md-12 col-sm-12 col-xs-12 pl-2 pr-2 price_views_img")

                if price_views:
                    total_views = price_views.find('span')
                    if total_views:
                        total_views_text = total_views.text.strip()
                        match = re.search(r'\d+', total_views_text)
                        if match:
                            item['views'] = int(match.group())
                        else :
                            item['views'] = None
                    else:
                        item['views'] = None
                    
                    total_reactions = price_views.find('span', class_="pl-2")
                    if total_reactions:
                        total_reactions_text = total_reactions.text.strip()
                        match = re.search(r'\d+', total_reactions_text)
                        if match:
                            item["reactions"] =int(match.group())
                        else:
                            item['reactions'] = None
                    else:
                        item["reactions"] = None
            
                data.append(item)
        current_page += 1

    new_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/listings.csv')
    df = pd.DataFrame(data)
    df.to_csv(new_file_path)


import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def similarity_check(query, top_n=5):
    # Increase the field size limit
    csv.field_size_limit(1000000000)

    # Read the dataset from the CSV
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/processed_data.csv')
    print('I am in the similarity check function and i want to check the query', query)
    dataset = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dataset.append(row)

    # Create a CountVectorizer to convert the queries to vectors
    vectorizer = CountVectorizer()

    # Extract the unique queries and their associated listings
    queries = set()
    query_to_listings = {}
    for row in dataset:
        q = row['query']
        queries.add(q)
        if q not in query_to_listings:
            query_to_listings[q] = []
        query_to_listings[q].append(row)

    # Fit and transform the unique queries to vectors
    query_vectors = vectorizer.fit_transform(list(queries))

    # Calculate the cosine similarity between the input query and all the queries
    input_query_vector = vectorizer.transform([query])
    scores = cosine_similarity(input_query_vector, query_vectors)[0]

    # Find the indices of the top-N queries with the highest similarity scores
    top_indices = scores.argsort()[-top_n:][::-1]
    top_queries = [list(queries)[i] for i in top_indices]
    print('cosine similarity', top_queries)
    # Get the top-N matching listings and their corresponding scores
    top_listings = []
    top_scores = []
    for q in top_queries:
        for listing in query_to_listings[q]:
            listing_id = listing['listing']
            images = Image.objects.filter(listing_id=listing_id)
            listing_with_images = listing.copy()
            listing_with_images['images'] = [image.image for image in images]
            top_listings.append(listing_with_images)
            top_scores.append(scores[list(queries).index(q)])
    return top_listings, top_scores

def Images(listing_id,*args, **kwagrs):
        listing_images = []
        print(type(listing_id))
        images = Image.objects.filter(listing_id=listing_id)
        print('in the building', images)
        listing_images = [image.image for image in images]
        print('listing', listing_images)
        return listing_images


def similarity_checkas(*args, **kwargs):

    def find_best_matches(query, dataset, top_n=5):
        # Increase the field size limit
        csv.field_size_limit(1000000000)

        # Read the dataset from the CSV
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/processed_data.csv')

        dataset = []
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dataset.append(row)

        # Create a CountVectorizer to convert the queries to vectors
        vectorizer = CountVectorizer()

        # Extract the unique queries and their associated listings
        queries = set()
        query_to_listings = {}
        for row in dataset:
            q = row['query']
            queries.add(q)
            if q not in query_to_listings:
                query_to_listings[q] = []
            query_to_listings[q].append(row)

        # Fit and transform the unique queries to vectors
        query_vectors = vectorizer.fit_transform(list(queries))

        # Calculate the cosine similarity between the input query and all the queries
        input_query_vector = vectorizer.transform([query])
        scores = cosine_similarity(input_query_vector, query_vectors)[0]

        # Find the indices of the top-N queries with the highest similarity scores
        top_indices = scores.argsort()[-top_n:][::-1]
        top_queries = [list(queries)[i] for i in top_indices]

        # Get the top-N matching listings and their corresponding scores
        top_listings = []
        top_scores = []
        for q in top_queries:
            for listing in query_to_listings[q]:
                listing_id = listing['listing']
                print(listing['query'], listing_id)
                images = Image.objects.filter(listing_id=listing_id)
                listing_with_images = listing.copy()
                listing_with_images['images'] = [image.image for image in images]
                top_listings.append(listing_with_images)
                top_scores.append(scores[list(queries).index(q)])

        return top_listings, top_scores

    # Increase the field size limit
    csv.field_size_limit(1000000000)

    # Read the dataset from the CSV 
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/processed_data.csv')

    dataset = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dataset.append(row)

    # Example usage
    search_query = 'house in douala'
    top_listings, top_scores = find_best_matches(search_query, dataset, top_n=3)
    result_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/search_result.json')
    # Save the top matches to a JSON file
    with open(result_file_path, "w") as f:
        json.dump({"Listings": top_listings, "Scores": top_scores}, f, indent=4)