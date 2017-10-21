var locale_link_identifier = "countrySelectorStoreLocaleId=";

$("body").on("click", "a[href*='" + locale_link_identifier + "']", function(e) {
    var parts = this.href.split(locale_link_identifier)[1].split('-');
    var language_code = parts[0] + '-' + parts[1].toUpperCase();
    e.preventDefault();
    chrome.runtime.sendMessage({gwLang: language_code}, function() {location.reload()});
});
