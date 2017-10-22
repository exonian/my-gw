var locale_link_identifier = "countrySelectorStoreLocaleId=";

$("body").on("click", "a[href*='" + locale_link_identifier + "']", function(e) {
    var parts = this.href.split(locale_link_identifier)[1].split('-');
    var language_code = parts[0] + '-' + parts[1].toUpperCase();
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
