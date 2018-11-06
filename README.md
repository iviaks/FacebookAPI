# Django Facebook Application

## How to setup?

1.  Run `docker-compose build`
1.  Run `docker-compose run --rm backend python manage.py migrate`
1.  Run `docker-compose run --rm backend python manage.py createsuperuser`

## How to start?

Run `docker-compose up`

### Requirements

1.  You should create a few facebook pages (http://joxi.ru/n2YV9xMco1JR4A)
1.  Example for request data:

```json
{
  "users": ["103558563988536", "2055592611128180", "2025592611129180"],
  "page_id": "251462899052748",
  "label": "VIP1",
  "format": "json"
}
```
