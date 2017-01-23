#!/bin/bash

index_name="stock-ticker"

echo "Deleting index: ${index_name}"
curl -s -XDELETE 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/' | jq .
