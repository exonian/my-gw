var any_language_regex = /games-workshop.com\/\w{2}-\w{2}/;
var my_language_code, my_language_string, my_language_regex;

function getMyLanguage() {
    chrome.storage.local.get(function(obj) {
        my_language_code = obj['gwLang'] || 'en-GB';
        my_language_string = 'games-workshop.com/' + my_language_code;
        my_language_regex = new RegExp(my_language_string);
    });
}

function checkAndRedirect(details) {
    if (!details.url.match(my_language_regex) && details.url.match(any_language_regex)) {
        return {redirectUrl: details.url.replace(any_language_regex, my_language_string)};
    }
}

var url_filters = {
    urls: ["*://*.games-workshop.com/*-*/*"]
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    chrome.storage.local.set(request, getMyLanguage);
});

getMyLanguage();
chrome.webRequest.onBeforeRequest.addListener(
    checkAndRedirect,
    url_filters,
    ["blocking"]
);
