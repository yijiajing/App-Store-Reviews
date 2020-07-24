# App-Store-Reviews
<h2> What does it do </h2>
Extracts reviews of an app from App Store and saves them into json file (specifically date, rating, title, and content of each review).<br/>

<h2> How to use it </h2>
First find the two-character country code of the country of interest and the app id.<br/>
- Here is a comprehensive list of country code I found: https://gist.github.com/daFish/5990634
- The app id is found at the end of its App Store link (e.g. in ht<span>tps://apps.</span>apple.com/app/wei-xin/id414478124, 414478124 is the id of this app.)
<br/>
There are three ways of extraction to choose from:<br/>

~~~~
get_reviews_on_page(country, page, app_id, sort_by='mostRecent', out_filename='reviews.json')
get_reviews_on_pages(country, from_page, to_page, app_id, sort_by='mostRecent', out_filename='reviews.json')
get_all_reviews(country, app_id, sort_by='mostRecent', out_filename='reviews.json')
~~~~

By default, it sorts by most recent and saves reviews in a file called "reviews.json".
<br/>
Simply add function calls in the file, or import the functions to your own file and call them.
