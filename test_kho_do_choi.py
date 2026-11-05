from kho_do_choi import KHO, TRUY_VAN, QRELS

for ma_q, cau_hoi in TRUY_VAN.items():
    print(f"\nCau hoi {ma_q}: {cau_hoi}")

    for ma_tl, nhan in QRELS[ma_q].items():
        print(f"Tai lieu {ma_tl}: {KHO[ma_tl]}")
        print(f"Muc do lien quan: {nhan}")