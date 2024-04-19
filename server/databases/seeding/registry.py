import sys, os
sys.path.append(os.path.dirname(__file__))
import  attt_major, title_major,\
        cntt_major, cndpt_major,\
        kt_major, qtkd_major, ttdpt_major,\
        cnktddt_major, cntc_major,\
        users, roles, tmdt_major, cnttclc_major

def up():
    title_major.run()
    attt_major.run()
    cntt_major.run()
    cndpt_major.run()
    kt_major.run()
    qtkd_major.run()
    ttdpt_major.run()
    cnktddt_major.run()
    tmdt_major.run()
    cntc_major.run()
    cnttclc_major.run()
    users.run()
    roles.run()
    