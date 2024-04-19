import sys
sys.path.append("../")
from core import DB

def run():
    majors = [
            {
                'name' : ' Chọn để xem môn học của các nghành',
                'type' : 'default'
            },
            {
                'name' : 'Truyền thông Đa phương tiện',
                'type' : 'ttdpt',
            },
            {
                'name' : 'Công nghệ Đa phương tiện',
                'type' : 'cndpt',
            },
            {
                'name' : 'Kế toán',
                'type' : 'kt',
            },
            {
                'name' : 'Quản trị kinh doanh',
                'type' : 'qtkd',
            },
            {
                'name' : 'An toàn thông tin',
                'type' : 'attt',
            },
            {
                'name' : 'Công nghệ thông tin',
                'type' : 'cntt',
            },
            {
                'name' : 'Điện tử – Viễn thông',
                'type' : 'dtvt'
            },
            {
                'name' : 'Công nghệ Kỹ thuật Điện, điện tử',
                'type' : 'cnktddt',
            },
            {
                'name' : 'Thương mại Điện tử',
                'type' : 'tmdt'
            },
            {
                'name' : 'Công nghệ Tài chính',
                'type' : 'cntc'
            },
            {
                'name' : 'Công nghệ thông tin chất lượng cao',
                'type' : 'cnttclc',
            },
            {
                'name' : 'Khoa học máy tính',
                'type' : 'khmt'
            },
            {
                'name' : 'Báo chí',
                'type' : 'bc',
            },
            {
                'name' : 'Marketing',
                'type' : 'mar'
            }
            ]
    query = "insert into majors (name_major, type) values (%s, %s)"
    for _ in majors:
        print(_)
        DB().insert_data(query,params=(
            _['name'],
            _['type'],
        ))