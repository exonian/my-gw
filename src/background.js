var any_language_regex = /games-workshop.com\/\w{2}-\w{2}/;
var view_all_query_string = "&view=all";
var my_language_code, my_language_string, my_language_regex;
var view_all;

function getPreferences() {
    chrome.storage.local.get(function(obj) {
        my_language_code = obj['gwLang'] || 'en-GB';
        my_language_string = 'games-workshop.com/' + my_language_code;
        my_language_regex = new RegExp(my_language_string);
        view_all = obj['gwViewAll'] || false;
    });
}

function checkAndRedirect(details) {
    if (!details.url.match(my_language_regex) && details.url.match(any_language_regex)) {
        return {redirectUrl: details.url.replace(any_language_regex, my_language_string)};
    };
    if (details.url.includes("product.endDate")) {
        if (view_all && !details.url.endsWith(view_all_query_string)) {
            return {redirectUrl: details.url + view_all_query_string};
        }
        else if (!view_all && details.url.endsWith(view_all_query_string)) {
            return {redirectUrl: details.url.replace(view_all_query_string, "")};
        };
    };
}

var url_filters = {
    urls: ["*://*.games-workshop.com/*-*/*"]
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    chrome.storage.local.set(request, getPreferences);
});

getPreferences();
chrome.webRequest.onBeforeRequest.addListener(
    checkAndRedirect,
    url_filters,
    ["blocking"]
);
