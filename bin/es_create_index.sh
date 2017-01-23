#!/bin/bash

index_name="stock-ticker"

echo "Creating index: ${index_name}"
curl -s -XPUT 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}' -d '
{
 "mappings" : {
  "stock-value" : {
   "properties" : {
    "update_date" : {"type": "date", "index": "not_analyzed" },
    "currency" : {"type": "string", "index": "not_analyzed" },
    "value" : { "type" : "double", "index": "not_analyzed" }
   }
  }
 }
}' | jq .
curl -s -XGET 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}' | jq .
