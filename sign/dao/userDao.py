from sign.models import User



def get_user(account,password):
    print('acount======',account)
    #print(''' SELECT  * FROM user where account = '%s' ''' % ('jiyanjiao'))
    user_list = User.objects.raw(''' SELECT  * FROM user where account = '%s' and password = '%s' '''% (account,password))
    #user_list = User.objects.raw(''' SELECT  * FROM user where account = '%s' ''' ,[account])
    # for p in user_list:
    #     print('pp=========', p.phone)
    return user_list
