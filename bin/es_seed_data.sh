#!/bin/bash

index_name="stock-ticker"

echo "Seeding index: ${index_name}"
curl -s -XPOST 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/stock-value' -d '{
    "update_date" : "2017-01-10T11:00:00",
    "value" : 72796.88,
    "currency": "AUD"
}' | jq .
curl -s -XPOST 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/stock-value' -d '{
    "update_date" : "2017-01-11T12:00:00",
    "value" : 78796.88,
    "currency": "AUD"
}' | jq .
curl -s -XPOST 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/stock-value' -d '{
    "update_date" : "2017-01-12T13:00:00",
    "value" : 76796.88,
    "currency": "AUD"
}' | jq .
curl -s -XPOST 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/stock-value' -d '{
    "update_date" : "2017-01-13T14:00:00",
    "value" : 78796.88,
    "currency": "AUD"
}' | jq .
curl -s -XPOST 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/stock-value' -d '{
    "update_date" : "2017-01-14T15:00:00",
    "value" : 68796.88,
    "currency": "AUD"
}' | jq .
curl -s -XPOST 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/stock-value' -d '{
    "update_date" : "2017-01-15T16:00:00",
    "value" : 78000.00,
    "currency": "AUD"
}' | jq .
curl -s -XPOST 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/stock-value' -d '{
    "update_date" : "2017-01-16T17:00:00",
    "value" : 80000.00,
    "currency": "AUD"
}' | jq .
curl -s -XPOST 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/stock-value' -d '{
    "update_date" : "2017-01-17T18:00:00",
    "value" : 75000.00,
    "currency": "AUD"
}' | jq .
# curl -s -XGET 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/_search' | jq .
sleep 1
curl -s -XGET 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/${index_name}/_count' | jq .
