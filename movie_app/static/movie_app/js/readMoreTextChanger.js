let clicked = false;

document.getElementById("readMoreLink").onclick = () => {
    if (!clicked) {
        clicked = true
        document.getElementById("readMore").textContent = "Read less...";
        document.getElementById("readMore").id = 'readLess';
        document.getElementById("readMoreLink").href = "#readLess";
        document.getElementById("readMoreLink").id = "readLessLink";
    } else {
        clicked = false
        document.getElementById("readLess").textContent = "Read more...";
        document.getElementById("readLess").id = 'readMore';
        document.getElementById("readLessLink").href = "#readMore";
        document.getElementById("readLessLink").id = "readMoreLink";
    }
};
