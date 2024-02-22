function reScroll() {
    /* Waiting for tocboc to do its own scroll then scroll up a bit
       because of the sticky/fixed header. Fragile. */
    setTimeout(() => {
        window.scrollTo({
            top: window.scrollY - 130,
            behavior: 'smooth',
        })
    }, 800)
}

function getSetting(name) {
    return document
        .querySelector(`meta[property="pressoir:${name}"]`)
        .getAttribute('content')
}
