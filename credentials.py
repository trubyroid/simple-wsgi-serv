from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape
from json import dumps


def application(environ, start_response):

    response_body, response_headers = [], []
    response_dict = {}
    status = "404 ERROR"
    person = "Unknown"

    persons = {
            "Cyberman": "John Lumic",
            "Dalek": "Davros",
            "Judoon": "Shadow Proclamation Convention 15 Enforcer",
            "Human": "Leonardo da Vinci",
            "Ood": "Klineman Halpen",
            "Silence": "Tasha Lem",
            "Slitheen": "Coca-Cola salesman",
            "Sontaran": "General Staal",
            "Time Lord": "Rassilon",
            "Weeping Angel": "The Division Representative",
            "Zygon": "Broton"
            }

    rm = environ.get("REQUEST_METHOD")

    if rm == "GET":
        qs = parse_qs(environ['QUERY_STRING'])
        if "species" in qs:
            species = qs.get("species")[0]
            species = escape(species)
            if species in persons.keys():
                status = '200 OK'
                person = persons[species]
            response_dict["credentials"] = person
            json_string = dumps(response_dict)
            response_body.append(json_string.encode('utf-8') +
                                 "\n".encode('utf-8'))

        content_length = sum([len(s) for s in response_body])
        response_headers = [('Content-Type',
                            'application/json; charset=utf-8'),
                            ('Content-Length', str(content_length))]
    start_response(status, response_headers)
    return response_body


def run_wsgi_server():
    httpd = make_server('localhost', 8888, application)
    httpd.serve_forever()


if __name__ == "__main__":
    run_wsgi_server()
