from bottle import get, view, request, redirect, response, post
import common

@get("/logout")
@view("logout")
def get_logout():
    response.delete_cookie(common.JWT_COOKIE)
    print("#"*30)
    print("logout")
    return redirect("/login")
