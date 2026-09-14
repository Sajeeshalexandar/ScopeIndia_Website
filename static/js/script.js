        const navbarToggler = document.getElementById("navbarToggler");
        const navigationLinks = document.querySelector(".navigation-links");

        navbarToggler.addEventListener("click", function () {
            navigationLinks.classList.toggle("active");
        });







        
        const navLinks = document.querySelectorAll('.navigation-links a');
        const activeLink = localStorage.getItem('activeNav');
        if (activeLink) {
            navLinks.forEach(link => {
                if (link.getAttribute('href') === activeLink) {
                    link.classList.add('active');
                }
            });
        }
        navLinks.forEach(link => {
            link.addEventListener('click', function () {
                navLinks.forEach(item => {
                    item.classList.remove('active');
                });
                this.classList.add('active');
                localStorage.setItem('activeNav', this.getAttribute('href'));
            });
        });
