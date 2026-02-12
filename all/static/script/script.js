// Warning Button Functions
let accept = () => {
    document.querySelector("#warning").classList.add("hide");
    localStorage.setItem("adult_consent", "true");
}
let decline = () => {
    window.location.href = "https://google.com";
}
