var locale_link_identifier = "countrySelectorStoreLocaleId=";
var locale_class_prefix = "test-select-locale-";

$("body").on("click", "a[href*='" + locale_link_identifier + "']", function(e) {
    var classes = this.className.split(/\s+/);
    var language_code;
    $.each(classes, function(i, class_name) {
        if (class_name.startsWith(locale_class_prefix)) {
            var parts = language_code = class_name.split(locale_class_prefix)[1].split('-');
            language_code = parts[0] + '-' + parts[1].toUpperCase();
            return false;
        }
    });
    e.preventDefault();
    var gw = window.location.host.includes('games-workshop');
    if (gw) {
        chrome.runtime.sendMessage({gwLang: language_code}, function() {location.reload()});
    }
    else {
        chrome.runtime.sendMessage({fwLang: language_code}, function() {location.reload()});
    }
});

$("body").on("click", "a[href*='product.endDate'].read-more, a[href*='searchResults'].read-more", function(e) {
    e.preventDefault();
    if (this.href.endsWith('view=all')) {
        // currently viewing all, so turning it off
        viewAll = false;
    }
    else {
        viewAll = true;
    }
    chrome.runtime.sendMessage({gwViewAll: viewAll}, function() {location.reload()});
});

$(function() {
    $('.media-area__user-info').each(function() {
        var $userName = $(this).find('span');
        if ($userName.length) {
            $userName.html("<a href='https://instagram.com/" + $userName.text() + "' target='_blank'>"+ $userName.html() + " 🔗</a>");
        };
    });
});
