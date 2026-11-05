
# from collections import defaultdict
# from kho_do_choi import KHO

# chi_muc = defaultdict(list)

# def tach_khoang_trang(van_ban):
#     """Tach van ban thanh danh sach token theo khoang trang, ha chu thuong."""
#     return van_ban.lower().split()

# for ma_tai_lieu, van_ban in KHO.items():

#     # Câu 1: Tách văn bản thành danh sách từ
#     cac_tu =tach_khoang_trang(van_ban)

#     # Câu 2: Duyệt các từ không trùng lặp
    
#     for tu in set(cac_tu):
#         chi_muc[tu].append(ma_tai_lieu)

# print(chi_muc["tan"])
# print(chi_muc["do"])
# print(chi_muc["tai"])

# from bm25 import ChiMuc
# from kho_do_choi import KHO

# index = ChiMuc(KHO)
# print(KHO['d2'])
# print("So tai lieu:", index.n)
# print("Do dai d2:", index.do_dai["d2"])
# print("Tan so 'bm25' trong d2:", index.tf["d2"]["kkk"])
# print("Posting list 'tan':", index.chi_muc["tan"])
# print("Do dai trung binh:", index.avgdl)

#test tổng thể

from bm25 import ChiMuc
from kho_do_choi import KHO

index = ChiMuc(KHO)

print(index.diem("tan so tu"))
print(index.tim("tan so tu", k=3))