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
    chrome.runtime.sendMessage({gwLang: language_code}, function() {location.reload()});
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

$(document).on("DOMNodeInserted", "div.instagram-modal .modal", function(e) {
    var $authorName = $(this).find('.test-author-name');
    if ($authorName.length && !($authorName.find('a')).length) {
        var username = $(this).find('.test-author-img').attr('alt');
        $authorName.html("<a href='https://instagram.com/" + username + "' target='_blank'>"+ $authorName.html() + " 🔗</a>");
    }
});
