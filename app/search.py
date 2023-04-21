from flask import current_app


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return None
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    pk = model.__primarykey__

    current_app.elasticsearch.index(index=index, id=getattr(model, pk), document=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return None
    pk = model.__primarykey__
    current_app.elasticsearch.delete(index=index, id=getattr(model, pk))

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return None
    search = current_app.elasticsearch.search(index=index, 
                                              body={'query': 
                                                    {'multi_match': {'query': query, 'fields': ['*']}},
                                                     'from': (page - 1) * per_page,
                                                      'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]  # 'post_id'
    total = search['hits']['total']['value']  # 1
    return ids, total