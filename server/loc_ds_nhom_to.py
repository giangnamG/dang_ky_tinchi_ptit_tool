from access_qldt import AccessQLDT
from databases.core import DB

msv = 'b20dcat171'
password = '123456789'
new_user = AccessQLDT(username=msv, password=password)
response = new_user.login()
if response.get('code') == '200':
    ds_nhom_to = new_user.loc_ds_nhom_to().get('data').get('ds_nhom_to')
    for _ in ds_nhom_to:
        ma_mon = _.get('ma_mon')
        id_to_hoc = _.get('id_to_hoc')
        id_mon = _.get('id_mon')
        nhom_to = _.get('nhom_to')
        to = _.get('to')
        so_tc = _.get('so_tc')
        ds_lop = _.get('ds_lop')
        if len(ds_lop) > 0:
            ds_lop = _.get('ds_lop')[0]
        else:
            ds_lop = ''
        query = """
        insert into ds_nhom_to (ma_mon, id_to_hoc, id_mon, group_number, team_number, so_tc, ds_lop) values
        (%s, %s, %s, %s, %s, %s, %s)
        """
        DB().insert_data(query, (ma_mon, id_to_hoc, id_mon, nhom_to, to, so_tc, ds_lop))
        