"""
CN Code Database Module
Contains emission intensity data for all CBAM-covered products
"""

CN_CODE_DATABASE = {
    # ÇELIK VE DEMİR
    "2601 12 00": {"description": "Agglomerated iron ores", "category": "Iron and Steel", "direct": 0.31, "indirect": 0.05, "total": 0.36},
    "7201": {"description": "Pig iron", "category": "Iron and Steel", "direct": 1.90, "indirect": 0.17, "total": 2.07},
    "7202 1": {"description": "Ferro-manganese", "category": "Iron and Steel", "direct": 1.44, "indirect": 2.08, "total": 3.51},
    "7202 4": {"description": "Ferro-chromium", "category": "Iron and Steel", "direct": 2.07, "indirect": 3.38, "total": 5.45},
    "7202 6": {"description": "Ferro-nickel", "category": "Iron and Steel", "direct": 3.48, "indirect": 2.81, "total": 6.26},
    "7203": {"description": "Direct reduction iron (DRI)", "category": "Iron and Steel", "direct": 4.81, "indirect": 0.00, "total": 4.81},
    "7206 10 00": {"description": "Ingots", "category": "Crude Steel", "direct": 2.52, "indirect": 0.23, "total": 2.75},
    "7206 90 00": {"description": "Other crude steel", "category": "Crude Steel", "direct": 1.97, "indirect": 0.23, "total": 2.20},
    "7208": {"description": "Flat-rolled products", "category": "Steel Products", "direct": 2.01, "indirect": 0.27, "total": 2.28},
    "7209": {"description": "Flat-rolled cold-rolled", "category": "Steel Products", "direct": 2.03, "indirect": 0.36, "total": 2.39},
    "7210": {"description": "Flat-rolled clad/plated", "category": "Steel Products", "direct": 1.97, "indirect": 0.39, "total": 2.35},
    "7213": {"description": "Bars and rods hot-rolled", "category": "Steel Products", "direct": 1.89, "indirect": 0.32, "total": 2.21},
    "7214 10 00": {"description": "Forged bars and rods", "category": "Steel Products", "direct": 2.65, "indirect": 0.62, "total": 3.27},
    "7216": {"description": "Angles and shapes", "category": "Steel Products", "direct": 1.89, "indirect": 0.32, "total": 2.21},
    "7217 10": {"description": "Wire not plated", "category": "Steel Products", "direct": 1.88, "indirect": 0.49, "total": 2.37},
    "7218 99 19": {"description": "Stainless steel forged", "category": "Stainless Steel", "direct": 2.51, "indirect": 2.10, "total": 4.61},
    "7219": {"description": "Flat-rolled stainless", "category": "Stainless Steel", "direct": 2.18, "indirect": 1.90, "total": 4.08},
    "7220": {"description": "Flat-rolled stainless <600mm", "category": "Stainless Steel", "direct": 2.18, "indirect": 1.90, "total": 4.08},
    "7222 20": {"description": "Stainless bars cold-formed", "category": "Stainless Steel", "direct": 2.14, "indirect": 2.17, "total": 4.30},
    
    # ÇİMENTO
    "2507 00 80": {"description": "Calcined kaolin clays", "category": "Cement", "direct": 0.23, "indirect": 0.08, "total": 0.32},
    "2523 10 00": {"description": "Cement clinkers", "category": "Cement", "direct": 0.83, "indirect": 0.04, "total": 0.87},
    "2523 21 00": {"description": "White Portland cement", "category": "Cement", "direct": 1.16, "indirect": 0.10, "total": 1.26},
    "2523 29 00": {"description": "Other Portland cement", "category": "Cement", "direct": 0.81, "indirect": 0.06, "total": 0.87},
    "2523 90 00": {"description": "Other hydraulic cements", "category": "Cement", "direct": 0.59, "indirect": 0.04, "total": 0.63},
    "2523 30 00": {"description": "Aluminous cement", "category": "Cement", "direct": 1.75, "indirect": 0.15, "total": 1.90},
    
    # ALÜMİNYUM
    "7601": {"description": "Unwrought aluminium", "category": "Aluminium", "direct": 2.36, "indirect": 8.14, "total": 10.49},
    "7603": {"description": "Aluminium powders and flakes", "category": "Aluminium Products", "direct": 2.48, "indirect": 8.40, "total": 10.88},
    "7604 10 10": {"description": "Aluminium bars not alloyed", "category": "Aluminium Products", "direct": 2.31, "indirect": 7.49, "total": 9.80},
    "7604 10 90": {"description": "Aluminium profiles not alloyed", "category": "Aluminium Products", "direct": 2.73, "indirect": 9.30, "total": 12.04},
    "7604 29 10": {"description": "Aluminium bars alloys", "category": "Aluminium Products", "direct": 2.31, "indirect": 7.49, "total": 9.80},
    "7605": {"description": "Aluminium wire", "category": "Aluminium Products", "direct": 2.31, "indirect": 7.49, "total": 9.80},
    "7606": {"description": "Aluminium plates and sheets", "category": "Aluminium Products", "direct": 2.86, "indirect": 9.25, "total": 12.11},
    "7607": {"description": "Aluminium foil", "category": "Aluminium Products", "direct": 2.86, "indirect": 9.25, "total": 12.11},
    "7608": {"description": "Aluminium tubes and pipes", "category": "Aluminium Products", "direct": 2.73, "indirect": 9.30, "total": 12.04},
    "7610": {"description": "Aluminium structures", "category": "Aluminium Products", "direct": 2.73, "indirect": 9.30, "total": 12.04},
    "7612": {"description": "Aluminium casks and drums", "category": "Aluminium Products", "direct": 2.86, "indirect": 9.25, "total": 12.11},
    "7614": {"description": "Aluminium cables", "category": "Aluminium Products", "direct": 2.31, "indirect": 7.49, "total": 9.80},
    
    # GÜBRE
    "2808 00 00": {"description": "Nitric acid", "category": "Fertilizers", "direct": 2.56, "indirect": 0.05, "total": 2.60},
    "2814": {"description": "Ammonia", "category": "Fertilizers", "direct": 2.68, "indirect": 0.14, "total": 2.82},
    "2834 21 00": {"description": "Nitrates of potassium", "category": "Fertilizers", "direct": 1.82, "indirect": 0.06, "total": 1.88},
    "3102 10": {"description": "Urea", "category": "Fertilizers", "direct": 1.78, "indirect": 0.12, "total": 1.90},
    "3102 21 00": {"description": "Ammonium sulphate", "category": "Fertilizers", "direct": 0.86, "indirect": 0.09, "total": 0.94},
    "3102 29 00": {"description": "Ammonium sulphate mixtures", "category": "Fertilizers", "direct": 1.54, "indirect": 0.10, "total": 1.63},
    "3102 30": {"description": "Ammonium nitrate", "category": "Fertilizers", "direct": 2.32, "indirect": 0.07, "total": 2.39},
    "3102 40": {"description": "Ammonium nitrate with calcium", "category": "Fertilizers", "direct": 1.77, "indirect": 0.06, "total": 1.84},
    "3102 50 00": {"description": "Sodium nitrate", "category": "Fertilizers", "direct": 3.99, "indirect": 0.07, "total": 4.06},
    "3105 10 00": {"description": "Fertilizers in tablets", "category": "Fertilizers", "direct": 0.94, "indirect": 0.08, "total": 1.02},
    
    # HİDROJEN
    "2804 10 00": {"description": "Hydrogen", "category": "Hydrogen", "direct": 10.40, "indirect": 0.00, "total": 10.40}
}

LEGACY_CATEGORIES = {
    "cement": {"direct": 0.83, "indirect": 0.04},
    "steel": {"direct": 2.30, "indirect": 0.25},
    "aluminium": {"direct": 2.36, "indirect": 8.14}
}


def get_all_cn_codes():
    """Returns list of all CN codes"""
    return list(CN_CODE_DATABASE.keys())


def get_categories():
    """Returns unique product categories"""
    return list(set(item["category"] for item in CN_CODE_DATABASE.values()))


def search_by_description(search_term):
    """Search products by description"""
    results = []
    search_term = search_term.lower()
    for code, data in CN_CODE_DATABASE.items():
        if search_term in data["description"].lower():
            results.append({"cn_code": code, **data})
    return results
