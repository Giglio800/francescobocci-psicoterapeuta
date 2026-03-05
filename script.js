/* ============================================================
   DOTT. FRANCESCO BOCCI — Landing Page JS
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ---- NAVBAR SCROLL ---- */
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });

  /* ---- HAMBURGER MENU ---- */
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('nav-links');
  hamburger.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    hamburger.classList.toggle('open', open);
    hamburger.setAttribute('aria-expanded', open);
  });
  // Chiudi menu al click su link
  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      navLinks.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', false);
    });
  });

  /* ---- COOKIE BANNER ---- */
  const banner = document.getElementById('cookie-banner');
  const btnCookie = document.getElementById('cookie-accept');
  if (localStorage.getItem('cookie-accepted')) {
    banner.style.display = 'none';
  }
  btnCookie.addEventListener('click', () => {
    localStorage.setItem('cookie-accepted', '1');
    banner.style.display = 'none';
  });

  /* ---- SMOOTH SCROLL per link interni ---- */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      const offset = 76;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  /* ---- SCROLL REVEAL ---- */
  const revealEls = document.querySelectorAll(
    '.servizio-card, .dimensione-card, .ruolo-card, .pub-card, .sede-card, ' +
    '.approccio-block, .psicodiagnosi-block, .collaboratori-block, .form-item'
  );
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
    el.style.transition = 'opacity .5s ease, transform .5s ease';
    observer.observe(el);
  });

  /* ---- CONTACT FORM ---- */
  const form = document.getElementById('contact-form');
  const successMsg = document.getElementById('form-success');
  const errorMsg   = document.getElementById('form-error');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      successMsg.hidden = true;
      errorMsg.hidden   = true;

      // Validazione base
      const nome     = form.nome.value.trim();
      const email    = form.email.value.trim();
      const messaggio = form.messaggio.value.trim();
      const privacy  = form.privacy.checked;

      if (!nome || !email || !messaggio || !privacy) {
        errorMsg.querySelector('p').textContent =
          'Per favore compila tutti i campi obbligatori e accetta la Privacy Policy.';
        errorMsg.hidden = false;
        return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errorMsg.querySelector('p').textContent = 'Inserisci un indirizzo email valido.';
        errorMsg.hidden = false;
        return;
      }

      const btn = form.querySelector('.btn-submit');
      btn.disabled = true;
      btn.textContent = 'Invio in corso...';

      // Invio via Formspree (sostituire con endpoint reale)
      try {
        const res = await fetch('https://formspree.io/f/xpwzgkqr', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({
            nome:     form.nome.value,
            email:    form.email.value,
            telefono: form.telefono.value,
            sede:     form.sede.value,
            servizio: form.servizio.value,
            messaggio: form.messaggio.value,
            _subject: `Richiesta di appuntamento da ${form.nome.value}`
          })
        });
        if (res.ok) {
          successMsg.hidden = false;
          form.reset();
        } else {
          throw new Error('Server error');
        }
      } catch {
        // Fallback: apri mailto
        const subject = encodeURIComponent(`Richiesta appuntamento - ${nome}`);
        const body = encodeURIComponent(
          `Nome: ${nome}\nEmail: ${email}\nTelefono: ${form.telefono.value}\n` +
          `Sede: ${form.sede.value}\nServizio: ${form.servizio.value}\n\n${messaggio}`
        );
        window.location.href = `mailto:fbocci80@gmail.com?subject=${subject}&body=${body}`;
        successMsg.querySelector('p').textContent =
          '✓ Si aprirà il tuo client email. In alternativa scrivi direttamente a fbocci80@gmail.com';
        successMsg.hidden = false;
      } finally {
        btn.disabled = false;
        btn.textContent = 'Invia la richiesta';
      }
    });
  }

  /* ---- ACTIVE NAV LINK su scroll ---- */
  const sections = document.querySelectorAll('section[id]');
  const navItems = document.querySelectorAll('.nav-links a[href^="#"]');
  const activateNav = () => {
    let current = '';
    sections.forEach(sec => {
      if (window.scrollY >= sec.offsetTop - 120) current = sec.id;
    });
    navItems.forEach(a => {
      a.classList.toggle('active', a.getAttribute('href') === `#${current}`);
    });
  };
  window.addEventListener('scroll', activateNav, { passive: true });

});
