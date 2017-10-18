# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
ALFABETO = 'abcdefghijklmnopqrstuvwxyz'

def index():
    redirect(URL('default', 'cifrar'))

def cifrar():
    message = session.message_c if session.message_c else None

    form = SQLFORM.factory(
        Field('chave', 'integer', label='Chave:', default = session.chave_c,
            requires = [
                IS_NOT_EMPTY(error_message='Campo obrigatório'),
                IS_INT_IN_RANGE(0, 320, error_message='Precisa ser um número ente 0 e 320!')
            ]
        ),
        Field('texto', 'text', label='Texto:', default = session.texto_c,
            requires = [
                IS_NOT_EMPTY(error_message="Campo obrigatório"),
                IS_LENGTH(50)
            ]
        ),
    )

    if form.process().accepted:
        session.chave_c = request.vars.chave
        session.texto_c = request.vars.texto
        session.message_c = encrypt(int(request.vars.chave), request.vars.texto.lower())
        redirect(URL('default', 'index'))
    elif form.errors:
        response.flash = 'Ops, algo de errado não está certo'

    return dict(form=form, message=message)

def decifrar():
    message = session.message_d if session.message_d else None

    form = SQLFORM.factory(
        Field('chave', 'integer', label='Chave:', default = session.chave_d,
            requires = [
                IS_NOT_EMPTY(error_message='Campo obrigatório'),
                IS_INT_IN_RANGE(0, 320, error_message='Precisa ser um número ente 0 e 320!')
            ]
        ),
        Field('texto', 'text', label='Texto:', default = session.texto_d,
            requires = [
                IS_NOT_EMPTY(error_message="Campo obrigatório"),
                IS_LENGTH(50)
            ]
        ),
    )

    if form.process().accepted:
        session.chave_d = request.vars.chave
        session.texto_d = request.vars.texto
        session.message_d = decrypt(int(request.vars.chave), request.vars.texto.lower())
        redirect(URL('default', 'decifrar'))
    elif form.errors:
        response.flash = 'Ops, algo de errado não está certo'

    return dict(form=form, message=message)



def encrypt(chave, message):
    r = ''
    for c in message:
        if c in ALFABETO: # Se achar algum caractere que não esteja na lista, mantem iguam
            c_index = ALFABETO.index(c)
            r += ALFABETO[(c_index + chave) % len(ALFABETO)]
        else:
            r += c
    return r

def decrypt(chave, message):
    r = ''
    for c in message:
        if c in ALFABETO: # Se achar algum caractere que não esteja na lista, mantem iguam
            c_index = ALFABETO.index(c)
            r += ALFABETO[(c_index - chave) % len(ALFABETO)]
        else:
            r += c
    return r


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
