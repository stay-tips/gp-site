---

########################### hero slider ############################
hero_slider:
  enable : true
  slider_item:
    # slider item
    - subtitle : "I nostri valori"
      title : "Ospitalità"
      content : "Valorizzando le unicità dell'immobile e dei suoi dintorni, assicurando agli ospiti un soggiorno sereno e memorabile."
      bg_image_webp : "images/slider/banner-1.webp"
      bg_image : "images/slider/banner-1.jpg"
      animation : "fadeInUp" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "approfondisci"
        link : "about/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/
        
    # slider item
    - subtitle : "Il nostro metodo"
      title : "Professionalità"
      content : "Abbiamo ingegnierizzato processi unici per garantire il massimo del confort e del rendimento dell'immobile."
      bg_image_webp : "images/slider/banner-2.webp"
      bg_image : "images/slider/banner-2.jpg"
      animation : "fadeInDown" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "approfondisci"
        link : "about/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/
        
    # slider item
    - subtitle : "Il nostro approcio"
      title : "Sostenibilità"
      content : "Crediamo nel turismo etico e responsabile, che rispetti l'ambiente circostante e promuova prodotti e abitudini del territorio, negli affitti brevi"
      bg_image_webp : "images/slider/banner-3.webp"
      bg_image : "images/slider/banner-3.jpg"
      animation : "fadeInLeft" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "approfondisci"
        link : "about/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/
        
    # slider item
    - subtitle : "Garantiamo"
      title : "Massimo rendimento"
      content : "Solo raggiungendo il massimo rendimento dell'immobile possiamo promuovere i nostri valori e condividere con gli ospiti la nostra felicità"
      bg_image_webp : "images/slider/banner-4.webp"
      bg_image : "images/slider/banner-4.jpg"
      animation : "fadeInRight" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "approfondisci"
        link : "about/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/

################################## banner feature ############################
banner_feature:
  enable : true
  # Max use 4 item
  feature_item:

    # banner feature item loop
    # - name : "Business Solution"
    #   icon : "far fa-gem" # font-awesome 5 : https://fontawesome.com/icons/
    #   content : "Lorem ipsum dolor sit amet constur adipelit sed."
      
    # banner feature item loop
    - name : "Epserienze"
      icon : "fas fa-horse" # font-awesome 5 : https://fontawesome.com/icons/
      content : "vi facciamo vivere il territorio come se ci foste nati"
      
    # banner feature item loop
    - name : "Ospitalità"
      icon : "fas fa-house-user" # font-awesome 5 : https://fontawesome.com/icons/
      content : "accoglienti dimore ove sentirsi a casa"
      
    # banner feature item loop
    - name : "Servizi"
      icon : "fas fa-shuttle-van" # font-awesome 5 : https://fontawesome.com/icons/
      content : "copriamo le necessità particolari dei nostri ospiti"


################################## about ####################################
about:
  enable : true
  subtitle : "Chi siamo"
  title : "Siamo una squadra dedicata agli affitti brevi"
  content : "Siamo esperti nel trasformare ogni immobile in un'esperienza unica e redditizia. La nostra squadra si dedica con passione e professionalità a massimizzare il valore dell'immobile. Affidati a noi per una gestione senza pensieri e risultati garantiti."
  bg_image : "images/backgrounds/about-us-bg.png"
  bg_image_webp : "images/backgrounds/about-us-bg.webp"
  image_webp : "images/about/about-us.webp"
  image : "images/about/about-us.png"
  button:
    enable : true;
    label : "contattaci"
    link : "service/"

################################## funfacts ###############################
funfacts :
  enable : true
  funfacts_item :      

    # fanfacts item loop
    - name : "Anni d'esperienza"
      count : "5"
      icon : "far fa-calendar-alt" # font-awesome 5 : https://fontawesome.com/icons/
      
    # fanfacts item loop
    - name : "Immobili gestiti"
      count : "36"
      icon : "fas fa-house-user" # font-awesome 5 : https://fontawesome.com/icons/
      
    # fanfacts item loop
    - name : "Ospiti Soddisfatti"
      count : "5300"
      icon : "far fa-smile" # font-awesome 5 : https://fontawesome.com/icons/


