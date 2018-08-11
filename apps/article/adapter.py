# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/8/11 17:23'


from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/accounts/profile/{user_id}"
        return path.format(user_id=request.user.id)