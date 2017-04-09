import json
import time
import os

from bottle import route, run, template, static_file, request, template, post, get
from dateutil import tz

from models import BaseIface, Category, SubCategory, Content, DataBaseException



JQUERY_VERSION = "1.7.2"
TZ = tz.gettz('Paris/Europe')


@route('/static/:filename')
def send_static(filename):
    """Return statics files"""
    return static_file(filename, root='./static/')


# Ajax views prefixed by '_'

@post('/_category')
def _category():
    """Get all category"""
    q = BaseIface.get_all_category()
    response = []
    for ellmt in q:
        response.append(  [ ellmt.id,  ellmt.category_name ]  )

    return json.dumps(response)

@post('/_delete_content')
def _delete_content():
    to_delete_content = request.forms.get('to_delete_content')
    q = BaseIface.delete_content(to_delete_content)
    if q:
        return json.dumps([1,])

@post('/_sub_category')
def _sub_category():
    """ Get sub category depend to received category"""
    to_search_category = request.forms.get('to_search_category')
    q = BaseIface.get_sub_category(to_search_category)
    response = []
    for ellmt in q:
        response.append([ ellmt.id, ellmt.sub_category_name ])

    return json.dumps(response)


@post('/_content')
def _content():
    """ Get content depend to received category and sub-category"""
    to_search_category = request.forms.get('to_search_category')
    to_search_sub_category = request.forms.get('to_search_sub_category')
    to_search_description = request.forms.get('to_search_description', default='')
    q = BaseIface.get_content(to_search_category, to_search_sub_category, to_search_description )
    response = []
    for ellmt in q:
        parsed_descr = ellmt.description
        parsed_contt = ellmt.content.replace('\n', '<br>')
        while '\n' in parsed_descr:parsed_descr = parsed_descr.replace('\n', '<br>')
        while '\n' in parsed_contt: parsed_contt = parsed_contt.replace('\n', '<br>')
        response.append([ellmt.id, ellmt.date_parsed, parsed_descr,parsed_contt ])

    return json.dumps(response , ensure_ascii=False).encode('ISO-8859-1')


@post('/_add_category_content')
def _add_category_content():
    """ Add content and categorys, return a dict contain "valid" or "errors" key """
    category = request.forms.get("to_insert_category", default=False)
    sub_category = request.forms.get("to_insert_sub_category", default=False)
    description = request.forms.get("to_insert_description", default=False)
    content = request.forms.get("to_insert_content", default=False)
    response = []
    # Category and sub-category must exist for save content
    if category and sub_category:
        try:
            category = int(category)
        except ValueError as e:
            q = BaseIface.add_category(category)
            category = q.id
        try:
            sub_category = int(sub_category)
        except ValueError as e:
            q = BaseIface.add_sub_category(category, sub_category)
            sub_category = q.id

    # If they not exist return error.
    else:
        return json.dumps({"errors" : "Faut créer ou ajouter une catégorie et une sous catégorie avant d'ajouter du contenu."})
    # If content, try to save it
    if content:
        try:
            q = BaseIface.add_content(category, sub_category, description, content)
            response.append([q.id, q.date_parsed, q.description, q.content])

            if q:
                return json.dumps({"valid" : response})

        except Exception as e:
            raise (e)
            return json.dumps({"errors": "Le contenu n'a pas été sauvé."})
    return  json.dumps({"errors": "Le formulaire n'est pas complet."})



# Users pages


@route('/')
def root():
    return template('templates/main_page.tpl')


@route('/login')
def login():
    LIST_IP_DIR = 'ip'
    LIST_BAN_IP = 'ip/ban'
    try:
        os.mkdir(LIST_IP_DIR)
    except:
        pass
    try:
        os.mkdir(LIST_BAN_IP)
    except:
        pass

    client_ip = request.environ.get('REMOTE_ADDR')
    while '.' in client_ip:client_ip = client_ip.replace('.', '-')
    if not os.path.isfile(LIST_BAN_IP + client_ip + '.ban'):

        try:
            with open(client_ip + '.txt', 'r') as fil:
                count, timest = fil.read().split('|')
                count, timest = int(count), int(timest)
        except FileNotFoundError:
            with open(client_ip + '.txt', 'w') as fil:
                fil.wite('0|'+str(time.time()))
                count = 0
    else:
        with open(LIST_BAN_IP + client_ip + '.ban', 'r') as fil:
            timest = int(fil.read())

        if time.time() - timest > 345600:
            os.remove(LIST_BAN_IP + client_ip + '.ban')
        else:
            return ['You are banned :) ']

    if count > 5:
        with open(LIST_BAN_IP + client_ip + '.ban', 'w') as fil:
            fil.write(str(time.time()))






    return ['Your IP is: {}\n'.format(client_ip)]


run(host='localhost', port=8000, debug=True, reloader=True)
