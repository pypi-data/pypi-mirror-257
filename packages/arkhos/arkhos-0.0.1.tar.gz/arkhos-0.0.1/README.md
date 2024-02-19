# The Arkhos Python Client

[Arkhos](https://www.getArkhos.com>) is a Python framework for quickly deploying tiny Python apps.

```python
# main.py
def arkhos_handler(event):
    return arkhos.json({
        "greeting": f"Hello {event.GET.get("name")}!"
    })

```

```bash
$ git add main.py
$ git push arkhos
$ curl "https://my-first-app.arkhosapp.com?name=Wally"
{
  "greeting": "Hello Wally!"
}
```
