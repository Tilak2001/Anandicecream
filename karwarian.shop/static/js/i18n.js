/**
 * Karwarian.shop — full-site language switcher (English, Kannada, Hindi)
 * Static dictionary + Django API for saved preference + English fallback.
 */
(function () {
    'use strict';

    const STORAGE_KEY = 'karwarian-lang';
    const API_SET = '/api/i18n/set-language/';
    const API_CURRENT = '/api/i18n/current/';
    const translations = window.KARWARIAN_TRANSLATIONS || { en: {}, kn: {}, hi: {} };

    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? decodeURIComponent(match[2]) : null;
    }

    function getCsrfToken() {
        return getCookie('csrftoken');
    }

    function getLang() {
        const saved = localStorage.getItem(STORAGE_KEY);
        const cookieLang = getCookie('karwarian_lang');
        const candidate = saved || cookieLang;
        return candidate && translations[candidate] ? candidate : 'en';
    }

    function lookup(key, lang) {
        const lng = lang || getLang();
        const dict = translations[lng] || {};
        if (dict[key] !== undefined && dict[key] !== '') {
            return dict[key];
        }
        const en = translations.en || {};
        if (en[key] !== undefined) {
            return en[key];
        }
        return key;
    }

    function t(key, lang) {
        return lookup(key, lang);
    }

    function applyToElement(el, text) {
        if (el.hasAttribute('data-i18n-html')) {
            el.innerHTML = text;
        } else if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            if (el.hasAttribute('data-i18n-placeholder') || el.getAttribute('data-i18n-placeholder')) {
                el.placeholder = text;
            }
        } else if (el.tagName === 'OPTION') {
            el.textContent = text;
        } else {
            el.textContent = text;
        }
    }

    function applyLanguage(lang) {
        if (!translations[lang]) {
            lang = 'en';
        }

        const htmlLang = lang === 'kn' ? 'kn' : lang === 'hi' ? 'hi' : 'en';
        document.documentElement.lang = htmlLang;

        document.querySelectorAll('[data-i18n]').forEach(function (el) {
            const key = el.getAttribute('data-i18n');
            applyToElement(el, lookup(key, lang));
        });

        document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
            const key = el.getAttribute('data-i18n-placeholder');
            if (!el.hasAttribute('data-i18n')) {
                el.placeholder = lookup(key, lang);
            }
        });

        document.querySelectorAll('[data-i18n-title]').forEach(function (el) {
            const key = el.getAttribute('data-i18n-title');
            el.title = lookup(key, lang);
        });

        document.querySelectorAll('[data-i18n-value]').forEach(function (el) {
            const key = el.getAttribute('data-i18n-value');
            el.value = lookup(key, lang);
        });

        const docTitleKey = document.body && document.body.getAttribute('data-i18n-doc-title');
        if (docTitleKey) {
            document.title = lookup(docTitleKey, lang);
        }

        document.querySelectorAll('#languageSelect, #languageSelectMobile, #languageSelectIce').forEach(function (sel) {
            if (sel) sel.value = lang;
        });

        localStorage.setItem(STORAGE_KEY, lang);
        document.body.setAttribute('data-lang', lang);
        document.dispatchEvent(new CustomEvent('karwarian:language-changed', { detail: { lang: lang } }));
    }

    function persistLanguageToServer(lang) {
        return fetch(API_SET, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() || '',
            },
            credentials: 'same-origin',
            body: JSON.stringify({ lang: lang }),
        }).then(function (res) {
            if (!res.ok) {
                throw new Error('Failed to save language');
            }
            return res.json();
        });
    }

    function fetchServerLanguage() {
        return fetch(API_CURRENT, { credentials: 'same-origin' })
            .then(function (res) {
                if (!res.ok) return null;
                return res.json();
            })
            .then(function (data) {
                if (data && data.lang && translations[data.lang]) {
                    return data.lang;
                }
                return null;
            })
            .catch(function () {
                return null;
            });
    }

    function setLanguage(lang) {
        if (!translations[lang]) {
            lang = 'en';
        }
        applyLanguage(lang);
        return persistLanguageToServer(lang).catch(function () {
            /* localStorage still holds preference */
        });
    }

    function initLanguage() {
        var initial = getLang();
        if (document.body && document.body.getAttribute('data-initial-lang')) {
            var serverHint = document.body.getAttribute('data-initial-lang');
            if (translations[serverHint]) {
                initial = serverHint;
            }
        }

        applyLanguage(initial);

        fetchServerLanguage().then(function (serverLang) {
            if (serverLang && serverLang !== getLang()) {
                applyLanguage(serverLang);
            }
        });

        document.querySelectorAll('#languageSelect, #languageSelectMobile, #languageSelectIce').forEach(function (sel) {
            if (!sel) return;
            sel.addEventListener('change', function (e) {
                setLanguage(e.target.value);
            });
        });
    }

    window.karwarianI18n = {
        applyLanguage: applyLanguage,
        setLanguage: setLanguage,
        getLang: getLang,
        t: t,
        lookup: lookup,
        translations: translations,
        api: {
            setLanguage: API_SET,
            current: API_CURRENT,
            languages: '/api/i18n/languages/',
        },
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLanguage);
    } else {
        initLanguage();
    }
})();
