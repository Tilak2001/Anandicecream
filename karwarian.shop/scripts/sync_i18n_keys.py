"""Insert missing i18n keys into kn/hi from en + localized strings."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS_PATH = ROOT / 'static' / 'js' / 'i18n' / 'translations.js'

EXTRA_EN = {
    "label.age": "Age",
    "label.height": "Height",
    "label.fathers_name": "Father's Name",
    "label.gender": "Gender",
    "label.qualification": "Qualification",
    "label.occupation": "Occupation",
    "label.address": "Address",
    "label.additional_info": "Additional Information",
    "label.full_name": "Full Name",
    "label.contact_phone": "Contact Phone",
    "label.contact_email": "Contact Email",
    "common.years": "Years",
    "common.na": "N/A",
    "gender.male": "Male",
    "gender.female": "Female",
    "form.basic_info": "Basic Information",
    "form.education_occupation": "Education & Occupation",
    "form.contact_address": "Contact & Address",
    "form.select_gender": "Select Gender",
    "form.select_caste": "Select Caste",
}

LOCALIZED = {
    "kn": {
        "matrimony.filter_caste": "ಸಮುದಾಯ / ಜಾತಿ ಪ್ರಕಾರ ಫಿಲ್ಟರ್",
        "matrimony.profile_photo": "ಪ್ರೊಫೈಲ್ ಫೋಟೋ",
        "matrimony.photo_hint": "ಸ್ಪಷ್ಟ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ (JPG ಅಥವಾ PNG)",
        "matrimony.personal_details": "ವೈಯಕ್ತಿಕ ವಿವರಗಳು",
        "matrimony.education_work": "ಶಿಕ್ಷಣ ಮತ್ತು ಉದ್ಯೋಗ",
        "matrimony.contact_now": "ಈಗ ಸಂಪರ್ಕಿಸಿ",
        "matrimony.approval_note": "ನಿರ್ವಾಹಕ ಅನುಮೋದನೆಯ ನಂತರ ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಕಾಣಿಸುತ್ತದೆ",
        "matrimony.back_list": "ಪ್ರೊಫೈಲ್‌ಗಳಿಗೆ ಹಿಂತಿರುಗಿ",
        "matrimony.contact_section": "ಸಂಪರ್ಕ",
        "matrimony.no_contact": "ಸಂಪರ್ಕ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ.",
        "matrimony.view_full": "ಪೂರ್ಣ ಪ್ರೊಫೈಲ್ ನೋಡಿ",
        "shm.hub.title": "ಎರಡನೇ ಕೈ ಮಾರುಕಟ್ಟೆ",
        "shm.hub.desc": "ಕಾರವಾರದಲ್ಲಿ ಬಳಸಿದ ವಸ್ತುಗಳನ್ನು ಖರೀದಿ ಮತ್ತು ಮಾರಾಟ — ಫರ್ನಿಚರ್, ಬೈಕ್, ಎಲೆಕ್ಟ್ರಾನಿಕ್ಸ್",
        "shm.hub.listings": "ಸಕ್ರಿಯ ಪಟ್ಟಿಗಳು",
        "shm.hub.all_goods": "ಎಲ್ಲಾ ಸರಕು ಮತ್ತು ಸೇವೆಗಳು",
        "shm.hub.all_goods_desc": "ವಿಧಿ ಸೇವೆಗಳು, ಬಾಡಿಗೆ, ಸರಕು ಮತ್ತು ಅನುಮೋದಿತ ಪಟ್ಟಿಗಳು",
        "shm.hub.items": "ವಸ್ತುಗಳು",
        "shm.add_item": "ಎರಡನೇ ಕೈ ವಸ್ತು ಸೇರಿಸಿ",
        "shm.sell_item": "ಎರಡನೇ ಕೈ ವಸ್ತು ಮಾರಾಟ",
        "shm.list.subtitle": "ಕಾರವಾರ ಸ್ಥಳೀಯರ ಪಟ್ಟಿ ಮಾಡಿದ ಬಳಸಿದ ವಸ್ತುಗಳನ್ನು ಬ್ರೌಸ್ ಮಾಡಿ",
        "shm.all_items": "ಎಲ್ಲಾ ವಸ್ತುಗಳು",
        "shm.category": "ವರ್ಗ",
        "shm.results": "ಫಲಿತಾಂಶಗಳು",
        "shm.search_ph": "ಕಾರವಾರದಲ್ಲಿ ಎರಡನೇ ಕೈ ವಸ್ತುಗಳನ್ನು ಹುಡುಕಿ…",
        "shm.no_image": "ಚಿತ್ರ ಇಲ್ಲ",
        "shm.empty": "ಈ ವರ್ಗದಲ್ಲಿ ಇನ್ನೂ ಯಾವುದೇ ವಸ್ತುಗಳಿಲ್ಲ.",
        "shm.be_first": "ಮೊದಲ ಪಟ್ಟಿ ಮಾಡುವವರಾಗಿರಿ!",
        "shm.form.title": "ನಿಮ್ಮ ವಸ್ತು ಮಾರಾಟ ಮಾಡಿ",
        "shm.form.subtitle": "ನಿಮ್ಮ ಪಟ್ಟಿ ಪ್ರಕಟವಾಗುವ ಮೊದಲು ಪರಿಶೀಲಿಸಲಾಗುತ್ತದೆ",
        "shm.field.title": "ವಸ್ತುವಿನ ಹೆಸರು",
        "shm.field.description": "ವಿವರಣೆ",
        "shm.field.price": "ಬೆಲೆ",
        "shm.field.location": "ನಗರ / ಪ್ರದೇಶ",
        "shm.field.photo": "ಫೋಟೋ",
        "shm.field.photo_hint": "JPG, PNG ಅಥವಾ WebP ಶಿಫಾರಸು",
        "shm.submit": "ಪರಿಶೀಲನೆಗೆ ಸಲ್ಲಿಸಿ",
        "shm.back_list": "ಪಟ್ಟಿಗಳಿಗೆ ಹಿಂತಿರುಗಿ",
        "label.age": "ವಯಸ್ಸು",
        "label.height": "ಎತ್ತರ",
        "label.fathers_name": "ತಂದೆಯ ಹೆಸರು",
        "label.gender": "ಲಿಂಗ",
        "label.qualification": "ಅರ್ಹತೆ",
        "label.occupation": "ಉದ್ಯೋಗ",
        "label.address": "ವಿಳಾಸ",
        "label.additional_info": "ಹೆಚ್ಚುವರಿ ಮಾಹಿತಿ",
        "label.full_name": "ಪೂರ್ಣ ಹೆಸರು",
        "label.contact_phone": "ಸಂಪರ್ಕ ಫೋನ್",
        "label.contact_email": "ಸಂಪರ್ಕ ಇಮೇಲ್",
        "common.years": "ವರ್ಷ",
        "common.na": "ಲಭ್ಯವಿಲ್ಲ",
        "gender.male": "ಪುರುಷ",
        "gender.female": "ಮಹಿಳೆ",
        "form.basic_info": "ಮೂಲ ಮಾಹಿತಿ",
        "form.education_occupation": "ಶಿಕ್ಷಣ ಮತ್ತು ಉದ್ಯೋಗ",
        "form.contact_address": "ಸಂಪರ್ಕ ಮತ್ತು ವಿಳಾಸ",
        "form.select_gender": "ಲಿಂಗ ಆಯ್ಕೆಮಾಡಿ",
        "form.select_caste": "ಜಾತಿ ಆಯ್ಕೆಮಾಡಿ",
        "card.second_hand.title": "ಎರಡನೇ ಕೈ",
    },
    "hi": {
        "matrimony.filter_caste": "समुदाय / जाति से फ़िल्टर",
        "matrimony.profile_photo": "प्रोफ़ाइल फोटो",
        "matrimony.photo_hint": "स्पष्ट फोटो अपलोड करें (JPG या PNG)",
        "matrimony.personal_details": "व्यक्तिगत विवरण",
        "matrimony.education_work": "शिक्षा और कार्य",
        "matrimony.contact_now": "अभी संपर्क करें",
        "matrimony.approval_note": "एडमिन की मंजूरी के बाद आपकी प्रोफ़ाइल दिखेगी",
        "matrimony.back_list": "प्रोफ़ाइल पर वापस",
        "matrimony.contact_section": "संपर्क",
        "matrimony.no_contact": "संपर्क जानकारी उपलब्ध नहीं।",
        "matrimony.view_full": "पूरी प्रोफ़ाइल देखें",
        "shm.hub.title": "सेकंड हैंड मार्केटप्लेस",
        "shm.hub.desc": "कारवार में पुरानी चीज़ें खरीदें और बेचें — फर्नीचर, बाइक, इलेक्ट्रॉनिक्स",
        "shm.hub.listings": "सक्रिय लिस्टिंग",
        "shm.hub.all_goods": "सभी सामान और सेवाएं",
        "shm.hub.all_goods_desc": "समारोह सेवाएं, किराया, सामान और स्वीकृत लिस्टिंग",
        "shm.hub.items": "आइटम",
        "shm.add_item": "सेकंड हैंड आइटम जोड़ें",
        "shm.sell_item": "सेकंड हैंड आइटम बेचें",
        "shm.list.subtitle": "कारवार स्थानीयों द्वारा सूचीबद्ध पुरानी वस्तुएं देखें",
        "shm.all_items": "सभी आइटम",
        "shm.category": "श्रेणी",
        "shm.results": "परिणाम",
        "shm.search_ph": "कारवार में सेकंड हैंड आइटम खोजें…",
        "shm.no_image": "कोई छवि नहीं",
        "shm.empty": "इस श्रेणी में अभी कोई आइटम नहीं।",
        "shm.be_first": "सबसे पहले लिस्ट करें!",
        "shm.form.title": "अपना आइटम बेचें",
        "shm.form.subtitle": "लाइव होने से पहले आपकी लिस्ट की समीक्षा होगी",
        "shm.field.title": "आइटम का नाम",
        "shm.field.description": "विवरण",
        "shm.field.price": "कीमत",
        "shm.field.location": "शहर / क्षेत्र",
        "shm.field.photo": "फोटो",
        "shm.field.photo_hint": "JPG, PNG या WebP अनुशंसित",
        "shm.submit": "समीक्षा के लिए जमा करें",
        "shm.back_list": "लिस्टिंग पर वापस",
        "label.age": "आयु",
        "label.height": "ऊंचाई",
        "label.fathers_name": "पिता का नाम",
        "label.gender": "लिंग",
        "label.qualification": "योग्यता",
        "label.occupation": "व्यवसाय",
        "label.address": "पता",
        "label.additional_info": "अतिरिक्त जानकारी",
        "label.full_name": "पूरा नाम",
        "label.contact_phone": "संपर्क फोन",
        "label.contact_email": "संपर्क ईमेल",
        "common.years": "वर्ष",
        "common.na": "उपलब्ध नहीं",
        "gender.male": "पुरुष",
        "gender.female": "महिला",
        "form.basic_info": "मूल जानकारी",
        "form.education_occupation": "शिक्षा और व्यवसाय",
        "form.contact_address": "संपर्क और पता",
        "form.select_gender": "लिंग चुनें",
        "form.select_caste": "जाति चुनें",
        "card.second_hand.title": "सेकंड हैंड",
    },
}


def extract_lang_block(text, lang):
    m = re.search(rf'{lang}:\s*\{{', text)
    start = m.end()
    depth = 1
    i = start
    while i < len(text) and depth:
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
        i += 1
    chunk = text[start : i - 1]
    keys = dict(re.findall(r'"([^"]+)":\s*"((?:[^"\\]|\\.)*)"', chunk))
    return keys, start, i - 1


def js_escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def main():
    text = JS_PATH.read_text(encoding='utf-8')
    en_keys, _, _ = extract_lang_block(text, 'en')

    for key, val in EXTRA_EN.items():
        if key not in en_keys:
            en_keys[key] = val

    # Patch en block - insert before closing
    for lang in ('kn', 'hi'):
        keys, start, end = extract_lang_block(text, lang)
        merged = {**keys}
        for k, v in en_keys.items():
            if k not in merged:
                merged[k] = LOCALIZED[lang].get(k, en_keys[k])
        for k, v in LOCALIZED[lang].items():
            merged[k] = v

        lines = [f'    "{k}": "{js_escape(merged[k])}",' for k in sorted(merged.keys())]
        new_block = '\n'.join(lines)
        text = text[:start] + '\n' + new_block + '\n  ' + text[end:]

    # Rebuild en with extras
    keys_en, start_en, end_en = extract_lang_block(text, 'en')
    for k, v in EXTRA_EN.items():
        keys_en[k] = v
    lines_en = [f'    "{k}": "{js_escape(keys_en[k])}",' for k in sorted(keys_en.keys())]
    text = text[:start_en] + '\n' + '\n'.join(lines_en) + '\n  ' + text[end_en:]

    JS_PATH.write_text(text, encoding='utf-8')
    print('Updated', JS_PATH)
    print('en keys:', len(keys_en), 'kn/hi synced')


if __name__ == '__main__':
    main()
