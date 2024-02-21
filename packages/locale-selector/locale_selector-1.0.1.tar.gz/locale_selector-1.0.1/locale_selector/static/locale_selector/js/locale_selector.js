window._removeLocaleSelector = function(e) {
    let x = document.querySelector(".locale-selector-locales-wrapper");
    let y = document.querySelector("dialog.locale-selector-locales");
    if (x.classList.contains("locale-selector-hidden")) {return};
    if (e.key == "Escape") {
        e.preventDefault();
        x.classList.add("locale-selector-hidden");
        if (y && y.nodeName == "DIALOG") {
            y.close();
        }
        document.removeEventListener("keydown", window._removeLocaleSelector);
    }
};

window.localeSelectorToggle = function(btn) {
    let x = document.querySelector(".locale-selector-locales-wrapper");
    let y = document.querySelector("dialog.locale-selector-locales");

    document.addEventListener("keydown", window._removeLocaleSelector);

    if (x.classList.contains("locale-selector-hidden")) {
        x.classList.remove("locale-selector-hidden");
        if (y && y.nodeName == "DIALOG") {y.showModal();}
    } else {
        x.classList.add("locale-selector-hidden");
        if (y && y.nodeName == "DIALOG") {y.close();}
    }
};
