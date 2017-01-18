Run locally

```
python ./stock-ticker.py
```

Install deps

```
pip install lxml -t ~/dev/personal/stock-ticker
```

Create zip file for deployment

```
rm ../stock-ticker.zip && zip -qr ../stock-ticker.zip . -x ".git/*"
```

Push new source code for lambda

```
aws lambda update-function-code --function-name stock-ticker --zip-file fileb://../stock-ticker.zip
```




Notes:

Create ES index for the first time

```
curl -XPOST 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/_aliases' -d '{ "actions" : [ { "add" : { "index" : "stock-ticker", "alias" : "stock-ticker" } } ] }'
```

