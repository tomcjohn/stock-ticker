Create zip file for deployment

```
rm ../stock-ticker.zip && zip -r ../stock-ticker.zip . -x ".git/*"
```

Push new source code for lambda

```
aws lambda update-function-code --function-name stock-ticker --zip-file fileb://../stock-ticker.zip
```
