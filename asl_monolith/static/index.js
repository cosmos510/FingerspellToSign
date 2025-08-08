// Lightweight language toggle (no framework)
const TRANSLATIONS = {
  en: {
    navHome: 'Home',
    navPredict: 'Predict',
    navAbout: 'About',
    secHow: 'How it works',
    secHighlights: 'Highlights',
    secPractice: 'Practice',
    secAbout: 'About',
    heroTitle: 'Learn ASL letters in real‑time',
    heroSubtitle: 'Practice the ASL alphabet with instant feedback—right in your browser.',
    highlightsTitle: 'Key capabilities',
    h1: 'ASL Recognition',
    practiceCta: 'Start practicing',
    tryTitle: 'Ready to try?',
    trySubtitle: 'Open the camera and start signing.',
    tryButton: 'Try now'
  },
  fr: {
    navHome: 'Accueil',
    navPredict: 'Prédire',
    navAbout: 'À propos',
    secHow: 'Comment ça marche',
    secHighlights: 'Points forts',
    secPractice: 'Pratique',
    secAbout: 'À propos',
    heroTitle: 'Apprenez les lettres de l’ASL en temps réel',
    heroSubtitle: 'Pratiquez l’alphabet ASL avec un retour instantané — directement dans votre navigateur.',
    highlightsTitle: 'Fonctionnalités clés',
    h1: 'Reconnaissance ASL',
    practiceCta: 'Commencer',
    tryTitle: 'Prêt à essayer ?',
    trySubtitle: 'Ouvrez la caméra et commencez à signer.',
    tryButton: 'Essayer'
  }
};

function setLang(lang) {
  const t = TRANSLATIONS[lang] || TRANSLATIONS.en;
  const el = (sel) => document.querySelector(sel);
  const setText = (sel, text) => { const n = el(sel); if (n && text) n.textContent = text; };
  setText('header h1', t.h1);
  setText('#nav-home', t.navHome);
  setText('#nav-predict', t.navPredict);
  setText('#nav-about', t.navAbout);
  setText('#sec-how', t.secHow);
  setText('#sec-highlights', t.secHighlights);
  setText('#sec-practice', t.secPractice);
  setText('#sec-about', t.secAbout);
  setText('#hero-section .title', t.heroTitle);
  setText('#hero-section .subtitle', t.heroSubtitle);
  setText('#cap-title', t.highlightsTitle);
  setText('#alpha-title', lang === 'fr' ? "Découvrir l’alphabet" : 'Explore the alphabet');
  setText('#alpha-desc', lang === 'fr' ? 'Parcourez les lettres puis essayez en direct.' : 'Browse the letters, then try them live.');
  setText('#alpha-cta', t.practiceCta);
  // How it works steps
  setText('#hiw-1-h', lang === 'fr' ? 'Ouvrir la caméra' : 'Open camera');
  setText('#hiw-1-p', lang === 'fr' ? 'Autorisez l’accès à la webcam.' : 'Allow webcam access.');
  setText('#hiw-2-h', lang === 'fr' ? 'Signer une lettre' : 'Sign a letter');
  setText('#hiw-2-p', lang === 'fr' ? 'Maintenez une pose nette.' : 'Hold a clear pose.');
  setText('#hiw-3-h', lang === 'fr' ? 'Recevoir le résultat' : 'Get feedback');
  setText('#hiw-3-p', lang === 'fr' ? 'Voyez la prédiction instantanément.' : 'See the prediction instantly.');

  // Capabilities lines
  setText('#cap-1', lang === 'fr' ? 'Détection des lettres en temps réel avec retour visuel clair' : 'Real‑time letter detection with clear visual feedback');
  setText('#cap-2', lang === 'fr' ? 'Composez des mots en direct : confirmez, modifiez rapidement' : 'Build words as you go: confirm letters, edit quickly');
  setText('#cap-3', lang === 'fr' ? 'Fonctionne dans votre navigateur — aucune installation, juste votre webcam' : 'Runs in your browser — no installs, just your webcam');
  setText('#cta-section h2', t.tryTitle);
  setText('#cta-section p', t.trySubtitle);
  setText('#cta-section a.btn.btn-secondary', t.tryButton);
  setText('#aboutproj-title', t.navAbout);
  setText('#aboutproj-p1', lang === 'fr' ? 'ASL Recognition vous aide à pratiquer l’alphabet ASL avec un retour en temps réel — rapide, accessible et facile à prendre en main.' : 'ASL Recognition helps you practice the ASL alphabet with real‑time feedback—fast, approachable, and accessible.');
  setText('#aboutproj-p2', lang === 'fr' ? 'Conçu pour les apprenants, les familles et les enseignants. Conseils clairs, résultats instantanés.' : 'Designed for learners, families, and educators. Clear guidance, instant results.');
  setText('#aboutproj-learn', lang === 'fr' ? 'En savoir plus' : 'Learn more');
  const btn = document.getElementById('lang-toggle');
  if (btn) btn.textContent = lang.toUpperCase();
  localStorage.setItem('lang', lang);
}

