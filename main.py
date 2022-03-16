from bs4 import BeautifulSoup
import requests
import pandas


product_url = 'https://www.audible.com/pd/The-Book-Audiobook/1515919463?qid=1647416681&sr=1-1&ref=a_search_c3_lProduct_1_1&pf_rd_p=83218cca-c308-412f-bfcf-90198b687a2f&pf_rd_r=PD4ZKJ2JZRGNHG2HNK1P'
header ={
  "Accept-Language":"en-US,en;q=0.9,ru;q=0.8,es;q=0.7,ar;q=0.6",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
 }

response = requests.get(product_url, headers=header)
web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")
#print(soup.title)
book_price = soup.find('a', class_='bc-button-text')
#print(book_price.getText().strip())
book_title = soup.find('h1', class_='bc-heading')
#print(book_title.getText().strip())
book_description = soup.find('span', class_='bc-size-medium')
#print(book_description.getText().strip())


publisher_summary = soup.find('div', class_='bc-container productPublisherSummary')
publisher_summary_paragraph = publisher_summary.find('p')
#print(publisher_summary_paragraph.getText().strip())


critic_reviews = soup.find('div', class_='bc-container productCriticsSummary')
critic_reviews_paragraph = critic_reviews.find('p')
#print(critic_reviews_paragraph.getText().strip())

the_reviews_url = "https://www.amazon.com/The-Book-Keith-Houston-audiobook/product-reviews/B07QVMHX1C/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
response_2 = requests.get(the_reviews_url, headers=header)
soup_2 = BeautifulSoup(response_2.text, 'html.parser')
user_review = soup_2.find('div', class_='a-section a-spacing-none review-views celwidget')
all_reviews_list = []
all_reviews = user_review.find_all('span', class_='a-size-base review-text review-text-content')
for review in all_reviews:
    single_review = review.getText().strip()
    all_reviews_list.append(single_review)
for item in all_reviews_list:
    print(item)

product_information = {'Book Title': book_title.getText().strip(),
                 'Book Description': book_description.getText().strip(),
                 'Publisher Information': publisher_summary_paragraph.getText().strip(),
                 'Critic Reviews': critic_reviews_paragraph.getText().strip(),
                 'Price': book_price.getText().strip(),
                 'Reviews': (item for item in all_reviews_list),
                 }
new_data = pandas.DataFrame(product_information)
new_data.to_csv('product.csv')