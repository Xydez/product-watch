# product-watch
*product-watch* is a python script that scrapes URL:s and watches them for changes, and then calls a webhook with the changed product.

The typical use case is to ping the user when a product is in stock (e.g. keyboards).

To get started, create a `data.json` that contains the configuration:
```json
{
  "webhook_url": "https://discord.com/api/webhooks/FOO/BAR",
  "products": [
    {
      "name": "PRODUCT NAME",
      "sources": [
        {
          "name": "SOURCE NAME",
          "url": "URL TO FETCH",
          "watch": [
            "CSS SELECTOR TO WATCH FOR CHANGES",
          ]
        }
      ]
    }
  ]
}
```

The program will watch the given urls for changes in all text nodes.

To start the program, run:
```console
$ python app.py
```

I license this code as public domain - you can use it for whatever you please.

