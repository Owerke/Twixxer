from bottle import get, view, request, redirect, response, post
import common

@get("/logout")
@view("logout")
def get_logout():
    response.set_cookie(common.JWT_COOKIE, "", expires=0)
    print("#"*30)
    print("logout")
    return redirect("/login")
