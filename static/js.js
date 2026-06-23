document.addEventListener("DOMContentLoaded", () => {

/*
==========================
TOAST NOTIFICATIONS
==========================
*/

const notifications = document.querySelectorAll(".notification");

notifications.forEach((notification, index) => {

    notification.style.opacity = "0";
    notification.style.transform = "translateY(-10px)";

    setTimeout(() => {
        notification.style.transition = "0.3s ease";
        notification.style.opacity = "1";
        notification.style.transform = "translateY(0)";
    }, index * 100);

    setTimeout(() => {
        notification.style.opacity = "0";
        notification.style.transform = "translateX(30px)";

        setTimeout(() => {
            notification.remove();
        }, 300);

    }, 4000);
});

/*
==========================
MOBILE MENU
==========================
*/

const burger = document.getElementById("burger");
const nav = document.getElementById("nav");

if (burger && nav) {

    burger.addEventListener("click", () => {

        burger.classList.toggle("active");
        nav.classList.toggle("nav-mobile-open");

        document.body.classList.toggle("menu-open");
    });

    document.addEventListener("click", (event) => {

        const insideNav = nav.contains(event.target);
        const insideBurger = burger.contains(event.target);

        if (
            !insideNav &&
            !insideBurger &&
            nav.classList.contains("nav-mobile-open")
        ) {
            nav.classList.remove("nav-mobile-open");
            burger.classList.remove("active");
            document.body.classList.remove("menu-open");
        }
    });

    nav.querySelectorAll("a").forEach(link => {

        link.addEventListener("click", () => {

            nav.classList.remove("nav-mobile-open");
            burger.classList.remove("active");
            document.body.classList.remove("menu-open");
        });
    });
}

/*
==========================
BURGER ANIMATION
==========================
*/

if (burger) {

    burger.addEventListener("click", () => {

        const spans = burger.querySelectorAll("span");

        if (burger.classList.contains("active")) {

            spans[0].style.transform =
                "translateY(6px) rotate(45deg)";

            spans[1].style.opacity = "0";

            spans[2].style.transform =
                "translateY(-6px) rotate(-45deg)";

        } else {

            spans[0].style.transform = "";
            spans[1].style.opacity = "1";
            spans[2].style.transform = "";
        }
    });
}

/*
==========================
SMOOTH SCROLL
==========================
*/

document.querySelectorAll('a[href^="#"]').forEach(link => {

    link.addEventListener("click", function (e) {

        const target = document.querySelector(
            this.getAttribute("href")
        );

        if (!target) return;

        e.preventDefault();

        target.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    });
});

/*
==========================
SCROLL REVEAL
==========================
*/

const revealElements = document.querySelectorAll(
    ".card, .section-title, .reveal"
);

const observer = new IntersectionObserver(

    entries => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

                observer.unobserve(entry.target);
            }
        });

    },

    {
        threshold: 0.15
    }
);

revealElements.forEach(element => {

    element.classList.add("hidden");

    observer.observe(element);
});

/*
==========================
HEADER SCROLL EFFECT
==========================
*/

const header = document.querySelector(".header");

window.addEventListener("scroll", () => {

    if (window.scrollY > 30) {

        header.classList.add("header-scrolled");

    } else {

        header.classList.remove("header-scrolled");
    }
});

});
