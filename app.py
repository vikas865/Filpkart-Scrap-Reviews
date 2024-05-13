from flask import Flask, render_template, request,jsonify
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pymongo
import ssl
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/review', methods=['GET','POST'])
@cross_origin()
def get_reviews():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ", "")
        #searchString = "ipnone12"
        flipkart_url = "https://www.flipkart.com/search?q=" + searchString
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        uClient = urlopen(flipkart_url, context=ctx)
        flipkartPage = uClient.read()
        #flipkartPage
        flipkart_html = bs(flipkartPage,'html.parser')
        # flipkart_html

        allphones= flipkart_html.find_all('div',{'class': 'cPHDOP'})

        del allphones[0:3]
        # for i in allphones:
        #     prod_url="https://www.flipkart.com"+i.div.a['href']
        prod_url="https://www.flipkart.com"+allphones[0].div.a['href']

        product_page= requests.get(prod_url)
        product_page.encoding='utf-8'
        prod_html= bs(product_page.text,  'html.parser')

        all_comments= prod_html.find_all('div', {'class' : 'RcXBOT'})
        filename= searchString+'.csv'
        fw=open(filename,'w',encoding="utf-8")
        headers= "Product, Customer Name, Rating, Heading, Comment \n"
        fw.write(headers)
        reviews=[]
        for i in all_comments:
            try:
                name = i.div.div.find_all('p', '_2NsDsF AwS1CA')[0].text.strip()
            except:
                name= 'No Name'
            try:
                comment_head = i.div.div.div.text
            except:
                comment_head= 'no comment'
            try:
                ratings = i.div.div.div.div.text
            except:
                ratings = 'No Rating'
            try:
                message = i.div.div.find_all('div', {'class': ''})[0].div.text
            except:
                message = 'No Message'
            mydict = {"Product": searchString, "Name": name, "Rating": ratings, "CommentHead": comment_head,
                      "Comment": message}
            reviews.append(mydict)
            fw.write(searchString+','+name+','+ratings+','+comment_head+','+message+'\n')
        client = pymongo.MongoClient("mongodb+srv://vikas865:vikas865@cluster0.rh4sjbj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        db = client['review_scrap']
        review_col = db['review_scrap_data']
        review_col.insert_many(reviews)
        fw.close()
        client.close()
        return render_template('results.html',reviews=reviews[0:len(reviews)-1])
    else:
        return render_template('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