document.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('lang') || 'en';
  setLang(saved);
  // If we are on about page, also translate it using the same keys
  const isAbout = window.location.pathname.endsWith('/about');
  if (isAbout) {
    const lang = saved;
    const setText = (sel, text) => { const n = document.querySelector(sel); if (n && text) n.textContent = text; };
    setText('#nav-home', lang === 'fr' ? 'Accueil' : 'Home');
    setText('#nav-predict', lang === 'fr' ? 'Prédire' : 'Predict');
    setText('#nav-about', lang === 'fr' ? 'À propos' : 'About');
    setText('#mission', lang === 'fr' ? 'Notre mission' : 'Our mission');
    setText('#about-mission', lang === 'fr' ? "Rendre la pratique de l’alphabet ASL simple et accueillante pour tous. Nous privilégions la clarté, la rapidité et l’accessibilité pour que chacun puisse communiquer avec confiance." : 'Make practicing the ASL alphabet simple and welcoming for everyone. We focus on clarity, speed, and accessibility so more people can communicate with confidence.');
    setText('#accessibility', lang === 'fr' ? 'Accessibilité' : 'Accessibility');
    const a11yItemsFr = [
      'Navigation au clavier avec états de focus visibles',
      'Couleurs à fort contraste et typographie lisible',
      'Respect des préférences de réduction des animations',
      'Libellés clairs et texte alternatif des images'
    ];
    const a11yList = document.querySelector('#about-a11y-list');
    if (a11yList && lang === 'fr') {
      a11yList.innerHTML = a11yItemsFr.map(t => `<li>${t}</li>`).join('');
    }
    setText('#about-a11y-note', lang === 'fr' ? "Si nous pouvons rendre cette expérience plus accessible pour vous, merci de nous le signaler." : 'If we can make this experience more accessible for you, please open an issue or share feedback.');
    setText('#how-it-works', lang === 'fr' ? 'Fonctionnement' : 'How it works');
    setText('#about-how-1', lang === 'fr' ? 'Votre webcam capture des images qui sont traitées pour reconnaître les lettres ASL. Aucune installation requise : tout fonctionne dans votre navigateur et est envoyé en toute sécurité à l’application pour la prédiction.' : 'Your webcam captures frames which are processed to recognize ASL letters. No installation is required—everything runs in your browser and is sent securely to the app for prediction.');
    setText('#about-how-2', lang === 'fr' ? 'Technologies : Django, MediaPipe, OpenCV, scikit‑learn.' : 'Technology: Django, MediaPipe, OpenCV, scikit‑learn.');
    setText('#links', lang === 'fr' ? 'Liens' : 'Links');
    setText('#about-start', lang === 'fr' ? 'Commencer' : 'Start practicing');
    setText('#about-contact', lang === 'fr' ? 'Contacter Maxime' : 'Contact Maxime');
  }
  const toggle = document.getElementById('lang-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const next = (localStorage.getItem('lang') || 'en') === 'en' ? 'fr' : 'en';
      setLang(next);
    });
  }
});