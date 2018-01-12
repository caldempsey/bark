/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function toggleNav() {

    if (document.getElementById("sidenav").style.width === "250px") {
        document.getElementById("sidenav").style.width = "0";
        document.getElementById("main").style.marginLeft = "0";
    } else {

        document.getElementById("sidenav").style.width = "250px";
        document.getElementById("main").style.marginLeft = "250px";

    }
}
