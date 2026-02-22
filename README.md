# URLShortner

The functionality of URL Shortner is taking a long URL and to return a unique short link. When the user clicks the short link, redirect them to the original URL with minimal latency. 

Users can optionally pick their own short "slug." Links should have a default or user-defined lifespan.

I used the following to generate the URL:

1. Fast API to demonstrate the API calls quickly.
2. Used MD5 hashing algorithm and take the first 7 characters.
3. I have used sqlite for demo purposes where I have created a table called url_list(id INT PRIMARY_KEY, long_url TEXT, short_url TEXT)
4. Write Path: User submits a URL → Load Balancer → App Service → Get unique ID from Range Handler → Store in NoSQL DB → Return short link.
5. Read Path: User clicks link → Load Balancer → Cache (Redis) → If not in cache, check NoSQL DB → 301 Redirect to original URL.
