var any_language_fw_regex = /forgeworld.co.uk\/\w{2}-\w{2}/;
var any_language_gw_regex = /games-workshop.com\/\w{2}-\w{2}/;
var view_all_query_string = "&view=all";
var my_language_code, my_language_fw_string, my_language_fw_regex, my_language_gw_string, my_language_gw_regex;
var view_all;

function getPreferences() {
    chrome.storage.local.get(function(obj) {
        my_language_code = obj['gwLang'] || 'en-GB';
        my_language_fw_string = 'forgeworld.co.uk/' + my_language_code;
        my_language_fw_regex = new RegExp(my_language_fw_string);
        my_language_gw_string = 'games-workshop.com/' + my_language_code;
        my_language_gw_regex = new RegExp(my_language_gw_string);
        view_all = obj['gwViewAll'] || false;
    });
}

function checkAndRedirect(details) {
    if (!details.url.match(my_language_fw_regex) && details.url.match(any_language_fw_regex)) {
        return {redirectUrl: details.url.replace(any_language_fw_regex, my_language_fw_string)};
    };
    if (!details.url.match(my_language_gw_regex) && details.url.match(any_language_gw_regex)) {
        return {redirectUrl: details.url.replace(any_language_gw_regex, my_language_gw_string)};
    };
    if (details.url.includes("product.endDate") || details.url.includes("searchResults")) {
        if (view_all && !details.url.endsWith(view_all_query_string)) {
            return {redirectUrl: details.url + view_all_query_string};
        }
        else if (!view_all && details.url.endsWith(view_all_query_string)) {
            return {redirectUrl: details.url.replace(view_all_query_string, "")};
        };
    };
}

var url_filters = {
    urls: ["*://*.forgeworld.co.uk/*-*/*", "*://*.games-workshop.com/*-*/*"]
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
