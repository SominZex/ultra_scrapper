# NLP Based Website Scrapper

This is comprehensive web scrapping program integrated with NLP(Transformer) based website classifier.
The model was trained with 1400 instances of website metadata. It takes metadata from a website and categorize the website based on it's sentiment.

Model Training was carried out in Google Colab. Further the model is integrated into the 'scrapper.py' to classify websites based on their sentiments.


## Setup Instructions

1. **Install Python Packages:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Setup MySQL Database:**
    - Run the provided SQL script `DB_Table_Creator.sql` to create the necessary tables in the MySQL database.

3. **Configure Database Connection:**
    - Update the database connection details in the `extract_website_data` function.

4. **Run the Script:**
    ```bash
    python scrapper.py
    ```
5. **MySQL DB Essential:**
    Make sure to put your Hostname, Username and Password in the 'db_connector.py' in the '/root/db' directory.

5. **Ignore Terminal Error:**

## How it works:

1. Set up the environment by installing necessary modules or packages.
2. The 'Scrapper.py' script takes website input from 'websites.txt' file.
3. If you want to scrap a website then Include the URL into the 'websites.txt' and execute 'scrapper.py'

## Additional: Building NLP Model for website categorization (Wasn't necessary though)

#### Reason being:

1. To make website classification for robust and accurate I choose this. The model was trained with 1400 different websites Metadata, Keywords and Website Slogans so that it accurately Identifies what type of website it is. 

2. We can reuse the model is any further relevant projects in future.

3. The model takes the keywords from the scrapped website's metadata scan through it, classify the website and insert the relevant website category on the "category" field on 'websites' table.

3. Processing & Training operation was done on Google Colab and 'model_train.ipynb' file is provided. Check how it was done.

4. Model Integration into the scrapper.

5. Custom prediction can be done by executing "model_pred.py".

## Explanation
- The script fetches website data using `requests` and `BeautifulSoup`.
- Extracts meta title, description, language, social media links, tech stack, payment gateways, and category.
- Stores the extracted data in a MySQL database.
- The SQL script creates a database with 4 tables payment_gateways, social_media_links, tech_stacks & websites

## Challenges
- Handling dynamic content with `selenium`.
- Ensuring the script handles different website structures and possible errors gracefully.
- Definitely 403 Forbidden error are a bit tricky to handle.

## The End.