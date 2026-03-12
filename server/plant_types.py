"""
Plant Types Database - מאגר סוגי צמחים
=======================================
מאגר מקיף של צמחי בית, גינה, תבלינים וירקות
כולל דרישות לחות קרקע, טמפרטורה וטיפים

moisture_min/max = אחוזי לחות קרקע מומלצים (0-100)
temp_min/max = טווח טמפרטורה מומלץ (צלזיוס)
"""

PLANTS = [
    # ==================== צמחי בית נפוצים ====================
    {"id": "ficus_benjamina", "name_he": "פיקוס בנימינה", "name_en": "Ficus Benjamina", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 16, "temp_max": 30, "water_tip_he": "השקה כשהקרקע יבשה בס\"מ העליון"},
    {"id": "ficus_elastica", "name_he": "פיקוס גומי", "name_en": "Rubber Plant", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 15, "temp_max": 30, "water_tip_he": "השקה כשהקרקע יבשה למגע"},
    {"id": "ficus_lyrata", "name_he": "פיקוס כינור", "name_en": "Fiddle Leaf Fig", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 16, "temp_max": 28, "water_tip_he": "השקה כשהקרקע יבשה ב-2-3 ס\"מ העליונים"},
    {"id": "pothos", "name_he": "פוטוס", "name_en": "Pothos", "category": "medium", "moisture_min": 35, "moisture_max": 60, "temp_min": 15, "temp_max": 30, "water_tip_he": "צמח סלחני - השקה כשהעלים מתחילים לרדת"},
    {"id": "monstera", "name_he": "מונסטרה", "name_en": "Monstera Deliciosa", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 18, "temp_max": 30, "water_tip_he": "השקה כשהקרקע יבשה ב-3 ס\"מ העליונים"},
    {"id": "monstera_adansonii", "name_he": "מונסטרה אדנסוני", "name_en": "Monstera Adansonii", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 18, "temp_max": 30, "water_tip_he": "אוהבת לחות קצת יותר גבוהה ממונסטרה רגילה"},
    {"id": "spathiphyllum", "name_he": "ספטיפיליום (שושנת השלום)", "name_en": "Peace Lily", "category": "high", "moisture_min": 50, "moisture_max": 75, "temp_min": 18, "temp_max": 30, "water_tip_he": "אוהב לחות - השקה לפני שהעלים מתחילים לרדת"},
    {"id": "sansevieria", "name_he": "סנסווריה (חרב)", "name_en": "Snake Plant", "category": "low", "moisture_min": 15, "moisture_max": 40, "temp_min": 10, "temp_max": 35, "water_tip_he": "מעט מים - השקה רק כשהקרקע יבשה לגמרי"},
    {"id": "aloe_vera", "name_he": "אלוורה", "name_en": "Aloe Vera", "category": "low", "moisture_min": 10, "moisture_max": 35, "temp_min": 10, "temp_max": 35, "water_tip_he": "השקה מעט - הקרקע חייבת להתייבש בין השקיות"},
    {"id": "dracaena_marginata", "name_he": "דרצנה מרגינטה", "name_en": "Dragon Tree", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 15, "temp_max": 30, "water_tip_he": "השקה כשחצי העליון של הקרקע יבש"},
    {"id": "dracaena_fragrans", "name_he": "דרצנה פרגרנס", "name_en": "Corn Plant", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 15, "temp_max": 30, "water_tip_he": "השקה כשהקרקע יבשה ב-2-3 ס\"מ"},
    {"id": "dracaena_warneckii", "name_he": "דרצנה וורנקי", "name_en": "Dracaena Warneckii", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 15, "temp_max": 30, "water_tip_he": "השקה מתונה, הימנע מהצפה"},
    {"id": "zamioculcas", "name_he": "זמיוקולקס (ZZ)", "name_en": "ZZ Plant", "category": "low", "moisture_min": 15, "moisture_max": 40, "temp_min": 15, "temp_max": 30, "water_tip_he": "עמיד מאוד - השקה רק כשהקרקע יבשה לחלוטין"},
    {"id": "philodendron_heartleaf", "name_he": "פילודנדרון לב", "name_en": "Heartleaf Philodendron", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 16, "temp_max": 28, "water_tip_he": "השקה כשהקרקע יבשה בס\"מ העליון"},
    {"id": "philodendron_birkin", "name_he": "פילודנדרון בירקין", "name_en": "Philodendron Birkin", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 16, "temp_max": 28, "water_tip_he": "שמור על לחות קבועה, לא רטוב מדי"},
    {"id": "philodendron_xanadu", "name_he": "פילודנדרון קסנדו", "name_en": "Philodendron Xanadu", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 16, "temp_max": 30, "water_tip_he": "השקה כשהקרקע יבשה למחצה"},
    {"id": "calathea", "name_he": "קלתיאה", "name_en": "Calathea", "category": "high", "moisture_min": 55, "moisture_max": 75, "temp_min": 18, "temp_max": 27, "water_tip_he": "לחות גבוהה - השתמש במים מסוננים, רגישה לכלור"},
    {"id": "calathea_orbifolia", "name_he": "קלתיאה אורביפוליה", "name_en": "Calathea Orbifolia", "category": "high", "moisture_min": 55, "moisture_max": 75, "temp_min": 18, "temp_max": 27, "water_tip_he": "לחות גבוהה, רגישה מאוד למים קשים"},
    {"id": "maranta", "name_he": "מרנתה (צמח התפילה)", "name_en": "Prayer Plant", "category": "high", "moisture_min": 50, "moisture_max": 70, "temp_min": 18, "temp_max": 28, "water_tip_he": "אוהבת לחות - השקה במים פושרים"},
    {"id": "croton", "name_he": "קרוטון", "name_en": "Croton", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 16, "temp_max": 30, "water_tip_he": "שמור על לחות קבועה, לא להציף"},
    {"id": "dieffenbachia", "name_he": "דיפנבכיה", "name_en": "Dieffenbachia", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 16, "temp_max": 30, "water_tip_he": "השקה כשהקרקע יבשה בס\"מ העליון"},
    {"id": "schefflera", "name_he": "שפלרה", "name_en": "Umbrella Plant", "category": "medium", "moisture_min": 35, "moisture_max": 60, "temp_min": 15, "temp_max": 28, "water_tip_he": "השקה מתונה, תן לקרקע להתייבש קצת"},
    {"id": "chlorophytum", "name_he": "כלורופיטום (עכביש)", "name_en": "Spider Plant", "category": "medium", "moisture_min": 35, "moisture_max": 60, "temp_min": 12, "temp_max": 30, "water_tip_he": "סלחני - השקה כשהקרקע יבשה"},
    {"id": "asparagus_fern", "name_he": "אספרגוס (שרך)", "name_en": "Asparagus Fern", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 13, "temp_max": 28, "water_tip_he": "שמור על לחות, אל תתן לקרקע להתייבש לגמרי"},
    {"id": "boston_fern", "name_he": "שרך בוסטון", "name_en": "Boston Fern", "category": "high", "moisture_min": 60, "moisture_max": 80, "temp_min": 15, "temp_max": 27, "water_tip_he": "צריך לחות גבוהה מאוד - רסס בקביעות"},
    {"id": "maidenhair_fern", "name_he": "שערות שולמית", "name_en": "Maidenhair Fern", "category": "high", "moisture_min": 60, "moisture_max": 80, "temp_min": 15, "temp_max": 25, "water_tip_he": "רגיש מאוד ליובש - שמור על לחות קבועה"},
    {"id": "birds_nest_fern", "name_he": "שרך קן ציפור", "name_en": "Bird's Nest Fern", "category": "high", "moisture_min": 55, "moisture_max": 75, "temp_min": 16, "temp_max": 27, "water_tip_he": "השקה לקרקע, לא לתוך הרוזטה"},
    {"id": "alocasia", "name_he": "אלוקסיה", "name_en": "Alocasia", "category": "high", "moisture_min": 50, "moisture_max": 70, "temp_min": 18, "temp_max": 30, "water_tip_he": "לחות גבוהה אבל לא להציף - ניקוז טוב חובה"},
    {"id": "aglaonema", "name_he": "אגלאונמה", "name_en": "Chinese Evergreen", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 16, "temp_max": 30, "water_tip_he": "השקה כשהקרקע יבשה, סלחנית למדי"},
    {"id": "anthurium", "name_he": "אנטוריום", "name_en": "Anthurium", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 18, "temp_max": 28, "water_tip_he": "לחות קבועה, ניקוז טוב"},
    {"id": "begonia", "name_he": "בגוניה", "name_en": "Begonia", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 15, "temp_max": 27, "water_tip_he": "השקה כשהקרקע יבשה בס\"מ העליון, הימנע מהרטבת עלים"},
    {"id": "tradescantia", "name_he": "טרדסקנטיה (יהודי נודד)", "name_en": "Tradescantia", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 13, "temp_max": 28, "water_tip_he": "השקה מתונה, סלחנית"},
    {"id": "peperomia", "name_he": "פפרומיה", "name_en": "Peperomia", "category": "low", "moisture_min": 25, "moisture_max": 50, "temp_min": 15, "temp_max": 28, "water_tip_he": "השקה מעט - רגישה להצפה"},
    {"id": "pilea", "name_he": "פילאה (צמח המטבע)", "name_en": "Pilea Peperomioides", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 13, "temp_max": 28, "water_tip_he": "השקה כשהקרקע יבשה, ניקוז טוב"},
    {"id": "string_of_pearls", "name_he": "מחרוזת פנינים", "name_en": "String of Pearls", "category": "low", "moisture_min": 15, "moisture_max": 35, "temp_min": 12, "temp_max": 30, "water_tip_he": "השקה מעט - סוקולנט תלוי"},
    {"id": "string_of_hearts", "name_he": "מחרוזת לבבות", "name_en": "String of Hearts", "category": "low", "moisture_min": 15, "moisture_max": 40, "temp_min": 12, "temp_max": 30, "water_tip_he": "השקה רק כשהקרקע יבשה לגמרי"},
    {"id": "hoya", "name_he": "הויה", "name_en": "Hoya", "category": "low", "moisture_min": 25, "moisture_max": 45, "temp_min": 15, "temp_max": 30, "water_tip_he": "תן לקרקע להתייבש בין השקיות"},
    {"id": "syngonium", "name_he": "סינגוניום", "name_en": "Syngonium", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 16, "temp_max": 28, "water_tip_he": "לחות קבועה, סלחני"},
    {"id": "yucca", "name_he": "יוקה", "name_en": "Yucca", "category": "low", "moisture_min": 15, "moisture_max": 40, "temp_min": 7, "temp_max": 35, "water_tip_he": "עמיד מאוד - השקה מעט"},
    {"id": "palm_areca", "name_he": "דקל אריקה", "name_en": "Areca Palm", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 16, "temp_max": 30, "water_tip_he": "השקה כשהקרקע יבשה בס\"מ העליון"},
    {"id": "palm_kentia", "name_he": "דקל קנטיה", "name_en": "Kentia Palm", "category": "medium", "moisture_min": 35, "moisture_max": 60, "temp_min": 15, "temp_max": 30, "water_tip_he": "סלחני - השקה כשהקרקע יבשה"},
    {"id": "palm_parlor", "name_he": "דקל סלון", "name_en": "Parlor Palm", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 16, "temp_max": 28, "water_tip_he": "השקה מתונה ובקביעות"},
    {"id": "palm_majesty", "name_he": "דקל מג'סטי", "name_en": "Majesty Palm", "category": "high", "moisture_min": 50, "moisture_max": 70, "temp_min": 18, "temp_max": 30, "water_tip_he": "אוהב לחות גבוהה"},
    {"id": "strelitzia", "name_he": "סטרליציה (ציפור גן עדן)", "name_en": "Bird of Paradise", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 15, "temp_max": 30, "water_tip_he": "השקה כשהקרקע יבשה ב-2-3 ס\"מ"},
    {"id": "ctenanthe", "name_he": "קטננתה", "name_en": "Ctenanthe", "category": "high", "moisture_min": 50, "moisture_max": 70, "temp_min": 16, "temp_max": 27, "water_tip_he": "לחות קבועה, רגישה ליובש"},
    {"id": "fittonia", "name_he": "פיטוניה", "name_en": "Nerve Plant", "category": "high", "moisture_min": 55, "moisture_max": 75, "temp_min": 18, "temp_max": 28, "water_tip_he": "רגישה מאוד - מתעלפת כשיבשה"},
    {"id": "oxalis", "name_he": "חמציץ", "name_en": "Oxalis", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 12, "temp_max": 25, "water_tip_he": "השקה מתונה, נכנס לתרדמה"},
    {"id": "cyclamen", "name_he": "רקפת", "name_en": "Cyclamen", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 10, "temp_max": 20, "water_tip_he": "השקה מלמטה, אוהב קור"},
    {"id": "african_violet", "name_he": "סיגלית אפריקאית", "name_en": "African Violet", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 18, "temp_max": 27, "water_tip_he": "השקה מלמטה, לא להרטיב עלים"},
    {"id": "bromeliad", "name_he": "ברומליה", "name_en": "Bromeliad", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 16, "temp_max": 30, "water_tip_he": "מלא מים בגביע המרכזי"},
    {"id": "tillandsia", "name_he": "טילנדסיה (צמח אוויר)", "name_en": "Air Plant", "category": "low", "moisture_min": 10, "moisture_max": 30, "temp_min": 12, "temp_max": 32, "water_tip_he": "השרה במים פעם בשבוע ל-20 דקות"},

    # ==================== סוקולנטים וקקטוסים ====================
    {"id": "echeveria", "name_he": "אצ'ווריה", "name_en": "Echeveria", "category": "low", "moisture_min": 10, "moisture_max": 30, "temp_min": 10, "temp_max": 35, "water_tip_he": "השקה מעט - תן לקרקע להתייבש לגמרי"},
    {"id": "haworthia", "name_he": "חוורטיה", "name_en": "Haworthia", "category": "low", "moisture_min": 10, "moisture_max": 35, "temp_min": 10, "temp_max": 32, "water_tip_he": "השקה מעט, עמידה"},
    {"id": "crassula", "name_he": "קרסולה (עץ הכסף)", "name_en": "Jade Plant", "category": "low", "moisture_min": 10, "moisture_max": 35, "temp_min": 10, "temp_max": 30, "water_tip_he": "השקה רק כשהקרקע יבשה לחלוטין"},
    {"id": "sedum", "name_he": "סדום", "name_en": "Sedum", "category": "low", "moisture_min": 10, "moisture_max": 30, "temp_min": 5, "temp_max": 35, "water_tip_he": "מינימום מים"},
    {"id": "kalanchoe", "name_he": "קלנכואה", "name_en": "Kalanchoe", "category": "low", "moisture_min": 15, "moisture_max": 35, "temp_min": 12, "temp_max": 30, "water_tip_he": "השקה מעט, ניקוז מצוין"},
    {"id": "sempervivum", "name_he": "צמח-עד (סמפרוויוום)", "name_en": "Sempervivum", "category": "low", "moisture_min": 10, "moisture_max": 25, "temp_min": -10, "temp_max": 35, "water_tip_he": "כמעט לא צריך השקיה"},
    {"id": "lithops", "name_he": "אבנים חיות", "name_en": "Lithops", "category": "low", "moisture_min": 5, "moisture_max": 20, "temp_min": 10, "temp_max": 35, "water_tip_he": "השקה רק כמה פעמים בשנה!"},
    {"id": "cactus_barrel", "name_he": "קקטוס חבית", "name_en": "Barrel Cactus", "category": "low", "moisture_min": 5, "moisture_max": 25, "temp_min": 10, "temp_max": 40, "water_tip_he": "השקה פעם בחודש בקיץ, פחות בחורף"},
    {"id": "cactus_prickly_pear", "name_he": "צבר", "name_en": "Prickly Pear Cactus", "category": "low", "moisture_min": 5, "moisture_max": 25, "temp_min": 5, "temp_max": 40, "water_tip_he": "מינימום מים, עמיד מאוד"},
    {"id": "cactus_christmas", "name_he": "קקטוס חג המולד", "name_en": "Christmas Cactus", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 15, "temp_max": 27, "water_tip_he": "קקטוס טרופי - צריך יותר מים מקקטוס רגיל"},
    {"id": "euphorbia", "name_he": "חלבלוב", "name_en": "Euphorbia", "category": "low", "moisture_min": 10, "moisture_max": 30, "temp_min": 10, "temp_max": 35, "water_tip_he": "השקה מעט, דומה לקקטוס"},
    {"id": "adenium", "name_he": "ורד המדבר", "name_en": "Desert Rose", "category": "low", "moisture_min": 15, "moisture_max": 35, "temp_min": 15, "temp_max": 38, "water_tip_he": "השקה מעט, אוהב חום"},

    # ==================== תבלינים ====================
    {"id": "basil", "name_he": "בזיליקום", "name_en": "Basil", "category": "high", "moisture_min": 50, "moisture_max": 70, "temp_min": 18, "temp_max": 30, "water_tip_he": "אוהב לחות - השקה כשפני הקרקע יבשים"},
    {"id": "mint", "name_he": "נענע", "name_en": "Mint", "category": "high", "moisture_min": 50, "moisture_max": 75, "temp_min": 13, "temp_max": 28, "water_tip_he": "צמא מאוד - שמור על קרקע לחה תמיד"},
    {"id": "rosemary", "name_he": "רוזמרין", "name_en": "Rosemary", "category": "low", "moisture_min": 20, "moisture_max": 45, "temp_min": 5, "temp_max": 30, "water_tip_he": "ים-תיכוני - השקה מעט, אוהב יובש"},
    {"id": "thyme", "name_he": "קורנית (טימין)", "name_en": "Thyme", "category": "low", "moisture_min": 20, "moisture_max": 40, "temp_min": 5, "temp_max": 30, "water_tip_he": "השקה מעט, ניקוז טוב"},
    {"id": "oregano", "name_he": "אורגנו", "name_en": "Oregano", "category": "low", "moisture_min": 20, "moisture_max": 45, "temp_min": 10, "temp_max": 30, "water_tip_he": "ים-תיכוני - מעדיף קרקע יבשה"},
    {"id": "parsley", "name_he": "פטרוזיליה", "name_en": "Parsley", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 10, "temp_max": 25, "water_tip_he": "השקה בקביעות, אוהבת לחות"},
    {"id": "cilantro", "name_he": "כוסברה", "name_en": "Cilantro", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 10, "temp_max": 25, "water_tip_he": "השקה בקביעות, לא אוהבת חום"},
    {"id": "sage", "name_he": "מרווה", "name_en": "Sage", "category": "low", "moisture_min": 20, "moisture_max": 45, "temp_min": 5, "temp_max": 30, "water_tip_he": "ים-תיכוני - השקה מעט"},
    {"id": "lavender", "name_he": "לבנדר", "name_en": "Lavender", "category": "low", "moisture_min": 15, "moisture_max": 40, "temp_min": 5, "temp_max": 32, "water_tip_he": "אוהב יובש - השקה מעט מאוד"},
    {"id": "chives", "name_he": "עירית (שאלוט ירוק)", "name_en": "Chives", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 5, "temp_max": 25, "water_tip_he": "השקה בקביעות"},
    {"id": "dill", "name_he": "שמיר", "name_en": "Dill", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 10, "temp_max": 25, "water_tip_he": "השקה בקביעות, לא אוהב חום קיצוני"},
    {"id": "lemongrass", "name_he": "עשב לימון", "name_en": "Lemongrass", "category": "high", "moisture_min": 50, "moisture_max": 70, "temp_min": 15, "temp_max": 35, "water_tip_he": "אוהב לחות וחום"},
    {"id": "zaatar", "name_he": "זעתר", "name_en": "Za'atar / Hyssop", "category": "low", "moisture_min": 15, "moisture_max": 40, "temp_min": 5, "temp_max": 35, "water_tip_he": "צמח ארץ-ישראלי - מעט מים"},

    # ==================== ירקות ====================
    {"id": "tomato", "name_he": "עגבניה", "name_en": "Tomato", "category": "high", "moisture_min": 55, "moisture_max": 75, "temp_min": 18, "temp_max": 32, "water_tip_he": "השקה בקביעות ובעומק - לא על העלים"},
    {"id": "pepper", "name_he": "פלפל", "name_en": "Pepper", "category": "medium", "moisture_min": 45, "moisture_max": 70, "temp_min": 18, "temp_max": 32, "water_tip_he": "השקה בקביעות, מעדיף חום"},
    {"id": "hot_pepper", "name_he": "פלפל חריף", "name_en": "Hot Pepper / Chili", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 18, "temp_max": 35, "water_tip_he": "השקה מתונה, אוהב חום"},
    {"id": "cucumber", "name_he": "מלפפון", "name_en": "Cucumber", "category": "high", "moisture_min": 60, "moisture_max": 80, "temp_min": 18, "temp_max": 32, "water_tip_he": "צמא מאוד - שמור על לחות גבוהה"},
    {"id": "lettuce", "name_he": "חסה", "name_en": "Lettuce", "category": "high", "moisture_min": 55, "moisture_max": 75, "temp_min": 10, "temp_max": 22, "water_tip_he": "לחות קבועה, לא אוהבת חום"},
    {"id": "spinach", "name_he": "תרד", "name_en": "Spinach", "category": "high", "moisture_min": 50, "moisture_max": 70, "temp_min": 5, "temp_max": 22, "water_tip_he": "לחות קבועה, מעדיף קור"},
    {"id": "eggplant", "name_he": "חציל", "name_en": "Eggplant", "category": "medium", "moisture_min": 45, "moisture_max": 70, "temp_min": 20, "temp_max": 35, "water_tip_he": "השקה בקביעות, אוהב חום"},
    {"id": "zucchini", "name_he": "קישוא", "name_en": "Zucchini", "category": "high", "moisture_min": 55, "moisture_max": 75, "temp_min": 18, "temp_max": 32, "water_tip_he": "השקה שופעת ובקביעות"},
    {"id": "strawberry", "name_he": "תות", "name_en": "Strawberry", "category": "high", "moisture_min": 55, "moisture_max": 75, "temp_min": 10, "temp_max": 28, "water_tip_he": "לחות קבועה, ניקוז טוב"},
    {"id": "carrot", "name_he": "גזר", "name_en": "Carrot", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 10, "temp_max": 25, "water_tip_he": "השקה קבועה ואחידה"},
    {"id": "onion", "name_he": "בצל", "name_en": "Onion", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 10, "temp_max": 28, "water_tip_he": "השקה מתונה, הפסק לפני הקטיף"},
    {"id": "garlic", "name_he": "שום", "name_en": "Garlic", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 5, "temp_max": 25, "water_tip_he": "השקה מתונה, הפסק לפני הקטיף"},
    {"id": "bean", "name_he": "שעועית", "name_en": "Bean", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 18, "temp_max": 30, "water_tip_he": "השקה בקביעות, במיוחד בפריחה"},
    {"id": "pea", "name_he": "אפונה", "name_en": "Pea", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 8, "temp_max": 22, "water_tip_he": "לחות קבועה, מעדיף קור"},
    {"id": "radish", "name_he": "צנון", "name_en": "Radish", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 8, "temp_max": 22, "water_tip_he": "לחות אחידה למניעת סדיקה"},
    {"id": "sweet_potato", "name_he": "בטטה", "name_en": "Sweet Potato", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 18, "temp_max": 35, "water_tip_he": "השקה מתונה, אוהבת חום"},
    {"id": "corn", "name_he": "תירס", "name_en": "Corn", "category": "high", "moisture_min": 55, "moisture_max": 75, "temp_min": 18, "temp_max": 35, "water_tip_he": "צמא מאוד במיוחד בפריחה"},
    {"id": "watermelon", "name_he": "אבטיח", "name_en": "Watermelon", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 20, "temp_max": 35, "water_tip_he": "השקה עמוקה אבל לא תכופה"},
    {"id": "melon", "name_he": "מלון", "name_en": "Melon", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 20, "temp_max": 35, "water_tip_he": "השקה עמוקה, הפחת לפני הקטיף"},

    # ==================== פרחים ====================
    {"id": "rose", "name_he": "ורד", "name_en": "Rose", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 10, "temp_max": 30, "water_tip_he": "השקה עמוקה בבסיס, לא על העלים"},
    {"id": "geranium", "name_he": "גרניום (פלרגון)", "name_en": "Geranium", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 10, "temp_max": 30, "water_tip_he": "השקה כשהקרקע יבשה, סלחני"},
    {"id": "jasmine", "name_he": "יסמין", "name_en": "Jasmine", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 12, "temp_max": 30, "water_tip_he": "לחות קבועה, ניקוז טוב"},
    {"id": "hibiscus", "name_he": "היביסקוס", "name_en": "Hibiscus", "category": "high", "moisture_min": 50, "moisture_max": 70, "temp_min": 15, "temp_max": 35, "water_tip_he": "אוהב לחות וחום"},
    {"id": "bougainvillea", "name_he": "בוגנוויליה", "name_en": "Bougainvillea", "category": "low", "moisture_min": 20, "moisture_max": 40, "temp_min": 10, "temp_max": 38, "water_tip_he": "פורח יותר כשמשקים פחות"},
    {"id": "gardenia", "name_he": "גרדניה", "name_en": "Gardenia", "category": "high", "moisture_min": 50, "moisture_max": 70, "temp_min": 16, "temp_max": 28, "water_tip_he": "לחות גבוהה, מים חומציים"},
    {"id": "orchid_phalaenopsis", "name_he": "סחלב פלנופסיס", "name_en": "Phalaenopsis Orchid", "category": "low", "moisture_min": 25, "moisture_max": 45, "temp_min": 18, "temp_max": 28, "water_tip_he": "השרה פעם בשבוע, תן לייבוש מלא"},
    {"id": "orchid_dendrobium", "name_he": "סחלב דנדרוביום", "name_en": "Dendrobium Orchid", "category": "low", "moisture_min": 25, "moisture_max": 45, "temp_min": 15, "temp_max": 30, "water_tip_he": "השקה כשהמצע יבש"},
    {"id": "plumeria", "name_he": "פלומריה (יסמין הוואי)", "name_en": "Plumeria", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 15, "temp_max": 35, "water_tip_he": "השקה מתונה, פחות בחורף"},
    {"id": "chrysanthemum", "name_he": "חרצית", "name_en": "Chrysanthemum", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 10, "temp_max": 25, "water_tip_he": "לחות קבועה, ניקוז טוב"},
    {"id": "sunflower", "name_he": "חמנייה", "name_en": "Sunflower", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 15, "temp_max": 35, "water_tip_he": "השקה עמוקה, עמיד ליובש"},

    # ==================== עצים ושיחים ====================
    {"id": "olive", "name_he": "זית", "name_en": "Olive Tree", "category": "low", "moisture_min": 15, "moisture_max": 40, "temp_min": 5, "temp_max": 38, "water_tip_he": "ים-תיכוני - מעט מים, עמיד מאוד"},
    {"id": "lemon", "name_he": "לימון", "name_en": "Lemon Tree", "category": "medium", "moisture_min": 40, "moisture_max": 65, "temp_min": 10, "temp_max": 35, "water_tip_he": "השקה בקביעות, ניקוז מצוין"},
    {"id": "orange", "name_he": "תפוז", "name_en": "Orange Tree", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 10, "temp_max": 35, "water_tip_he": "השקה עמוקה ובקביעות"},
    {"id": "avocado", "name_he": "אבוקדו", "name_en": "Avocado", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 12, "temp_max": 32, "water_tip_he": "השקה שופעת, ניקוז מצוין - רגיש להצפה"},
    {"id": "fig", "name_he": "תאנה", "name_en": "Fig Tree", "category": "medium", "moisture_min": 35, "moisture_max": 55, "temp_min": 8, "temp_max": 35, "water_tip_he": "השקה מתונה, עמיד"},
    {"id": "pomegranate", "name_he": "רימון", "name_en": "Pomegranate", "category": "low", "moisture_min": 25, "moisture_max": 45, "temp_min": 5, "temp_max": 38, "water_tip_he": "עמיד ליובש, השקה מעט"},
    {"id": "grape", "name_he": "גפן", "name_en": "Grape Vine", "category": "low", "moisture_min": 25, "moisture_max": 50, "temp_min": 5, "temp_max": 35, "water_tip_he": "השקה עמוקה ולא תכופה"},
    {"id": "mango", "name_he": "מנגו", "name_en": "Mango", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 15, "temp_max": 38, "water_tip_he": "השקה בקביעות, אוהב חום"},
    {"id": "banana", "name_he": "בננה", "name_en": "Banana", "category": "high", "moisture_min": 55, "moisture_max": 75, "temp_min": 18, "temp_max": 35, "water_tip_he": "צמא מאוד - לחות גבוהה תמיד"},
    {"id": "guava", "name_he": "גויאבה", "name_en": "Guava", "category": "medium", "moisture_min": 40, "moisture_max": 60, "temp_min": 15, "temp_max": 35, "water_tip_he": "השקה בקביעות"},
    {"id": "passion_fruit", "name_he": "פסיפלורה (שעונית)", "name_en": "Passion Fruit", "category": "medium", "moisture_min": 45, "moisture_max": 65, "temp_min": 15, "temp_max": 32, "water_tip_he": "לחות קבועה, מטפסת"},

    # ==================== דשא ====================
    {"id": "lawn_warm", "name_he": "דשא חם (ברמודה/קיקויו)", "name_en": "Warm Season Grass", "category": "medium", "moisture_min": 35, "moisture_max": 60, "temp_min": 15, "temp_max": 40, "water_tip_he": "השקה עמוקה פעם-פעמיים בשבוע"},
    {"id": "lawn_cool", "name_he": "דשא קר (רגרס/פסטוקה)", "name_en": "Cool Season Grass", "category": "high", "moisture_min": 45, "moisture_max": 70, "temp_min": 5, "temp_max": 28, "water_tip_he": "השקה בקביעות, רגיש לחום"},
]


def get_all_plants():
    """מחזיר את כל סוגי הצמחים"""
    return PLANTS


def get_plant_by_id(plant_id):
    """מחזיר צמח לפי ID"""
    for plant in PLANTS:
        if plant['id'] == plant_id:
            return plant
    return None


def search_plants(query):
    """חיפוש צמחים לפי שם (עברית או אנגלית)"""
    query = query.lower().strip()
    if not query:
        return PLANTS

    results = []
    for plant in PLANTS:
        if (query in plant['name_he'].lower() or
            query in plant['name_en'].lower() or
            query in plant['id'].lower()):
            results.append(plant)

    return results