################################# feature ############################################
feature:
  enable : true
  subtitle : "Cosa facciamo noi"
  title : "Le nostre attività"
  image_webp : "images/feature/activities.webp"
  image : "images/feature/activities.png"
  content : "Il nostro impegno costante permette di affittare il tuo immobile meglio e con meno rischi"
  feature_item:
    # Business plan
    - name : "Business Plan"
      icon : "fas fa-ruler-combined" # font-awesome 5 : https://fontawesome.com/icons/
      content : "Redigiamo un business plan personalizzato con previsione di occupazione e ricavi."
    
    # Allestimento
    - name : "Allestimento e shooting fotografico"
      icon : "fas fa-camera" # font-awesome 5 : https://fontawesome.com/icons/
      content : "Professionisti della fotografia e dell' home staging faranno del tuo immobile la miglior vetrina possibile."

    # Burocrazia
    - name : "Burocrazia"
      icon : "fas fa-landmark" # font-awesome 5 : https://fontawesome.com/icons/
      content : "Facciamo noi le pratiche burocratiche necessarie, ci manteniamo aggiornati e garantiamo che l'attività sia sempre in regola."
 
    # Pulizia
    - name : "Pulizia e manutenzione"
      icon : "fas fa-broom" # font-awesome 5 : https://fontawesome.com/icons/
      content : "Garantiamo igiene e pulizia ad ogni check-out avvalendoci solo di partner certificati e controlliamo che l'immobile sia perfettamente mantenuto; l'immobile è la nostra attività e vetrina."

    # Accoglienza
    - name : "Accoglienza e assistenza ospiti"
      icon : "fas fa-door-open" # font-awesome 5 : https://fontawesome.com/icons/
      content : "Accogliamo noi gli ospiti in viaggio gestendo con cura adempimenti e pagamenti."

    # Gestione Prezzi
    - name : "Gestione prezzi"
      icon : "fas fa-money-bill-wave" # font-awesome 5 : https://fontawesome.com/icons/
      content : "Usiamo le migliori tecniche di gestione dei ricavi per affittare l'immobile al miglior prezzo possibile; garantito."
 
################################# service ############################################
service:
  enable : true
  section: "service"
  show_item : 8
  # service item comes from "content/*/service" folder

################################# team ##############################################
team:
  enable : true
  section: "team"
  show_item : 3
  # team member comes from "content/*/team" folder

################################# project ############################################
project:
  enable : true
  section: "project"
  show_item : 4
  button:
    enable : true
    label : "altri casi studio"
    link : "project/"
  # project item comes from "content/*/project" folder

################################# testimonial #########################################
testimonial:
  enable : true
  subtitle : "Testimonianze"
  title : "Cosa dicono i clienti?"
  testimonial_item:
    # testimonial item loop
    - client_image : "images/testimonial/client-1.jpg"
      name : "Elisa"
      designation : "Proprietario"
      content : "Enrico si è dimostrato preparato attento e ha trovato la struttura fiscale giusta per far rendere il mio immobile al massimo, avanti così"
      
    # testimonial item loop
    - client_image : "images/testimonial/client-2.jpg"
      name : "Renato"
      designation : "Proprietario"
      content : "Enrico e i suoi collaboratori gestiscono gli affitti brevi con metodo e concretezza. Sanno organizzare gli spazi, coordinare le pulizie e incontrare le esigenze dei clienti senza troppi fronzoli. Il lavoro richiede capacità pratiche, disciplina e una buona dose di flessibilità, riuscendo a far girare l'attività in modo professionale e amichevole."

    # testimonial item loop
    - client_image : "images/testimonial/client-3.jpg"
      name : "Alessandra"
      designation : "Proprietario"
      content : "Nella gestione degli affitti brevi, Green Property ha portato competenza. Sanno come preparare gli appartamenti, districarsi con la burocrazia, coordinare pulizie e manutenzioni e soprattutto gestire le aspettative dei clienti professionalmente. Sempre reperibili, hanno risolto imprevisti e mantenuto standard di qualità costanti."


################################# blog ################################################
cta:
  enable : true
  title : "Bexar give the smart solution for your business"
  bg_image_webp : "images/backgrounds/cta-lg.webp"
  bg_image : "images/backgrounds/cta-lg.jpg"
  button:
    enable : true
    label : "chiedi valutazione gatuita"
    link : "contact/"

################################# blog ################################################
blog:
  enable : true
  section : "blog"
  show_item : 3
  # blog post comes from "content/*/blog" folder

---
