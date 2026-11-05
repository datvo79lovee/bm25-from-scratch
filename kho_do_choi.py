# -*- coding: utf-8 -*-
"""Kho do choi tam tai lieu, ba truy van, nhan nhieu muc.

Kho nay dung de kiem cach cai, khong dung de ket luan ve chat luong.
Van ban bo dau de khong lan sang phan tach tu tieng Viet o muc B2.

d7 la mot dong tieu de muc, khong chua noi dung nao; nhan cua no la 0.
d8 tra loi dung cau hoi cua q3 nhung khong dung mot tu nao cua q3.
"""

KHO = {
    "d1": "chi muc nghich dao luu danh sach tai lieu theo tung tu khoa",
    "d2": "bm25 tinh diem theo tan so tu va do dai tai lieu",
    "d3": "tan so tu can bao hoa nen bm25 dung mot phan so co tiem can",
    "d4": "do dai tai lieu duoc chuan hoa theo do dai trung binh cua kho",
    "d5": "phan dinh lien quan duoc gan boi nguoi theo he hinh cranfield",
    "d6": "pooling lay hop cua ket qua dau cua nhieu he thong khac nhau",
    "d7": "tan so tu va do dai tai lieu",
    "d8": "nhan dung cua tang truy xuat la tai lieu nao tra loi duoc cau hoi",
}

TRUY_VAN = {
    "q1": "tan so tu",
    "q2": "do dai tai lieu",
    "q3": "phan dinh lien quan",
}

# Nhan nhieu muc: 2 la lien quan truc tiep, 1 la lien quan mot phan.
QRELS = {
    "q1": {"d3": 2, "d2": 1},
    "q2": {"d4": 2, "d2": 1},
    "q3": {"d5": 2, "d8": 1},
}
